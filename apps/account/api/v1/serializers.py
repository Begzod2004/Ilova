from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_bytes, smart_str, force_str, DjangoUnicodeDecodeError
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from apps.account.models import Account, ForCheckModel



class EnterPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForCheckModel
        fields = ('phone',)


class CodeVerificationSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=5)

    def validate(self, attrs):
        code = attrs.get('code')
        if not code.isdigit():
            raise serializers.ValidationError("Code raqamlardan iborat bo`lishi kerak!")

        phone = attrs.get('phone')
        # user = authenticate(phone=phone)
        user = Account.objects.get(phone = phone)
        if not user:
            raise AuthenticationFailed({
                'message': 'Email or password is not correct'
            })
        if user.activ_code is None and (str(code) != user.activ_code):
            raise serializers.ValidationError({'success':False, 'Note':'Invalid code or code expired'})

        data = {
            'phone': user.phone,
            'tokens':user.tokens
        }
        user.activ_code = None
        user.save()
        return data

    class Meta:
        model = ForCheckModel
        fields = ('code', 'phone',)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100)

    class Meta:
        model = ForCheckModel
        fields = ('phone', 'password')

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        user = authenticate(phone=phone, password=password)
        if not user:
            raise AuthenticationFailed({
                'message': 'Phone or password is not correct'
            })

        data = {
            'phone': user.phone,
            'tokens': user.tokens
        }
        return data



# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(min_length=6, max_length=68, write_only=True)
#     password2 = serializers.CharField(min_length=6, max_length=68, write_only=True)
#
#     class Meta:
#         model = Account
#         fields = ('full_name', 'email', 'password', 'password2')
#
#     def validate(self, attrs):
#         password = attrs.get('password')
#         password2 = attrs.get('password2')
#
#         if password != password2:
#             raise serializers.ValidationError({'success': False, 'message': 'Password did not match, please try again'})
#         return attrs
#
#     def create(self, validated_data):
#         del validated_data['password2']
#         return Account.objects.create_user(**validated_data)
#
#

#
#
# class EmailVerificationSerializer(serializers.ModelSerializer):
#     tokens = serializers.CharField(max_length=555)
#
#     class Meta:
#         model = Account
#         fields = ('tokens',)
#
#
# class ResetPasswordSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField()
#
#     class Meta:
#         model = Account
#         fields = ('email',)
#
#
# class AccountUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Account
#         fields = ('id', 'full_name', 'image_url', 'email', 'phone',)
#
#
# class AccountOwnImageUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Account
#         fields = ('image',)
#
#
# class SetNewPasswordSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(min_length=6, max_length=64, write_only=True)
#     password2 = serializers.CharField(min_length=6, max_length=64, write_only=True)
#     uidb64 = serializers.CharField(max_length=68, required=True)
#     token = serializers.CharField(max_length=555, required=True)
#
#     class Meta:
#         model = Account
#         fields = ('password', 'password2', 'uidb64', 'token')
#
#     def validate(self, attrs):
#         password = attrs.get('password')
#         password2 = attrs.get('password2')
#         uidb64 = attrs.get('uidb64')
#         token = attrs.get('token')
#         _id = force_str(urlsafe_base64_decode(uidb64))
#         user = Account.objects.filter(id=_id).first()
#         current_password = user.password
#         if not PasswordResetTokenGenerator().check_token(user, token):
#             raise AuthenticationFailed({'success': False, 'message': 'The token is not valid'})
#         if password != password2:
#             raise serializers.ValidationError({
#                 'success': False, 'message': 'Password did not match, please try again'
#             })
#
#         if check_password(password, current_password):
#             raise serializers.ValidationError(
#                 {'success': False, 'message': 'New password should not similar to current password'})
#
#         user.set_password(password)
#         user.save()
#         return attrs
#
#
# class ChangeNewPasswordSerializer(serializers.ModelSerializer):
#     old_password = serializers.CharField(min_length=6, max_length=64, write_only=True)
#     password = serializers.CharField(min_length=6, max_length=64, write_only=True)
#     password2 = serializers.CharField(min_length=6, max_length=64, write_only=True)
#
#     class Meta:
#         model = Account
#         fields = ('old_password', 'password', 'password2')
#
#     def validate(self, attrs):
#         old_password = attrs.get('old_password')
#         password = attrs.get('password')
#         password2 = attrs.get('password2')
#         request = self.context.get('request')
#         user = request.user
#         if not user.check_password(old_password):
#             print(55555555)
#             raise serializers.ValidationError(
#                 {'success': False, 'message': 'Old password did not match, please try again new'})
#
#         if password != password2:
#             print(321)
#             raise serializers.ValidationError(
#                 {'success': False, 'message': 'Password did not match, please try again new'})
#
#         user.set_password(password)
#         user.save()
#         return attrs
