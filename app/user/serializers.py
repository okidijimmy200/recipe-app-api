from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    '''serializer for the user object'''
    class Meta:
        model = get_user_model()
        # fields to include in the serializer
        fields = ('email', 'password', 'name')
        # extra settings in the model serializers and password is 5 characters
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validted_data):
        '''create a new user with encrypted password and return it'''
        return get_user_model().objects.create_user(**validted_data)

    # update function(using the setPassword function)
    def update(self, instance, validated_data):
        '''update a user, setting the password correctly and return it'''
        password = validated_data.pop('password', None)
        # run update on password
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

class AuthTokenSerializer(serializers.Serializer):
    '''serializer for the user authentication object'''
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    # validation command
    def validate(self, attrs):
        '''validate and authenticate user'''
        email = attrs.get('email')
        password = attrs.get('password')

        # authenticate requests
        user =authenticate(
            # request to authenticate
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        # set user in attrs
        attrs['user'] = user
        return attrs
