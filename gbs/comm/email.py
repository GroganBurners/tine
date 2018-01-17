from django.template.loader import render_to_string, get_template
from django.template import TemplateDoesNotExist, Context
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from email.mime.application import MIMEApplication
from gbs.conf import settings as app_settings
from io import BytesIO
from gbs.export.pdf import export_invoice


def send_invoice(invoice):
    pdf = export_invoice(invoice)
    attachment = MIMEApplication(pdf)
    attachment.add_header("Content-Disposition", "attachment",
                          filename=invoice.file_name())

    subject = f'Your Grogan Burner Services Invoice {invoice.invoice_id} is ready'
    email_kwargs = {
        "invoice": invoice,
        "SITE_NAME": "Grogan Burner Services",
        "SUPPORT_EMAIL": app_settings.EMAIL,
    }

    template = get_template("email/html/invoice-compiled.html")
    html_body = template.render(email_kwargs)
    body = render_to_string("email/txt/invoice.txt", email_kwargs)

    email = EmailMultiAlternatives(
        subject=subject,
        body=strip_tags(body),
        from_email='mick@grogan.ie',
        to=['neil@grogan.ie'])
    email.attach_alternative(html_body, "text/html")
    email.attach(attachment)
    email.send(fail_silently=False)
