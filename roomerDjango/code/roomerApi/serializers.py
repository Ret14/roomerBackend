from rest_framework import serializers
from roomerApi import models


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Interest
        fields = ['id', 'interest']


class HousingPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HousingPhoto
        fields = ['photo']


class RoomAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoomAttribute
        fields = ['attribute']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = ['score', 'author', 'user', 'comment', ]


class ProfileSerializer(serializers.ModelSerializer):
    interests = InterestSerializer(many=True, required=False)

    class Meta:
        model = models.Profile
        fields = [
            'id', 'first_name', 'last_name', 'birth_date', 'sex', 'avatar', 'email', 'about_me',
            'employment', 'alcohol_attitude', 'smoking_attitude', 'sleep_time',
            'personality_type', 'clean_habits', 'interests'
        ]

    def update(self, instance, validated_data):
        print(validated_data)
        if 'interests' in validated_data:
            interests = validated_data.pop('interests')
            for interest in interests:
                interest_obj = models.Interest.objects.get(interest=interest['interest'])
                instance.interests.add(interest_obj)

        return super().update(instance, validated_data)


class HousingSerializer(serializers.ModelSerializer):
    file_content = HousingPhotoSerializer(required=False, many=True)

    class Meta:
        model = models.Housing
        fields = [
            'id', 'month_price', 'host', 'description', 'file_content', 'title', 'location',
            'bathrooms_count', 'bedrooms_count', 'housing_type', 'room_attributes', 'sharing_type'
        ]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = ['id', 'date_time', 'text', 'donor', 'recipient', 'isChecked']
