from django.core.mail import EmailMessage
from random import choice


def generate_code() -> str:
    """Generates random verify code"""
    password: str = ''
    numbers: tuple = tuple('1234567890')

    for _ in range(5):
        password += choice(choice(numbers))

    return password

class Util:

    @staticmethod
    def send_email(data: dict):
        email = EmailMessage(to=[data['to_email']], subject=data['email_subject'], body=data['email_body'])
        email.send()