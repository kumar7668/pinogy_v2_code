from django.utils.safestring import mark_safe

from pos_api.utils import *  # noqa

ERROR_MESSAGE_MAPPING = {
    "not_found": "There is some problem on our side. Please check with your account manager.",
    "bad_request": "Request structure is corrupted",
    "validation_error": "Some fields data is not correct.",
    "unexpected_error": "Some Unexcepted error occurred. Please contact your account manager",
}


class ApiException(Exception):
    def __init__(self, status_code, error_data):
        self.status_code = status_code
        self.error_data = error_data
        error_dict = error_data.get("error", {})

        self.error_message = ERROR_MESSAGE_MAPPING.get(
            error_dict.get("type"),
            error_dict.get("message") or ERROR_MESSAGE_MAPPING.get("unexpected_error"),
        )
        print(error_dict)
        if error_dict and error_dict.get("details"):
            self.error_message = self.error_message.format(
                **error_dict.get("details", {})
            )
        if error_dict.get("type") == "validation_error":
            self.error_message += dict_to_ul(error_dict.get("details"))  # noqa
            self.error_message = mark_safe(self.error_message)

    def __str__(self):
        return "API error {0}: {1}".format(self.status_code, self.error_data)


class ApiException401(Exception):
    def __init__(self, status_code, error_data):
        self.status_code = status_code
        self.error_data = error_data

    def __str__(self):
        return "API error {0}: {1}".format(self.status_code, self.error_data)
