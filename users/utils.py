import uuid

from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

def generate_unique_username(first_name, last_name):
    unique_username = first_name + last_name + uuid.uuid4().hex[:10]

    return unique_username

def is_valid_email(email):
    email_validator = EmailValidator()

    try:
        is_valid = email_validator(email)

        if is_valid: return True
    except ValidationError:
        return False
