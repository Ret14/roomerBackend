from rest_framework import serializers
from roomerApi import models


class RoomAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoomAttribute
        fields = ['attribute']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = ['score', 'author', 'user', 'comment', ]


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Profile
        fields = [
            'id', 'first_name', 'last_name', 'birth_date', 'sex', 'avatar', 'email', 'about_me',
            'employment', 'alcohol_attitude', 'smoking_attitude', 'sleep_time',
            'personality_type', 'clean_habits', 'interests'
        ]
        extra_kwargs = {'interests': {'required': False}}


class HousingSerializer(serializers.ModelSerializer):
    host = ProfileSerializer()

    class Meta:
        model = models.Housing
        fields = [
            'month_price', 'host', 'description', 'photo',
            'bathrooms_count', 'bedrooms_count', 'housing_type', 'room_attributes', 'sharing_type'
        ]


class InterestSerializer(serializers.ModelSerializer):
    profiles = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = models.Interest
        fields = ['interest', 'profiles']
