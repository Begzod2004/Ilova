import jwt
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db.models import Q
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from drf_yasg import openapi
from apps.account.api.v1.permissions import IsOwnUserOrReadOnly, IsSimpleUser
# from apps.account.api.v1.permissions import IsOwnUserOrReadOnly
from rest_framework import generics, status, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.account.api.v1.libs.sms import sms
from apps.account.api.v1.serializers import EnterPhoneNumberSerializer, CodeVerificationSerializer, LoginSerializer
from apps.account.api.v1.utils import Util, generate_code
from apps.account.models import Account



class EnterPhoneNumberView(generics.GenericAPIView):
    serializer_class = EnterPhoneNumberSerializer
    permission_classes = (AllowAny,)


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        user, created = Account.objects.get_or_create(phone=user_data.get('phone'))
        code: str = generate_code()
        response = sms._send_verify_message(user.phone, code)
        if response >= 400:
            return Response({'success': False, 'message': 'Some error with sms server'}, status=status.HTTP_400_BAD_REQUEST)
        user.activ_code = code
        user.save()
        return Response({'success': True, 'message': 'Activation code was sent your phone','phone':user.phone},
                        status=status.HTTP_201_CREATED)


class CodeVerificationLoginAPIView(APIView):
    serializer_class = CodeVerificationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'data': serializer.validated_data}, status=status.HTTP_200_OK)



class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'data': serializer.validated_data}, status=status.HTTP_200_OK)



#
#
# class AccountRegisterView(generics.GenericAPIView):
#     # http://127.0.0.1:8000/api/account/v1/register/
#     serializer_class = RegisterSerializer
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         user_data = serializer.data
#         user = Account.objects.get(phone=user_data['phone'])
#
#         code: str = generate_code()
#         sms._send_verify_message(user.phone, code)
#
#         return Response({'success': True, 'message': 'Activate url was sent your email'},
#                         status=status.HTTP_201_CREATED)
#
#
# class EmailVerificationAPIView(APIView):
#     # http://127.0.0.1:8000/account/verify-email/?token={token}/
#     serializer_class = EmailVerificationSerializer
#     permission_classes = (AllowAny,)
#     token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Verify email',
#                                            type=openapi.TYPE_STRING)
#
#     def get(self, request):
#         token = request.GET.get('token')
#         try:
#             payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
#             user_id = Account.objects.get(id=payload['user_id'])
#             if not user_id.is_active:
#                 user_id.is_active = True
#                 user_id.save()
#             return Response({'success': True, 'message': 'Email successfully activated'},
#                             status=status.HTTP_201_CREATED)
#         except jwt.ExpiredSignatureError as e:
#             return Response({'success': False, 'message': f'Verification expired | {e.args}'},
#                             status=status.HTTP_400_BAD_REQUEST)
#         except jwt.exceptions.DecodeError as e:
#             return Response({'success': False, 'message': f'Invalid token | {e.args}'},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#
# class LoginView(generics.GenericAPIView):
#     # http://127.0.0.1:8000/api/account/v1/login/
#     serializer_class = LoginSerializer
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
#
#

