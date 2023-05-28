import uuid

from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.response import Response

from users.models import Profiles
from users.utils import generate_unique_username, is_valid_email

User = get_user_model()


class UserModelSerializer(serializers.ModelSerializer):
    """
    Serializer class for creating django auth User model
    """
    email = serializers.EmailField(required=True)
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name",
                    "password", "confirm_password")
        extra_kwags = {
            "password": {"write_only": True, "style": {"input_type": "password"}},
            "email": {"required": True, "allow_blank": False, },
        }

    def _get_request(self):
        request = self.context.get("request")
        if (
            request
            and not isinstance(request, HttpRequest)
            and hasattr(request, "_request")
        ):
            request = request._request
        return request

    # def validate_email(self, email):
    #     email = is_valid_email(email)

    #     if email:
    #         if User.objects.filter(email=email).exists():
    #             raise serializers.ValidationError(
    #                 _("This email has already been used. Try another one or recover your password.")
    #             )
    #     else:
    #         raise serializers.ValidationError(
    #             _("This is not a valid email address.")
    #         )

    #     return email

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')

        confirm_password = self.data.get('confirm_password')


        username = generate_unique_username(first_name, last_name)
        new_user = User.objects.filter(username__icontains=username)

        if new_user.exists():
            username = f"{username}{new_user.count() + 1}-{str(uuid.uuid4())}"

        if password == confirm_password:
            user = User(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            user.set_password(password)
            user.save()

            user_profile = Profiles(
                user=user
            )
            user_profile.save()

            return {
                "id": user.id,
                "email": user.email
            }

        else:
            raise serializers.ValidationError(
                _("This email has already been used. Try another one or recover your password.")
            )


class AuthCustomTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                validate_email(email)
                user_request = get_object_or_404(User, email=email)
                email = user_request.username
            except ValidationError as e:
                return Response({
                    "status": 400,
                    "error": True,
                    "message": str(e),
                })

            user = authenticate(username=email, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)
            else:
                msg = _('Unable to login with the provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include email and a password.')
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs