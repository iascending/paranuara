from faker import Faker
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Food, Tag, People, Company
from api.serializers import EmployeesSerializer

EMPLOYEES_URL = reverse('api:employees')
FRIENDS_URL = reverse('api:friends')
FRUITS_URL = reverse('api:fruits')
fakegen = Faker()


def sample_food(name='apple'):
    """Create and return a sample food"""
    return Food.objects.create(name=name)


def sample_tag(name='excepteur'):
    """Create and return a sample tag"""
    return Tag.objects.create(name=name)


def sample_company(index, name="BIGCOMP"):
    """Create and return a sample company"""
    return Company.objects.create(index=index, name=name)


def sample_employee(index, company):
    """Create and return a sample employee"""
    sample_data = {
        "pid": str(fakegen.random_number(20)),
        "guid": str(fakegen.random_number(20)),
        "has_died": False,
        "balance": fakegen.random_number(5),
        "picture": "http://placehold.it/32x32",
        "age": fakegen.random_int(),
        "eye_color": "brown",
        "name": "{} {}".format(fakegen.first_name(), fakegen.last_name()),
        "gender": "female",
        "email": fakegen.email(),
        "phone": fakegen.phone_number(),
        "street_name": "{} {}".format(fakegen.random_int(), fakegen.street_name()),
        "suburb": "Sperryville",
        "state": "American Samoa",
        "postcode": fakegen.postcode(),
        "about": "Non duis dolore ad enim.enderit dolor",
        "greeting": "Hello",
        "index": index,
        "company": company
    }
    return People.objects.create(**sample_data)


class PublicEmployeeApiTests(TestCase):
    """Test unauthorized employee API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required_employees(self):
        """Test that authorization is required to get employees' list"""
        res = self.client.get(EMPLOYEES_URL, {'company': '0'})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_friends(self):
        """Test that authorization is required to get common friends"""
        res = self.client.get(FRIENDS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_fruits(self):
        """Test that authorization is required to get fruits and vegetables"""
        res = self.client.get(FRUITS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateEmployeeApiTests(TestCase):
    """Test authorized employee API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='testuser@gmail.com',
            password='testpass',
            name='Test User'
        )
        self.client.force_authenticate(self.user)
        self.food_names = ['cucumber', 'apple', 'carrot']
        self.company_names = ['INTERLOO', 'LINGOAGE', 'MAINELAND']
        self.foods = []
        self.companies = []
        self.employees = []

        size_list = len(self.food_names)
        for curr in range(size_list):
            self.foods.append(sample_food(self.food_names[curr]))
            self.companies.append(sample_company(index=curr, name=self.company_names[curr]))
            self.employees.append(sample_employee(index=curr, company=self.companies[int(curr/2)]))

        for curr in range(size_list-1):
            self.employees[curr].friends.add(self.employees[size_list-1])
            self.employees[curr].foods.add(self.foods[size_list-1])
            self.employees[curr].foods.add(self.foods[curr])
            self.employees[curr].save()

    def test_retrieve_employee_list_by_index(self):
        """Test to to retrieve all employees in a company by company index"""
        res = self.client.get(EMPLOYEES_URL, {'company': '0'})
        company = Company.objects.filter(index=0)
        serializer = EmployeesSerializer(company, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_employee_list_by_name(self):
        """Test to retrieve all employees in a company by company name"""
        res = self.client.get(
            EMPLOYEES_URL,
            {'company': self.companies[0].name}
        )
        company = Company.objects.filter(index=0)
        serializer = EmployeesSerializer(company, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_employee_list_wrong_index(self):
        """Test to retrieve employee list in a company by non-existing index"""
        res = self.client.get(EMPLOYEES_URL, {'company': '1000'})
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_employee_list_wrong_name(self):
        """Test to retrieve employee list in a company by non-existing index"""
        res = self.client.get(EMPLOYEES_URL, {'company': 'wrong'})
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_common_friends_without_params(self):
        """Test to retrieve common friends without 2 people"""
        res = self.client.get(FRIENDS_URL)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_common_friends_with_one_person(self):
        """Test to retrieve common friends with 1 people only"""
        res = self.client.get(FRIENDS_URL, {'index1': 0})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_common_friends_with_invalid_params(self):
        """Test to retrieve common friends with invalid_params"""
        res = self.client.get(FRIENDS_URL, {'people1': 0, 'people2': 1})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_common_friends_with_nonexist_people(self):
        """Test to retrieve common friends with nonexist people"""
        res = self.client.get(FRIENDS_URL, {'index1': 0, 'index2': 100})

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_common_friends(self):
        """Test to retrieve 2 people's common friends"""
        res = self.client.get(FRIENDS_URL, {'index1': 0, 'index2': 1})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.employees[2].name,
            res.data['common_friends'][0]['name']
        )

    def test_retrieve_fruits_vegetables_invalid_param(self):
        """Test to retrieve fruits or vegetables with invalid query param"""
        res = self.client.get(FRUITS_URL, {'name': 100})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_fruits_vegetables_non_exist(self):
        """Test to retrieve fruits or vegetables for non existing people"""
        res = self.client.get(FRUITS_URL, {'index': 100})

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_employee_fruits_vegetables(self):
        """Test to retrieve fruits or vegetables of indivial"""
        res = self.client.get(FRUITS_URL, {'index': 1})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(self.foods[1].name, res.data[0]['fruits'])
        self.assertIn(self.foods[2].name, res.data[0]['vegetables'])
