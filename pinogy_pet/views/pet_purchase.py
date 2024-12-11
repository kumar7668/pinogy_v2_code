import json
import logging
import traceback

from django.http import JsonResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from pos_api.pos_client import PWAPI
from ..forms import PetPurchaseUserForm, PetPaymentForm

logger = logging.getLogger('pet_purchase')

def log_api(url, req_params, response):

    logger.info(json.dumps(dict(
        request=url,
        req_params=req_params,
        response_data=response
    )))

def log_error(title: str, traceback: str) -> None:
    logger.error(f"{title}: {traceback}")


@method_decorator(csrf_exempt, name='dispatch')
class CreateTransactoin(View):

    def create_txn(self, data):

        pet_id = data['pet_id']
        pet_loc_entity_id = data['pet_loc_entity_id']
        user_data = data['user_data']
        product_data = data['addon_data']

        txn_type = "Shopping Cart"

        req_body = {
            "customer": {
                "eml_email": user_data['email'],
                "ent_first_name": user_data['first_name'],
                "ent_last_name": user_data['last_name'],
                "cnum_number": user_data['phone'],
                "addr_address_1": user_data['address'],
                "addr_address_2": user_data.get('address_2', ''),
                "addr_city": user_data['city'],
                "addr_postal_code": user_data['zip'],
                "prgn_iso_code": user_data['state'],
            },
            "txnlines": [
                {
                    "txnline_vertical_product_id": pet_id,
                    "txnline_tax_info": [],
                    "txnline_qty": "1.0",
                    "txnline_vertical_app_id": 3,
                    "txnline_customer_entity_id_req": True,
                    "txnline_children": [{
                        "txnline_product_id": product['product_id'],
                        "txnline_vertical_product_id": product['vertical_product_id'],
                        "txnline_vertical_app_id": 3,
                        "txnline_qty": "1.0",
                        "txnline_required_by_parent": False,
                        "txnline_tax_info": []
                    } for product in product_data],
                }
            ],
            "txn_type" : txn_type,
            "txn_loc_entity_id": pet_loc_entity_id,
        }

        try:
            client = PWAPI()
            result = client.complete_summary(req_body)
            log_api(url='/api/v1/txns', req_params=req_body, response=result)
            
            if "txn_id" in result:
                return True, result
            
            return False, result
        except Exception as e:
            log_error("Error: Creating txn for pet", traceback.format_exc())

        return False, {}

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Something went wrong, please contact admin.'}, status=400)
        
        user_form = PetPurchaseUserForm(data['user_data'])
        if not user_form.is_valid():
            return JsonResponse({'error': user_form.errors.as_ul()}, status=400)
        
        txn_success, api_result = self.create_txn(data)
        if txn_success:
            return JsonResponse({
                'txn_id': api_result['txn_id'],
                'txn_subtotal': api_result['txn_totals']['subtotal'],
                'txn_tax': api_result['txn_totals']['tax'],
                'txn_total': api_result['txn_totals']['total'],
            }, status=201)
        else:
            try:
                error_msg = api_result.get('message')
            except Exception as e:
                error_msg = 'Something went wrong, please contact admin.'
            return JsonResponse({'error': error_msg}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ExecutePayment(View):

    def update_expiry(self, source):
        # cardconnect-iframe get YYYYM instead YYYYMM
        # this must be updated with YYYY0M for month less 10 
        if len(source) == 5:
            return source[:4] + '0' + source[4:]
        else:
            return source

    def send_payment(self, client, payment_data, txn_data):
        txn_id = payment_data['txn_id']
        txn_email = payment_data['email']

        try:
            is_deposit = payment_data["is_deposit"]
            deposit_amount = payment_data["deposit_amount"]

            if is_deposit and deposit_amount > 0.0:
                cost = deposit_amount
            else:
                cost = txn_data["txn_totals"]["total"]

            req_param = {
                "transaction_id": txn_id,
                "token": payment_data['card_token'],
                "expiry": payment_data['card_expiry'],
                "cost": cost,
                "cardholder": payment_data['card_holder'],
                "method": payment_data['card_method'],
            }
            
            payment_result = client.pay(**req_param)
            log_api(
                url=f'/api/v1/txns/{txn_id}/payments',
                req_params=req_param,
                response=payment_result,
            )

            for payment_result in payment_result.get('payments', []):
                if 'error' in payment_result:
                    return False, payment_result

            # put txn on hold if payment is_deposit so no one can purchase this pet again
            hold_data = {"txn_reason": "On Hold"}
            client.update_txn(txn_id, hold_data)

            send_receipt = client.send_receipt(txn_id, txn_email)
            log_api(
                url=f"/api/v1/send_receipt/{txn_id}",
                req_params=txn_email,
                response=send_receipt,
            )

            return True, payment_result

        except Exception as e:
            log_error("Error: Accepting Payment", traceback.format_exc())
            return False, {}

    def post(self, request, *args, **kwargs):
        try:
            req_body = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Something went wrong, please contact admin.'}, status=400)
        
        payment_form = PetPaymentForm(req_body)
        if not payment_form.is_valid():
            return JsonResponse({'error': payment_form.errors.as_ul()}, status=400)

        client = PWAPI()
        txn_data = client.get_txn(req_body['txn_id'])
        if 'txn_id' not in txn_data:
            return JsonResponse({'error': 'Order was not created successfully, please contact admin.'}, status=400)

        is_success, api_result = self.send_payment(client, req_body, txn_data)
        if is_success:
            return JsonResponse({'invoice_id': txn_data['invoice_id']}, status=200)
        else:
            return JsonResponse({
                'error': api_result.get('error', 'Something went wrong, please contact admin.')
            }, status=400)

