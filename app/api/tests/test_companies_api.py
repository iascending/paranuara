from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Company
from api.serializers import CompanySerializer


COMPANIES_URL = reverse('api:company-list')


class PublicCompaniesApiTests(TestCase):
    """Test the publicly available companies API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving companies"""
        res = self.client.get(COMPANIES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCompaniesApiTests(TestCase):
    """Test the authorized user companies API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@myprivatedomain.com',
            'passtest'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_companies(self):
        """Test retrieving company list"""
        Company.objects.create(index=1000, name='BIGCOMPANY')
        Company.objects.create(index=1001, name='SMACOMPANY')

        res = self.client.get(COMPANIES_URL)

        companies = Company.objects.all().order_by('name')
        serializer = CompanySerializer(companies, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
