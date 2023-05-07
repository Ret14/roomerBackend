import random
import string
import traceback
from django.core.management.base import BaseCommand
from faker import Faker
from faker.providers import internet, lorem, person, geo
from roomerApi import models


class Command(BaseCommand):
    help = 'Fill db with dummy data'
    fake = Faker()
    random_char_set = string.ascii_letters

    def add_arguments(self, parser):
        parser.add_argument('ratio', default=10000, type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']
        Faker.seed(0)
        self.fake.add_provider(internet)
        self.fake.add_provider(lorem)
        self.fake.add_provider(person)
        self.fake.add_provider(geo)

        try:
            self.create_interests(30)
            self.create_cities()
            self.create_housing_photo()
            self.create_profiles(ratio)
            # self.create_messages(ratio)
            self.create_housings(ratio)
            self.create_favourites(100)
            self.follow_users()
        except Exception:
            models.Interest.objects.all().delete()
            models.Housing.objects.all().delete()
            traceback.print_exc()

    def create_random_string(self, a, b):
        return ''.join(self.fake.random_elements(elements=self.random_char_set,
                                                 length=random.randint(a, b)))

    def create_housing_photo(self):
        for i in range(5):
            models.HousingPhoto(photo=f'housing/flat_default_{i}.jpg').save()

    def create_interests(self, amount):
        interests = self.fake.words(nb=amount, unique=True)
        interests = [
            models.Interest(interest=interests[num])
            for num in range(amount)
        ]
        models.Interest.objects.bulk_create(interests)

    def create_cities(self):
        with open('./roomerApi/management/utils/cities.txt', 'r') as cities_file:
            cities = cities_file.read().strip().split(', ')
        cities_objects = [
            models.City(city=city)
            for city in cities
        ]
        models.City.objects.bulk_create(cities_objects)

    def create_messages(self, amount):
        profile_ids = list(models.Profile.objects.values_list('id', flat=True))
        messages = [
            models.Message(
                chat_id=random.randint(0, 1000),
                text=self.fake.text(max_nb_chars=random.randint(100, 200)),
                donor_id=random.choice(profile_ids),
                recipient_id=random.choice(profile_ids)
            )
            for _ in range(amount)
        ]
        models.Message.objects.bulk_create(messages)

    def create_profiles(self, amount):
        sex_field_choices = ('M', 'F')
        attitude_choices = ('P', 'N', 'I')
        sleep_time_choices = ('N', 'D', 'O')
        personality_choices = ('E', 'I', 'M')
        clean_choices = ('N', 'D', 'C')
        employment_choices = ('NE', 'E', 'S')

        city_ids = list(models.City.objects.values_list('id', flat=True))

        profiles = [
            models.Profile(email=self.fake.email(),
                           city_id=random.choice(city_ids),
                           username=self.create_random_string(5, 20),
                           password=self.fake.password(length=random.randint(20, 50)),
                           first_name=self.fake.first_name(),
                           last_name=self.fake.last_name(),
                           sex=random.choice(sex_field_choices),
                           about_me=self.fake.text(max_nb_chars=random.randint(400, 1000)),
                           employment=random.choice(employment_choices),
                           alcohol_attitude=random.choice(attitude_choices),
                           smoking_attitude=random.choice(attitude_choices),
                           sleep_time=random.choice(sleep_time_choices),
                           personality_type=random.choice(personality_choices),
                           clean_habits=random.choice(clean_choices),
                           birth_date=self.fake.date_between(),
                           avatar=f'avatar/default_{random.randint(0, 4)}.jpg'
                           )
            for _ in range(amount)]
        step = 100
        for i in range(0, amount, step):
            x = i
            models.Profile.objects.bulk_create(profiles[x:x + step])

        password = 'x2Q6$mUcn3'
        names = ('max', 'rodion', 'nika', 'andrew')
        for name in names:
            for i in range(3):
                models.Profile.objects.create_user(
                    city_id=random.choice(city_ids),
                    email=self.fake.email(),
                    username=f'{name}_user_{i}',
                    password=password,
                    first_name=self.fake.first_name(),
                    last_name=self.fake.last_name(),
                    sex=random.choice(sex_field_choices),
                    about_me=self.fake.text(max_nb_chars=random.randint(400, 1000)),
                    employment=random.choice(employment_choices),
                    alcohol_attitude=random.choice(attitude_choices),
                    smoking_attitude=random.choice(attitude_choices),
                    sleep_time=random.choice(sleep_time_choices),
                    personality_type=random.choice(personality_choices),
                    clean_habits=random.choice(clean_choices),
                    avatar=f'avatar/default_{random.randint(0, 4)}.jpg'
                )
        interests_ids = list(models.Interest.objects.values_list('id', flat=True))
        profile_ids = list(models.Profile.objects.values_list('id', flat=True))

        interest_to_profile_links = []
        for profile_id in profile_ids:
            profile_interests = random.sample(interests_ids, random.randint(5, 10))
            for interest_id in profile_interests:
                interest_profile = models.Profile.interests.through(profile_id=profile_id, interest_id=interest_id)
                interest_to_profile_links.append(interest_profile)

            models.Profile.interests.through.objects.bulk_create(interest_to_profile_links)
            interest_to_profile_links.clear()

    def create_housings(self, amount):
        housing_type_choices = ('F', 'DU', 'H', 'DO')
        sharing_type_choices = ('P', 'S')
        profile_ids = list(models.Profile.objects.values_list('id', flat=True))
        housings = [
            models.Housing(month_price=random.randint(30000, 100000),
                           host_id=profile_ids[number],
                           description=self.fake.text(max_nb_chars=random.randint(400, 1000)),
                           bedrooms_count=random.randint(1, 5),
                           bathrooms_count=random.randint(1, 5),
                           housing_type=random.choice(housing_type_choices),
                           sharing_type=random.choice(sharing_type_choices),
                           title=self.fake.text(max_nb_chars=random.randint(50, 150)),
                           location=' '.join(self.fake.location_on_land())
                           )
            for number in range(amount)]
        step = 100
        for i in range(0, amount, step):
            x = i
            models.Housing.objects.bulk_create(housings[x:x + step])

        housing_ids = list(models.Housing.objects.values_list('id', flat=True))
        housing_photo_id = list(models.HousingPhoto.objects.values_list('id', flat=True))

        photo_to_housing_links = []
        for h_id in housing_ids:
            housing_photos = random.sample(housing_photo_id, random.randint(1, 4))
            for photo_id in housing_photos:
                photo_housing = models.Housing.file_content.through(housing_id=h_id, housingphoto_id=photo_id)
                photo_to_housing_links.append(photo_housing)

        models.Housing.file_content.through.objects.bulk_create(photo_to_housing_links)

        photo_to_housing_links.clear()

    def create_favourites(self, amount):
        user = models.Profile.objects.get(username='max_user_0')
        housing = list(models.Housing.objects.all()[0:amount])
        favourites = [
            models.Favourite(
                user=user,
                housing=housing[number]
            ) for number in range(amount)]
        models.Favourite.objects.bulk_create(favourites)

    def follow_users(self):
        names = ('max_', 'rodion_', 'nika_', 'andrew_')
        for name in names:
            profile_ids = list(models.Profile.objects.filter(username__startswith=name).values_list('id', flat=True))
            for user_id in profile_ids:
                for follow_id in profile_ids:
                    if follow_id != user_id:
                        models.Follower(user_id=user_id, following_id=follow_id).save()
