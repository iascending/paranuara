from dateutil.parser import parse
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@mytestwebdomain.com'
        password = 'mysupersecret'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""

        email = 'test@mytestWEBDOMAIN.com'
        password = 'mysupersecret'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@mytestwebdomain.com',
            'test12343'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_company_str(self):
        """Test company string representation"""

        company, _ = models.Company.objects.get_or_create(
            index=200,
            name='SuPerStar'
        )
        self.assertEqual(
            str(company),
            '{}-{}'.format(company.index, company.name)
        )

    def test_food_str(self):
        """Test food string representation"""

        food, _ = models.Food.objects.get_or_create(
            name='kiwi'
        )
        self.assertEqual(str(food), food.name)
        self.assertEqual(food.category, 'fruit')

    def test_tag_str(self):
        """Test tag string representation"""

        tag, _ = models.Tag.objects.get_or_create(
            name='laborum'
        )

        self.assertEqual(str(tag), tag.name)

    def test_people_str(self):
        """Test people string representation"""
        company, _ = models.Company.objects.get_or_create(
            index=200,
            name='SuPerStar'
        )
        tag, _ = models.Tag.objects.get_or_create(
            name='laborum'
        )
        food, _ = models.Food.objects.get_or_create(
            name='kiwi'
        )

        people, _ = models.People.objects.get_or_create(
            pid="595eeb9b96d80a5bc7888b106",
            index=20000,
            guid="5e71dc5d-88c0-4f3b-8b92-d77310c7fa43",
            has_died=True,
            balance=2418.59,
            picture="http://placehold.it/32x32",
            age=61,
            eye_color="blue",
            name="Carmella Lambert",
            gender="female",
            company=company,
            email="carmellalambert@earthmark.com",
            phone="+1 (910) 567-3630",
            street_name="628 Sumner Place",
            suburb="Sperryville",
            state="American Samoa",
            postcode=9819,
            about="Non duis dolore ad enim",
            registered=parse("2016-07-13T12:29:07 -10:00"),
            greeting="Hello, Carmella Lambert! You have 6 unread messages.",
        )
        people.save()
        people.foods.add(food.id)
        people.tags.add(tag.id)

        self.assertEqual(str(people), '{}-{}'.format(people.index, people.name))