# class AccountRetrieveUpdateView(generics.RetrieveUpdateAPIView):
#     # http://127.0.0.1:8000/api/account/v1/retrieve-update/<id>/
#     serializer_class = AccountUpdateSerializer
#     queryset = Account.objects.all()
#     permission_classes = (IsOwnUserOrReadOnly, IsAuthenticated)
#
#     def get(self, request, *args, **kwargs):
#         query = self.get_object()
#         if query:
#             serializer = self.get_serializer(query)
#             return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
#         else:
#             return Response({'success': False, 'message': 'query did not exist'}, status=status.HTTP_404_NOT_FOUND)
#
#     def put(self, request, *args, **kwargs):
#         obj = self.get_object()
#         serializer = self.get_serializer(obj, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'success': True, 'data': serializer.data}, status=status.HTTP_202_ACCEPTED)
#         return Response({'success': False, 'message': 'credentials is invalid'}, status=status.HTTP_404_NOT_FOUND)
#
#
# class SetPasswordConfirmAPIView(views.APIView):
#     # http://127.0.0.1:8000/account/set-password-confirm/<uidb64>/<token>/
#     permission_classes = (AllowAny,)
#
#     def get(self, request, uidb64, token):
#         try:
#             _id = smart_str(urlsafe_base64_decode(uidb64))
#             user = Account.objects.filter(id=_id).first()
#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 return Response({'success': False, 'message': 'Token is not valid, please try again'},
#                                 status=status.HTTP_406_NOT_ACCEPTABLE)
#         except DjangoUnicodeDecodeError as e:
#             return Response({'success': False, 'message': f'DecodeError: {e.args}'},
#                             status=status.HTTP_401_UNAUTHORIZED)
#         return Response({'success': True, 'message': 'Successfully checked', 'uidb64': uidb64, 'token': token},
#                         status=status.HTTP_200_OK)
#
#
# class SetNewPasswordView(generics.UpdateAPIView):
#     # http://127.0.0.1:8000/api/account/v1/set-password/
#     serializer_class = SetNewPasswordSerializer
#     permission_classes = (IsOwnUserOrReadOnly, IsAuthenticated)
#
#     def patch(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             return Response({'success': True, 'message': 'Successfully set new password'}, status=status.HTTP_200_OK)
#         return Response({'success': False, 'message': 'Credentials is invalid'}, status=status.HTTP_406_NOT_ACCEPTABLE)
#
#
# class ResetPasswordAPIView(generics.GenericAPIView):
#     # http://127.0.0.1:8000/account/v1/reset-password/
#     serializer_class = ResetPasswordSerializer
#
#     def post(self, request):
#         user = Account.objects.filter(email=request.data['email']).first()
#
#         if user:
#             uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
#             token = PasswordResetTokenGenerator().make_token(user)
#             current_site = 'localhost:8000/'
#             abs_url = f'http://{current_site}account/v1/set-password-confirm/{uidb64}/{token}/'
#             email_body = f'Hello, \n User link below to activate your email \n {abs_url}'
#             data = {
#                 'to_email': user.email,
#                 'email_subject': 'Reset password',
#                 'email_body': email_body
#             }
#             Util.send_email(data)
#
#             return Response({'success': True, 'message': 'Link sent to email'}, status=status.HTTP_200_OK)
#         return Response({'success': False, 'message': 'Email did not match'}, status=status.HTTP_400_BAD_REQUEST)
#
#
# class AccountView(generics.RetrieveAPIView):
#     # http://127.0.0.1:8000/api/account/v1/get-account/
#     permission_classes = (IsOwnUserOrReadOnly, IsAuthenticated,)
#     serializer_class = AccountUpdateSerializer
#
#     def queryset(self, request, *args, **kwargs):
#         user = request.user
#         query = Account.objects.get(id=user.id)
#         serializer = self.get_serializer(query)
#         return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
#
#
# class AccountOwnImageUpdateView(generics.RetrieveUpdateAPIView):
#     # http://127.0.0.1:8000/api/account/v1/image-retrieve-update/<id>/
#     serializer_class = AccountOwnImageUpdateSerializer
#     queryset = Account.objects.all()
#     permission_classes = (IsOwnUserOrReadOnly, IsAuthenticated)
#
#     def get(self, request, *args, **kwargs):
#         query = self.get_object()
#         if query:
#             serializer = self.get_serializer(query)
#             return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
#         return Response({'success': False, 'message': 'query does not match'}, status=status.HTTP_404_NOT_FOUND)
#
#     def put(self, request, *args, **kwargs):
#         obj = self.get_object()
#         serializer = self.get_serializer(obj, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
#         return Response({'success': False, 'message': 'Credentials is invalid'}, status=status.HTTP_400_BAD_REQUEST)
#
#
# class AccountListView(generics.ListAPIView):
#     # http://127.0.0.1:8000/api/account/v1/list/
#     serializer_class = AccountUpdateSerializer
#     queryset = Account.objects.all()
#     permission_classes = (IsAuthenticated,)
#
#     def get_queryset(self):
#         qs = super().get_queryset()
#         q = self.request.GET.get('q')
#
#         q_condition = Q()
#         if q:
#             q_condition = Q(full_name__icontains=q) | Q(phone__icontains=q) | Q(email__icontains=q)
#
#         queryset = qs.filter(q_condition)
#
#         return queryset
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         if queryset:
#             serializer = self.get_serializer(queryset, many=True)
#             count = queryset.count()
#             return Response({'success': True, 'count': count, 'data': serializer.data}, status=status.HTTP_200_OK)
#         return Response({'success': False, 'data': 'queryset does not match'}, status=status.HTTP_404_NOT_FOUND)
#
#
# class ChangePasswordCompletedView(generics.UpdateAPIView):
#     # http://127.0.0.1:8000/account/change-password/
#     queryset = Account.objects.all()
#     serializer_class = ChangeNewPasswordSerializer
#     permission_classes = (IsAuthenticated,)
#     lookup_field = 'pk'
#
#     def patch(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         return Response({'success': True, 'message': 'Successfully set new password'}, status=status.HTTP_200_OK)
