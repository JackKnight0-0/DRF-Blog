from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import ValidationError, UniqueValidator

from django.contrib.auth.password_validation import validate_password


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False,
                                   validators=[UniqueValidator(queryset=get_user_model().objects.all())])
    password1 = serializers.CharField(write_only=True, validators=[validate_password], required=True)
    password2 = serializers.CharField(write_only=True, validators=[validate_password], required=True)

    class Meta:
        model = get_user_model()
        fields = (
            'username', 'email', 'password1', 'password2'
        )

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise ValidationError({'password2': 'The password not matching'})
        return attrs

    def create(self, validate_data):
        vd = validate_data
        if 'email' in vd:
            user = get_user_model().objects.create(
                username=vd.get('username'),
                email=vd.get('email')
            )
        else:
            user = get_user_model().objects.create(
                username=vd.get('username'),
            )
        user.set_password(validate_data['password1'])
        user.save()
        return user
