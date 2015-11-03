import copy

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import ContactNumber, InstituteAddress, Program, SecondaryEmail
from .oauth import DEFAULT_FIELDS, USER_FIELDS


class ProgramSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    degree_name = serializers.SerializerMethodField()

    def get_department_name(self, obj):
        return obj.get_department_display()

    def get_degree_name(self, obj):
        return obj.get_degree_display()

    class Meta:
        model = Program
        exclude = ['user']


class SecondaryEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondaryEmail
        exclude = ['user']


class ContactNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactNumber
        exclude = ['user']


class InstituteAddressSerializer(serializers.ModelSerializer):
    hostel_name = serializers.SerializerMethodField()

    def get_hostel_name(self, obj):
        return obj.get_hostel_display()

    class Meta:
        model = InstituteAddress
        exclude = ['user']


class UserSerializer(serializers.ModelSerializer):
    program = ProgramSerializer()
    secondary_emails = SecondaryEmailSerializer(many=True)
    contacts = ContactNumberSerializer(many=True)
    insti_address = InstituteAddressSerializer()
    mobile = serializers.CharField(source='userprofile.mobile')
    roll_number = serializers.CharField(source='userprofile.roll_number')
    profile_picture = serializers.ImageField(source='userprofile.profile_picture')
    sex = serializers.CharField(source='userprofile.sex')
    type = serializers.CharField(source='userprofile.type')
    is_alumni = serializers.BooleanField(source='userprofile.is_alumni')

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        fields = self.context.get('fields')
        if not isinstance(fields, list) and not isinstance(fields, set):
            fields = []
        fields.extend(DEFAULT_FIELDS)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            fields_to_remove = existing - allowed
            for field in fields_to_remove:
                self.fields.pop(field)

    class Meta:
        model = User
        fields = copy.deepcopy(DEFAULT_FIELDS).extend(USER_FIELDS)


class SendMailSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    subject = serializers.CharField()
    message = serializers.CharField()
    reply_to = serializers.ListField(
        child=serializers.EmailField()
    )
