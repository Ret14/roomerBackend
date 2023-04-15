from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
import datetime
from roomerApi import serializers
from roomerApi import models
from django.db.models import Q


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = models.Profile.objects.all()

    @staticmethod
    def get_birth_date_from_age(age: int):
        today_date = datetime.date.today()
        today_year = today_date.year
        target_year = today_year - age
        return datetime.date(target_year, today_date.month, today_date.day)

    @staticmethod
    def get_common_items_amount(list_a: list, list_b: list):
        return sum(x == y for x, y in zip(list_a, list_b))

    def filter_queryset(self, queryset):
        params = self.request.query_params
        offset = params.get('offset')
        limit = params.get('limit')
        try:
            offset = int(offset)
        except Exception:
            offset = 0
        try:
            limit = int(limit)
        except Exception:
            limit = 20

        if 'age_from' in params:
            queryset = queryset.filter(birth_date__range=(
                datetime.date(1970, 1, 1),
                self.get_birth_date_from_age(int(params['age_from']))
            ))

        if 'age_to' in params:
            queryset = queryset.filter(birth_date__range=(
                self.get_birth_date_from_age(int(params['age_to'])),
                datetime.date.today()
            ))

        if 'sex' in params:
            queryset = queryset.filter(sex=params['sex'])

        if 'sleep_time' in params:
            queryset = queryset.filter(sleep_time=params['sleep_time'])

        if 'personality_type' in params:
            queryset = queryset.filter(personality_type=params['personality_type'])

        if 'employment' in params:
            queryset = queryset.filter(employment=params['employment'])

        if 'alcohol_attitude' in params:
            queryset = queryset.filter(alcohol_attitude=params['alcohol_attitude'])

        if 'smoking_attitude' in params:
            queryset = queryset.filter(smoking_attitude=params['smoking_attitude'])

        if 'clean_habits' in params:
            queryset = queryset.filter(clean_habits=params['clean_habits'])

        if 'interests' in params:
            interests_ids = list(map(lambda x: int(x), params.getlist('interests')))
            if len(interests_ids) == 1:
                matching_interests_amount = 1
            else:
                matching_interests_amount = round(len(interests_ids) * 0.4)
            for query in queryset:
                query_interests_ids = list(map(lambda x: int(x['id']), query.interests.values('id')))
                query_match_amount = len(set(query_interests_ids) & set(interests_ids))
                if query_match_amount < matching_interests_amount:
                    queryset = queryset.exclude(id=query.id)

        if 'city' in params:
            city = params['city']
            city_id = models.City.objects.get(city=city).id
            queryset = queryset.filter(city_id=city_id)

        return queryset[offset:offset + limit]

    serializer_class = serializers.ProfileSerializer
    permission_classes = [permissions.AllowAny]


class InterestsViewSet(viewsets.ModelViewSet):
    queryset = models.Interest.objects.all()[:20]
    serializer_class = serializers.InterestSerializer
    permission_classes = [permissions.AllowAny]


class CitiesViewSet(viewsets.ModelViewSet):
    queryset = models.City.objects.all()
    serializer_class = serializers.CitySerializer
    permission_classes = [permissions.AllowAny]


class RoomAttributeViewSet(viewsets.ModelViewSet):
    queryset = models.RoomAttribute.objects.all()
    serializer_class = serializers.RoomAttributeSerializer
    permission_classes = [permissions.AllowAny]


class HousingViewSet(viewsets.ModelViewSet):
    queryset = models.Housing.objects.all()

    def filter_queryset(self, queryset):
        month_price_from = self.request.query_params.get('month_price_from')
        offset = self.request.query_params.get('offset')
        limit = self.request.query_params.get('limit')
        try:
            offset = int(offset)
        except Exception:
            offset = 0
        try:
            limit = int(limit)
        except Exception:
            limit = 20
        if month_price_from is not None:
            queryset = queryset.filter(month_price__gte=month_price_from)

        month_price_to = self.request.query_params.get('month_price_to')
        if month_price_to is not None:
            queryset = queryset.filter(month_price__lte=month_price_to)

        bathrooms_count = self.request.query_params.get('bathrooms_count')
        if bathrooms_count is not None:
            if bathrooms_count == '>3':
                queryset = queryset.filter(bathrooms_count__gt=3)
            else:
                queryset = queryset.filter(bathrooms_count=bathrooms_count)

        bedrooms_count = self.request.query_params.get('bedrooms_count')
        if bedrooms_count is not None:
            if bedrooms_count == '>3':
                queryset = queryset.filter(bedrooms_count__gt=3)
            else:
                queryset = queryset.filter(bedrooms_count=bedrooms_count)

        housing_type = self.request.query_params.get('housing_type')
        if housing_type is not None:
            queryset = queryset.filter(housing_type=housing_type)

        sharing_type = self.request.query_params.get('sharing_type')
        if sharing_type is not None:
            queryset = queryset.filter(sharing_type=sharing_type)

        return queryset[offset:offset + limit]

    def create(self, request, *args, **kwargs):
        files = request.FILES.getlist('file_content')
        mutable_data = request.data.copy()
        host_id = mutable_data.pop('host')[0]
        if files:
            mutable_data.pop('file_content')
            serializer = serializers.HousingSerializer(data=mutable_data)
            if serializer.is_valid():
                serializer.save(host_id=host_id)
                housing_record = models.Housing.objects.get(id=serializer.data['id'])
                uploaded_files = []
                for file in files:
                    content = models.HousingPhoto.objects.create(photo=file)
                    uploaded_files.append(content)
                housing_record.file_content.add(*uploaded_files)
                context = serializer.data
                context["file_content"] = [file.id for file in uploaded_files]
                return Response(context, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = serializers.HousingSerializer(data=mutable_data)
            if serializer.is_valid():
                serializer.save(host_id=host_id)
                context = serializer.data
                return Response(context, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer_class = serializers.HousingSerializer
    permission_classes = [permissions.AllowAny]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.AllowAny]


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer

    def filter_queryset(self, queryset):
        user_id = self.request.query_params.get('user_id')
        if user_id is not None:
            notification = list(queryset.filter(message__recipient_id=user_id).all())
            queryset.filter(message__recipient_id=user_id).delete()
            return notification
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ChatsViewSet(viewsets.ModelViewSet):
    queryset = models.Message.objects.all()

    @action(methods=['put'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def mark_checked(self, request, pk=None):
        message = self.queryset.filter(id=pk)[0]
        if message:
            data = {"is_checked": True}
            serializer = self.get_serializer(message, data=data, partial=True)
            models.Notification.objects.filter(message_id=pk).delete()
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def filter_queryset(self, queryset):
        user_id = self.request.query_params.get('user_id')
        chat_id = self.request.query_params.get('chat_id')
        offset = self.request.query_params.get('offset')
        limit = self.request.query_params.get('limit')
        try:
            offset = int(offset)
        except Exception:
            offset = 0
        try:
            limit = int(limit)
        except Exception:
            limit = 20
        if user_id is not None:
            if chat_id != "":
                queryset = queryset.filter(chat_id=chat_id)
            else:
                queryset = queryset.filter(Q(donor_id=user_id) | Q(recipient_id=user_id)).order_by("chat_id").distinct(
                    "chat_id")
        return queryset[offset:offset + limit]

    serializer_class = serializers.ChatsSerializer
    permission_classes = [permissions.AllowAny]
