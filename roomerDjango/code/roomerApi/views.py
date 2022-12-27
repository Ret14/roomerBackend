from rest_framework import permissions, viewsets

from roomerApi import serializers
from roomerApi import models


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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RoomAttributeViewSet(viewsets.ModelViewSet):

    queryset = models.RoomAttribute.objects.all()
    serializer_class = serializers.RoomAttributeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


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

    serializer_class = serializers.HousingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):

    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
