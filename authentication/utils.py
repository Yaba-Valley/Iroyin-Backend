from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string


def send_email(subject, body, receipients):
    """ 
    type Receipients  = Array<{email: String, fullName?: string}>
    """

    import environ
    from mailjet_rest import Client

    env = environ.Env()

    environ.Env.read_env()

    mailjet = Client(auth=(env('MAILJET_API_KEY'),
                     env('MAILJET_SECRET_KEY')), version='v3.1')

    data = {
        "Messages": [
            {
                "From": {
                    "Email": "jeremiah@fusionintel.io",
                    "Name": "The ReadNews Team"
                },
                "To": [
                    {
                        "Email": receipient['email'],
                        "Name": receipient["fullName"]
                    } for receipient in receipients
                ],
                "Subject": subject,
                "TextPart": subject,
                "HTMLPart": body,
            }
        ]
    }

    result = mailjet.send.create(data=data)
    print(f"{subject} return {str(result.status_code)}")
    return result


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.pk) + text_type(timestamp) + text_type(user.is_active) + text_type(user.password))

    def send_account_activation_mail(self, request, user):

        site = get_current_site(request).name
        token = self.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        template_string = render_to_string('activateAccount.html', {
                                           'user': user, 'uid': uid, 'token': token, 'site': site})

        res = send_email('Confirm your email', template_string, [
                         {'email': user.email, 'fullName': f"{user.first_name} {user.last_name}"}])

        print(res)

        return res.status_code

    def send_password_reset_mail(self, request, user):

        site = get_current_site(request).name
        token = self.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        template_string = render_to_string(
            'requestpasswordreset.html', {'user': user, 'uid': uid, 'token': token, 'site': site})
        
        res = send_email('Reset your password', template_string, [
            {'email': user.email, 'fullName': f"{user.first_name} {user.last_name}"}
        ])
        
        print(res)
        
        return res.status_code
