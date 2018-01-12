from django.template.loader import render_to_string, get_template
from django.template import TemplateDoesNotExist, Context
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from email.mime.application import MIMEApplication
from gbs.conf import settings as app_settings
from io import BytesIO
from gbs.pdf import export_invoice

def send_invoice(invoice):
    pdf = BytesIO()
    export_invoice(pdf, invoice)
    pdf.seek(0)
    attachment = MIMEApplication(pdf.read())
    attachment.add_header("Content-Disposition", "attachment",
                                          filename=invoice.file_name())
    pdf.close()

    subject = f'Your Grogan Burner Services Invoice {invoice.invoice_id} is ready'
    email_kwargs = {
        "invoice": invoice,
        "SITE_NAME": "Grogan Burner Services",
        "SUPPORT_EMAIL": app_settings.EMAIL,
    }

    # try:
    #     template = get_template("email/invoice.html")
    #     body = template.render(Context(email_kwargs))
    # except TemplateDoesNotExist:
    body = render_to_string("email/invoice.txt", email_kwargs)

    email = EmailMultiAlternatives(subject=subject, body=strip_tags(body), from_email='mick@grogan.ie', to=['neil@grogan.ie'])
    # email.attach_alternative(body, "text/html")
    email.attach(attachment)
    email.send(fail_silently=False)

