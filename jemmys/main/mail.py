from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_an_email(subject, recipient, context_data, html_file):
    """Sends an email to the recipient with loaded context."""
    subject = subject
    html_message = render_to_string(html_file, context=context_data)
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, plain_message, from_email, [recipient], html_message=html_message)