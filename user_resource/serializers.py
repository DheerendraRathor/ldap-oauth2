from rest_framework import serializers
from .models import Program, ContactNumber, SecondaryEmail, InstituteAddress
from django.contrib.auth.models import User
import copy
from .oauth import default_fields, user_fields


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program


class SecondaryEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondaryEmail


class ContactNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactNumber


class InstituteAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteAddress


class UserSerializer(serializers.ModelSerializer):
    program = ProgramSerializer()
    secondary_emails = SecondaryEmailSerializer(many=True)
    contacts = ContactNumberSerializer(many=True)
    insti_address = InstituteAddressSerializer()

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        fields = self.context.get('fields')
        if not isinstance(fields, list) and not isinstance(fields, set):
            fields = []
        fields.extend(default_fields)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            fields_to_remove = existing - allowed
            for field in fields_to_remove:
                self.fields.pop(field)

    class Meta:
        model = User
        fields = copy.deepcopy(default_fields).extend(user_fields)
