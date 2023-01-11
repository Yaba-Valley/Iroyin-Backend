from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string


def send_email(subject, body, receipient_email, receipient_fullName):

    import environ
    from mailjet_rest import Client

    env = environ.Env()

    environ.Env.read_env()

    mailjet = Client(auth=(env('MAILJET_API_KEY'),
                     env('MAILJET_SECRET_KEY')), version = 'v3.1')

    data = {
        "Messages": [
            {
                "From": {
                    "Email": "jeremiah@fusionintel.io",
                    "Name": "The ReadNews Team"
                },
                "To": [
                    {
                        "Email": receipient_email,
                        "Name": receipient_fullName
                    }
                ],
                "Subject": subject,
                "TextPart": subject,
                "HTMLPart": body,
            }
        ]
    }


    result = mailjet.send.create(data=data)
    print(receipient_fullName)
    print(f"{subject} return {str(result.status_code)}")
    return result


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.pk) + text_type(timestamp) + text_type(user.is_active))

    def send_account_activation_mail(self, request, user):

        site = get_current_site(request).name
        token = TokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        template_string = render_to_string('activateAccount.html', {
                                           'user': user, 'uid': uid, 'token': token, 'site': site})

        res = send_email('Confirm your email', template_string,
                   user.email, f"{user.first_name} {user.last_name}")
    
        print(res)
        
        return res.status_code;
    
    
    # test silly push