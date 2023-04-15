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
            self.create_profiles(ratio)
            self.create_housings(ratio)
        except Exception:
            # models.Profile.objects.all().delete()
            models.Interest.objects.all().delete()
            # models.Review.objects.all().delete()
            models.Housing.objects.all().delete()
            # models.RoomAttribute.objects.all().delete()
            traceback.print_exc()

    def create_random_string(self, a, b):
        return ''.join(self.fake.random_elements(elements=self.random_char_set,
                                                 length=random.randint(a, b)))

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
                           birth_date=self.fake.date_between()
                           )
            for _ in range(amount)]

        models.Profile.objects.bulk_create(profiles)
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

        models.Housing.objects.bulk_create(housings)
