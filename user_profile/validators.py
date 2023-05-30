import jsonschema

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator

PASSIONS_JSON_FIELD_SCHEMA = {
    "type": "array",
    "items": {
        "type": "string",
    },
    "minItems": 0,
    "maxItems": settings.MAX_PASSION_NUM,
    "uniqueItems": True,
}


class PassionsValidator(BaseValidator):
    def compare(self, value, schema):
        try:
            jsonschema.validate(value, schema)
        except jsonschema.exceptions.ValidationError:
            raise ValidationError("JSON schema check is failed.")
