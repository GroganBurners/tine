from email.mime.application import MIMEApplication
from io import BytesIO

from django.core.mail import EmailMultiAlternatives
from django.template import Context, TemplateDoesNotExist
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags

from gbs.conf import settings as app_settings
from gbs.export.pdf import export_invoice


def send_invoice(invoice):
    pdf = export_invoice(invoice)
    attachment = MIMEApplication(pdf)
    attachment.add_header(
        "Content-Disposition", "attachment", filename=invoice.file_name()
    )

    subject = f"Your Grogan Burner Services Invoice {invoice.invoice_id} is ready"
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
        from_email="mick@grogan.ie",
        to=["neil@grogan.ie"],
    )
    email.attach_alternative(html_body, "text/html")
    email.attach(attachment)
    result = email.send(fail_silently=False)
    return result
