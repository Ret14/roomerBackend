from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from roomerApi import serializers
from roomerApi import models
from django.db.models import Q

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = models.Profile.objects.all()

    def filter_queryset(self, queryset):
        sex = self.request.query_params.get('sex')
        if sex is not None:
            queryset = queryset.filter(sex=sex)

        sleep_time = self.request.query_params.get('sleep_time')
        if sleep_time is not None:
            queryset = queryset.filter(sleep_time=sleep_time)

        personality_type = self.request.query_params.get('personality_type')
        if personality_type is not None:
            queryset = queryset.filter(personality_type=personality_type)

        employment = self.request.query_params.get('employment')
        if employment is not None:
            queryset = queryset.filter(employment=employment)

        alcohol_attitude = self.request.query_params.get('alcohol_attitude')
        if alcohol_attitude is not None:
            queryset = queryset.filter(alcohol_attitude=alcohol_attitude)

        smoking_attitude = self.request.query_params.get('smoking_attitude')
        if smoking_attitude is not None:
            queryset = queryset.filter(smoking_attitude=smoking_attitude)

        clean_habits = self.request.query_params.get('clean_habits')
        if clean_habits is not None:
            queryset = queryset.filter(clean_habits=clean_habits)

        return queryset

    serializer_class = serializers.ProfileSerializer
    permission_classes = [permissions.AllowAny]


class InterestsViewSet(viewsets.ModelViewSet):
    queryset = models.Interest.objects.all()[:20]
    serializer_class = serializers.InterestSerializer
    permission_classes = [permissions.AllowAny]


class RoomAttributeViewSet(viewsets.ModelViewSet):
    queryset = models.RoomAttribute.objects.all()
    serializer_class = serializers.RoomAttributeSerializer
    permission_classes = [permissions.AllowAny]


class HousingViewSet(viewsets.ModelViewSet):
    queryset = models.Housing.objects.all()

    def filter_queryset(self, queryset):
        month_price_from = self.request.query_params.get('month_price_from')
        if month_price_from is not None:
            queryset = queryset.filter(month_price__gte=month_price_from)

        month_price_to = self.request.query_params.get('month_price_to')
        if month_price_to is not None:
            queryset = queryset.filter(month_price__lte=month_price_to)

        bathrooms_count = self.request.query_params.get('bathrooms_count')
        if bathrooms_count is not None:
            if bathrooms_count == '>3':
                queryset = queryset.filter(bathrooms_count__gte=3)
            else:
                queryset = queryset.filter(bathrooms_count=bathrooms_count)

        bedrooms_count = self.request.query_params.get('bedrooms_count')
        if bedrooms_count is not None:
            if bedrooms_count == '>3':
                queryset = queryset.filter(bedrooms_count__gte=3)
            else:
                queryset = queryset.filter(bedrooms_count=bedrooms_count)

        housing_type = self.request.query_params.get('housing_type')
        if housing_type is not None:
            queryset = queryset.filter(housing_type=housing_type)

        sharing_type = self.request.query_params.get('sharing_type')
        if sharing_type is not None:
            queryset = queryset.filter(sharing_type=sharing_type)

        return queryset

    def create(self, request, *args, **kwargs):
        files = request.FILES.getlist('file_content')
        if files:
            request.data.pop('file_content')
            serializer = serializers.HousingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
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
            serializer = serializers.HousingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                context = serializer.data
                return Response(context, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer_class = serializers.HousingSerializer
    permission_classes = [permissions.AllowAny]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.AllowAny]


class ChatsViewSet(viewsets.ModelViewSet):
    queryset = models.Message.objects.all()

    def filter_queryset(self, queryset):
        user_id = self.request.query_params.get('user_id')
        chat_id = self.request.query_params.get('chat_id')
        if user_id is not None:
            if chat_id != "":
                queryset = queryset.filter(chat_id=chat_id)
            else:
                queryset = queryset.filter(Q(donor_id=user_id) | Q(recipient_id=user_id)).order_by("chat_id").distinct("chat_id")
        return queryset

    serializer_class = serializers.ChatsSerializer
    permission_classes = [permissions.AllowAny]
