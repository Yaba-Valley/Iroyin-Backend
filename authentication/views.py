import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.forms import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse, Http404, HttpResponse
from .utils import TokenGenerator, send_email
from django.template.loader import render_to_string
from django.utils.encoding import force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from .models import User
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, TokenError


@csrf_exempt
def login(request):
    if request.method == "POST":
        request_body = json.loads(request.body.decode('utf-8'))
        email = request_body['email'].strip()
        password = request_body['password'].strip()

        if email and password:
            try:
                user = get_object_or_404(User, email=email)

                if user.check_password(password):

                    # if the token was generated successfully
                    if user.is_active:
                        token = AccessToken.for_user(user)

                        return JsonResponse(
                            {
                                'message': 'You have successfully logged in',
                                'success': True,
                                'data': {
                                    'token': str(token),
                                    'email': user.email,
                                    'first_name': user.first_name,
                                    'last_name': user.last_name,
                                    'last_login': user.last_login,
                                    'hasSetInterests': user.interests.count() > 0
                                }
                            }, status=200
                        )
                    else:

                        res = TokenGenerator().send_account_activation_mail(request, user)

                        return JsonResponse(
                            {
                                'success': False,
                                'message': 'Your account has not been activated',
                                'errors': []
                            }, status=401
                        )

                else:
                    return JsonResponse(
                        {
                            'message': 'Incorrect Login Credentials',
                            'success': False,
                            'errors': [],
                        }, status=401
                    )
            except Http404:
                return JsonResponse(
                    {
                        'message': 'Incorrect Login Credentials',
                        'success': False,
                        'errors': []
                    },  status=404
                )
        else:
            return JsonResponse({'success': False, 'errors': [],  'message': "Please input required fields"}, status=400)
    else:
        return JsonResponse({'success': False, 'errors': [], 'message': "Request Not Allowed"}, status=405)


@csrf_exempt
def register(request):

    if request.method == "POST":

        request_body = json.loads(request.body.decode('utf-8'))
        email = request_body['email'].strip()
        full_name = request_body['fullName'].strip().split(' ')
        password = request_body['password'].strip()

        if len(full_name) == 1:
            if full_name[0] == '':
                full_name = False
            else:
                first_name = full_name[0]
                last_name = ''
        else:
            first_name = full_name[0]
            last_name = full_name[len(full_name) - 1]

            full_name = True

        if full_name and email and password:
            try:

                # try to get the user to know if a user already exists with the email address
                user = User.objects.filter(email=email.lower())

                if len(user) == 1:
                    raise IntegrityError()

                # this code only runs if there no user with the same email address

                test_user = User(
                    email=email.lower(), first_name=first_name, last_name=last_name)

                validate_password(password=password, user=test_user)

                test_user.set_password(password)

                test_user.save()

                # SENDING ACTIVATION MAIL
                template_string = render_to_string('welcomeEmail.html', {
                                                   'registered_user': test_user})

                welcome_mail_res = send_email('Heeyyyy, We\'re sooo happy to have you here😊🎉🎉',
                                              template_string, email, f"{first_name} {last_name}")

                activation_mail_res = TokenGenerator().send_account_activation_mail(request, test_user)

                print(welcome_mail_res, activation_mail_res)

                return JsonResponse({
                    'success': True,
                    'message': 'Account has been created successfully. Check your mail to activate your account',
                    'data': {
                        'email': email,
                    }
                }, status=200)

            except ValidationError as errors:
                validation_errors = []

                [validation_errors.append(str(error)) for error in errors]

                return JsonResponse({'success': False, 'message': 'Please review your password', 'errors': validation_errors}, status=400)
            except IntegrityError:
                return JsonResponse({'success': False, 'message': 'Email Address is already in use', 'errors': ['Email Already in Use']}, status=400)

        else:
            errors = []

            if not email:
                errors.append('Email cannot be empty')

            if not password:
                errors.append('Password cannot be empty')

            if not full_name:
                errors.append('Your fullname cannot be empty')

            return JsonResponse({'success': False, 'message': 'Please fill the required fields', 'errors': errors}, status=400)

    else:
        return JsonResponse({'success': False, 'message': "Request Not Allowed"}, status=405)


class Activate_Account(APIView):

    def get(self, request,  uid, token):

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user_id = int(user_id)

            user = User.objects.get(id=user_id)

            is_valid_token = TokenGenerator().check_token(user=user, token=token)

            if is_valid_token:
                print('Token is Valid')
                user.is_active = True
                user.save()
            else:
                return HttpResponse('Invalid token')

            return HttpResponse('hi ' + user.first_name + '. You can now log in normally')

        except User.DoesNotExist:
            return HttpResponse("Guy how far, this person no dey our databse")
        except DjangoUnicodeDecodeError:
            return HttpResponse('I catch you, couldn\'t decode this unicode')


def verify_token(request):
    token = request.GET.get('token')

    try:
        if token:
            access_token = AccessToken(token)
            print(token)
            user = get_object_or_404(
                User, id=access_token.payload['user_id'])

            print(user)

            return JsonResponse(
                {
                    'message': 'Token Verified',
                    'success': True,
                    'data': {
                        'token': str(token),
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'last_login': user.last_login,
                        'hasSetInterests': user.interests.count() > 0
                    }
                }, status=200
            )
        else:
            return JsonResponse({'message': 'Authorization header not set properly', 'success': False})
    except Http404:
        return JsonResponse({'message': 'Could not find user associated with token', 'success': False}, status=404)
    except TokenError:
        return JsonResponse({'message': 'Invalid Token - Expired or Invalid', 'success': False}, status=401)
    except Exception as e:
        return JsonResponse({'message': 'Authorization header not set properly', 'success': False}, status=400)
