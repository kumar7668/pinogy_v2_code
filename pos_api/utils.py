import logging
import string

from pos_api.models.pet import ApiPetPhoto

logger = logging.getLogger(__name__)


def pretty_name(name):
    if not name:
        return ""
    return string.capwords(name.replace("_", " "))


def dict_to_ul(data):
    if isinstance(data, dict):
        return "".join(
            "<div><b>{}</b></div><ul>{}</ul>".format(
                pretty_name(title),
                "".join("<li>{}</li>".format(item) for item in items),
            )
            for (title, items) in data.items()
        )

    logger.debug("Wrong argument `{}` passed to `dict_to_ul`, it isn\t a dict")
    return ""


def get_base_quippet_params(quippet_name=None):
    if quippet_name == "read__qpt__list_locations":
        return {"qp_public_call": True, "qp_loc_available_publicly": True}

    return {"qp_public_call": True}
    # return {}


def get_pet_images(client, file_ids, pet_id, is_badges=False):

    items = client.post_queries(
        **{
            "quippet_name": "read__tbl__vw_files_with_in_band_contents",
            "quippet_params": {"qp_file_id": ",".join(str(item) for item in file_ids)},
        }
    )["objects"]

    result = []
    for item in items:
        item_obj, created = ApiPetPhoto.objects.get_or_create(
            file_id=item["file_id"], pet_id=pet_id, is_badges=is_badges
        )
        if created:
            file_data = item["flin_contents"].encode("utf-8")
            item_obj.file_extension = item["file_orig_extension"]
            item_obj.alt = item["file_description"]
            item_obj.save()
            item_obj.save_file(file_data)
            result.append(item_obj)
    return result

def add_pet_image(client, file_ids, pet_id):
    # TODO: Need move pet image logic to base image logic
    default_image_url = "/static/images/dog-placeholder-img.webp"
    default_image = {
        "url": default_image_url,
        "file_image": {
            "url": default_image_url,
        },
        "placeholder": True
    }
    
    if file_ids:
        try:
            pet_img = ApiPetPhoto.objects.filter(file_id=file_ids[0], pet_id=pet_id).first()
            if pet_img:
                return pet_img
            else:
                pet_imgs = get_pet_images(client, file_ids, pet_id)
                return pet_imgs[0] if pet_imgs else ""
        except ApiPetPhoto.DoesNotExist:
            return default_image

    return default_image

def populate_pet_files(client,file_id, file_description, model_class, model_default=None, filter_extensions=None, is_badge=False):
        model_class=ApiPetPhoto
        try:
                if model_default is None:
                    model_default = {}
                model_default['order'] = 0

                items = client.post_queries(**{
                    "quippet_name": 'read__tbl__vw_files_with_in_band_contents',
                    "quippet_params": {
                        'qp_file_id': file_id
                    }
                })['objects']
                result = []
                for item in items:
                    if filter_extensions and item['file_orig_extension'].lower() not in filter_extensions:
                        continue

                # to avoid duplicate image start
                    if is_badge:
                        model_default['pet_id'] = 0
                        item_obj, created = model_class.objects.get_or_create(
                            file_id=item['file_id'], is_badges=is_badge, defaults=model_default)
                    else:
                        item_obj, created = model_class.objects.get_or_create(
                            file_id=item['file_id'], defaults=model_default)
                # end
                    if created:
                        file_data = item['flin_contents'].encode('utf-8')
                        item_obj.file_extension = item['file_orig_extension']
                        item_obj.alt = file_description
                        item_obj.file_name = item['file_orig_basename']
                        item_obj.save()
                        item_obj.save_file(file_data)
                        result.append(item_obj)
                    else:
                        result.append(item_obj)
                return result
        except Exception as e:
            print(e)
            