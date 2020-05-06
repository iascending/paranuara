from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('companies/', views.CompanyViewSet.as_view({'get': 'list'}), name='company-list'),
    path('employees/', views.EmployeesView.as_view(), name='employees'),
    path('friends/', views.CommonFriendsView.as_view(), name='friends'),
    path('fruits/', views.FruitVegetalbeView.as_view(), name='fruits'),
]
