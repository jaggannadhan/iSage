
import traceback, os
from mailjet_rest import Client as MailJet

MJ_API_KEY = os.getenv("MJ_APIKEY_PUBLIC")
MJ_SECRET_KEY = os.getenv("MJ_APIKEY_PRIVATE")
MJ_CLIENT = MailJet(auth=(MJ_API_KEY, MJ_SECRET_KEY), version='v3.1')


def send_email(from_mail, subject, message):
    try:
        if not (from_mail or message):
            raise IncompleteException()
        
        toName = "Jagan"
        toEmail = "jaggannadhan1994@gmail.com"
        
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "raconteur.ing4u@gmail.com",
                        "Name": "Katturai"
                    },
                    "To": [
                        {
                            "Email": toEmail,
                            "Name": toName
                        }
                    ],
                    "Subject": subject,
                    # "TextPart": message,
                    "HTMLPart": f"<h3>Dear {toName},</h3><br/> \
                        <p>You have a message from <b>{from_mail}.</b></p><br/> \
                        <b>Message: </b><br/> \
                        <p>{message}</p> \
                        <b>Regards,</b><br/><b>Team Katturai</b><br/>" 
                    
                }
            ]
        }

        result = MJ_CLIENT.send.create(data=data)
        print(result.status_code)
        print(result.json())

        return True, "Email Sent Successfully"
    
    except IncompleteException:
        return False, "Email/Message cannot be empty"
    except Exception:
        print(traceback.format_exc())
        return False, f"Unable to send email!"
    
class IncompleteException(Exception):
    def __init__(self, message=""):
        self.message = message

    