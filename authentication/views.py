import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.forms import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render
from .utils import TokenGenerator, send_email
from django.template.loader import render_to_string
from django.utils.encoding import force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from .models import User
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from rest_framework.permissions import IsAuthenticated


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

                if len(user) >= 1:
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
                                              template_string, [{'email': email, 'fullName': f"{first_name} {last_name}"}])

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

            return HttpResponse('hi ' + user.first_name + '. You can now log in on the app')

        except User.DoesNotExist:
            return HttpResponse("Guy how far, this person no dey our databse")
        except DjangoUnicodeDecodeError:
            return HttpResponse('I catch you, couldn\'t decode this unicode')


def verify_token(request):
    token = request.GET.get('token')

    try:
        if token:
            access_token = AccessToken(token)
            user = get_object_or_404(
                User, id=access_token.payload['user_id'])

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
            return JsonResponse({'message': 'Authorization header not set properly', 'success': False}, status=400)
    except Http404:
        return JsonResponse({'message': 'Could not find user associated with token', 'success': False}, status=400)
    except TokenError:
        return JsonResponse({'message': 'Invalid Token - Expired or Invalid', 'success': False}, status=400)
    except Exception as e:
        return JsonResponse({'message': 'Authorization header not set properly', 'success': False}, status=400)


class Set_Push_Notification_Token(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        push_token = request.POST.get('push_token')
        user = User.objects.get(id=request.user.id)
        user.push_notification_token = push_token
        user.save()

        return JsonResponse({'success': True, 'errors': [], 'message': 'Successfully added device token'})


class Request_Password_Reset(APIView):

    def get(self, request):
        user_email = request.GET.get('email')
        host = request.GET.get('host') or 'exp://172.20.10.2:19000/--/'
        route = request.GET.get('route') or 'Auth/ResetPassword'

        try:
            user = User.objects.get(email=user_email)
            TokenGenerator().send_password_reset_mail(request, user, host, route)

        except Exception:
            return JsonResponse({'message': 'Failed to reset password. User does not exist'}, status=404)

        return JsonResponse({'message': 'request successful'}, status=200)


class Reset_Password(APIView):

    # this endpoint just renders the template that contains javascript to open the reset password screen on the app
    # with the token and the id... which ends up calling the post endpoint with the new password...
    def get(self, request, uid, token):
        user_id = force_str(urlsafe_base64_decode(uid))
        user_id = int(user_id)
        host = request.GET.get('host')
        route = request.GET.get('route')

        try:
            user = User.objects.get(id=user_id)

            if TokenGenerator().check_token(token=token, user=user):
                redirect_url = f'{host}{route}?passwordResetToken={token}&userId={user_id}'
                return render(request, 'redirect_to_app.html', {'redirect_url': redirect_url})
            else:
                return HttpResponse('400 - Invalid Token')

        except User.DoesNotExist:
            return HttpResponse('404 - Not Found')

    # the post request is to handle the actual password change
    def post(self, request, uid, token):
        request_body = json.loads(request.body.decode('utf-8'))
        # new password string
        new_password = request_body['new_password'].strip()
        # confirm password string
        confirm_new_password = request_body['confirm_new_password'].strip()
        user_id = request_body['user_id']  # expected to be a number
        # password reset token
        reset_token = request_body['reset_token'].strip()

        user = User.objects.get(id=user_id)

        # token is valid
        if not TokenGenerator().check_token(user=user, token=reset_token):
            return JsonResponse({'message': 'Invalid token. Request password reset again'}, status=400)

        # passwords match
        if new_password != confirm_new_password:
            return JsonResponse({'message': 'passwords do not match. we\'re done here'}, status=400)

        # password is valid
        try:
            validate_password(new_password, user)
        except ValidationError as errors:
            validation_errors = []
            [validation_errors.append(str(error)) for error in errors]
            return JsonResponse({'success': False, 'message': 'Please review your password', 'errors': validation_errors}, status=400)

        user.set_password(new_password)
        user.save()

        return JsonResponse({'message': 'Password successfully reset'}, status=200)


class Logout(APIView):

    authentication_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        user.push_notification_token = ''
        user.save()

        return JsonResponse({'success': True, 'errors': [], 'message': 'Logged out successfully'})
