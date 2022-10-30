import json
import jsonschema
from jsonschema import validate
from .exceptions import ValidationError

COMPANY_POST_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 2, "maxLength": 50},
        "description": {"type": "string",  "minLength": 2, "maxLength": 100},
        "symbol": {
            "type": "string",  "minLength": 2,  "maxLength": 10,    
            "pattern": "(NYSE|AMEX|NASDAQ):([A-Z]{1,4})"
        },
    },
    "required":[
        "name",
        "description",
        "symbol",
    ],
}


COMPANY_PUT_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 2, "maxLength": 50},
        "description": {"type": "string",  "minLength": 2, "maxLength": 100},
        "symbol": {
            "type": "string",  "minLength": 2,  "maxLength": 10,    
            "pattern": "(NYSE|AMEX|NASDAQ):([A-Z]{1,4})"
        },
    },
}


def validate_json(json_data, schema):
    try:
        validate(instance=json_data, schema=schema)
        return {"error":None}
    except jsonschema.exceptions.ValidationError as err:
        return {"error":err.message}


def validate_post_company(json_data):
    return validate_json(json_data, COMPANY_POST_SCHEMA)


def validate_put_company(json_data):
    return validate_json(json_data, COMPANY_PUT_SCHEMA)
