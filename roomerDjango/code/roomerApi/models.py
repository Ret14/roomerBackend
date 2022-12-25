from django.contrib.auth.models import AbstractUser
from django.db import models

from roomerApi import utils
from roomerApi import managers


class Interest(models.Model):
    interest = models.CharField(max_length=50)


class RoomAttribute(models.Model):
    attribute = models.CharField(max_length=50)


class Profile(AbstractUser):
    birth_date = models.DateField(auto_now=True)
    sex = models.CharField(choices=utils.sex_field_choices, max_length=1, default='M')
    avatar = models.ImageField(default='static/img/default.png')
    about_me = models.CharField(max_length=1000, default='I\'m good')
    employment = models.CharField(choices=utils.employment_choices, max_length=3, default='E')
    alcohol_attitude = models.CharField(choices=utils.attitude_choices, max_length=1, default='N')
    smoking_attitude = models.CharField(choices=utils.attitude_choices, max_length=1, default='N')
    sleep_time = models.CharField(choices=utils.sleep_time_choices, max_length=1, default='N')
    personality_type = models.CharField(choices=utils.personality_choices, max_length=1, default='E')
    clean_habits = models.CharField(choices=utils.clean_choices, max_length=1, default='N')
    interests = models.ManyToManyField('Interest', related_name='profiles', blank=True)

    objects = managers.ProfileManager()


class Housing(models.Model):
    title = models.CharField(max_length=150)
    month_price = models.IntegerField()
    host = models.ForeignKey(Profile, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    bedrooms_count = models.IntegerField(choices=utils.amount_score_choices)
    bathrooms_count = models.IntegerField(choices=utils.amount_score_choices)
    housing_type = models.CharField(choices=utils.housing_type_choices, max_length=5)
    room_attributes = models.ManyToManyField(RoomAttribute)
    sharing_type = models.CharField(choices=utils.sharing_type_choices, max_length=1)
    photo = models.ImageField(default='static/img/flat_default.jpeg')
    location = models.CharField(max_length=200)


class Review(models.Model):
    class Meta:
        unique_together = ("author", "user")

    score = models.IntegerField(choices=utils.amount_score_choices)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author_set')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_set')
    comment = models.CharField(max_length=1000)
    date_time = models.DateTimeField(auto_now=True)
