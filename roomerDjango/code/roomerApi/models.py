from django.contrib.auth.models import AbstractUser
from django.db import models
from roomerApi import utils
from roomerApi import managers


class Interest(models.Model):
    interest = models.CharField(max_length=50)


class City(models.Model):
    city = models.CharField(max_length=30)


class RoomAttribute(models.Model):
    attribute = models.CharField(max_length=50)


class Profile(AbstractUser):
    birth_date = models.DateField(default='2022-01-30')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    sex = models.CharField(choices=utils.sex_field_choices, max_length=1, default='M')
    avatar = models.ImageField(default='avatar/default_0.jpg', upload_to='avatar/%Y/%m/%d/')
    about_me = models.CharField(max_length=1000, default='I\'m good')
    employment = models.CharField(choices=utils.employment_choices, max_length=3, default='E')
    alcohol_attitude = models.CharField(choices=utils.attitude_choices, max_length=1, default='N')
    smoking_attitude = models.CharField(choices=utils.attitude_choices, max_length=1, default='N')
    sleep_time = models.CharField(choices=utils.sleep_time_choices, max_length=1, default='N')
    personality_type = models.CharField(choices=utils.personality_choices, max_length=1, default='E')
    clean_habits = models.CharField(choices=utils.clean_choices, max_length=1, default='N')
    interests = models.ManyToManyField(Interest, blank=True)

    objects = managers.ProfileManager()


class HousingPhoto(models.Model):
    photo = models.FileField(upload_to='housing/%Y/%m/%d/', default='housing/flat_default_0.jpg')


class Housing(models.Model):
    title = models.CharField(max_length=150)
    month_price = models.IntegerField()
    host = models.ForeignKey(Profile, on_delete=models.CASCADE)
    file_content = models.ManyToManyField(HousingPhoto, related_name='file_content', blank=True)
    description = models.CharField(max_length=1000)
    bedrooms_count = models.IntegerField(choices=utils.amount_score_choices)
    bathrooms_count = models.IntegerField(choices=utils.amount_score_choices)
    housing_type = models.CharField(choices=utils.housing_type_choices, max_length=5)
    room_attributes = models.ManyToManyField(RoomAttribute, blank=True)
    sharing_type = models.CharField(choices=utils.sharing_type_choices, max_length=1)
    location = models.CharField(max_length=200)


class Review(models.Model):

    score = models.IntegerField(choices=utils.amount_score_choices)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    comment = models.CharField(max_length=1000)
    date = models.DateField(auto_now=True)
    is_anon = models.BooleanField(default=False)


class Message(models.Model):
    chat_id = models.IntegerField()
    date_time = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=512)
    donor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='donor')
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='recipient')
    is_checked = models.BooleanField(default=False)


class Notification(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created = models.DateField(auto_now=True)


class Favourite(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    housing = models.ForeignKey(Housing, on_delete=models.CASCADE)


class Follower(models.Model):
    class Meta:
        unique_together = ("user", "following")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user')
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
