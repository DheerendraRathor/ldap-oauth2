from rest_framework import serializers

from user_resource.models import InstituteAddress


class UserRoomSerializer(serializers.ModelSerializer):
    roll_number = serializers.CharField(source='user.userprofile.roll_number')

    class Meta:
        model = InstituteAddress
        exclude = ['id', 'user']
