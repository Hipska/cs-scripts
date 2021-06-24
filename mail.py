import sendgrid
from config import api_key
from sendgrid.helpers.mail import Mail

# Send an email following the conditions. Make sure you loaded your sendgrid environment before use.
# eg. sendMail('dylan@webfaster.com', 'dylan@webfaster.com', 'Test API', 'Bonjour<br/>How are you ?')
def mail(mail_to, mail_from, mail_subject, mail_message=''):
    email = Mail(
        from_email=mail_from,
        to_emails=mail_to,
        subject=mail_subject,
        html_content=mail_message,
    )
    
    try:
        #print('api_key:', api_key)
        api = sendgrid.SendGridAPIClient(api_key=api_key)
        response = api.send(email)
        print('Response Status', response.status_code)
        print('Response Body', response.body)
        #print('Response Headers', response.headers)
    except Exception as e:
        print(e)
        print(response.body)