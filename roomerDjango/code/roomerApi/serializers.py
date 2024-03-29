from rest_framework import serializers
from roomerApi import models


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Interest
        fields = ['id', 'interest']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = ['id', 'city']


class HousingPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HousingPhoto
        fields = ['photo']


class RoomAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoomAttribute
        fields = ['attribute']


class ProfileSerializer(serializers.ModelSerializer):
    interests = InterestSerializer(many=True, required=False)
    city = serializers.CharField(required=False, source='city.city')

    class Meta:
        model = models.Profile
        fields = [
            'id', 'first_name', 'last_name', 'birth_date', 'sex', 'avatar', 'email', 'about_me', 'city',
            'employment', 'alcohol_attitude', 'smoking_attitude', 'sleep_time',
            'personality_type', 'clean_habits', 'interests'
        ]

    def update(self, instance, validated_data):
        if 'interests' in validated_data:
            interests = validated_data.pop('interests')
            for interest in interests:
                interest_obj = models.Interest.objects.get(interest=interest['interest'])
                instance.interests.add(interest_obj)
        if 'city' in validated_data:
            city = validated_data.pop('city')['city']
            city_obj = models.City.objects.get(city=city)
            instance.city = city_obj

        return super().update(instance, validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(required=False)

    class Meta:
        model = models.Review
        fields = ['id', 'score', 'author', 'receiver', 'comment', 'is_anon']


class HousingSerializer(serializers.ModelSerializer):
    file_content = HousingPhotoSerializer(required=False, many=True)
    host = ProfileSerializer(required=False)

    class Meta:
        model = models.Housing
        fields = [
            'id', 'month_price', 'host', 'description', 'file_content', 'title', 'location',
            'bathrooms_count', 'bedrooms_count', 'housing_type', 'room_attributes', 'sharing_type'
        ]


class ChatsSerializer(serializers.ModelSerializer):
    donor = ProfileSerializer(required=False)
    recipient = ProfileSerializer(required=False)

    class Meta:
        model = models.Message
        fields = ['id', 'chat_id', 'date_time', 'text', 'donor', 'recipient', 'is_checked']


class NotificationSerializer(serializers.ModelSerializer):
    message = ChatsSerializer()

    class Meta:
        model = models.Notification
        fields = ['id', 'message']


class FavouritesSerializer(serializers.ModelSerializer):
    housing = HousingSerializer()

    class Meta:
        model = models.Favourite
        fields = ['id', 'housing']


class FollowersSerializer(serializers.ModelSerializer):
    following = ProfileSerializer()

    class Meta:
        model = models.Follower
        fields = ['id', 'following']

