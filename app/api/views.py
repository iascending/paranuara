from rest_framework import generics, viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Company, People
from api import serializers


class CompanyViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage companies in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Company.objects.all()
    serializer_class = serializers.CompanySerializer


class EmployeesView(generics.ListAPIView):
    """An APIView for listing all employees in a company"""
    serializer_class = serializers.EmployeesSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = Company.objects.all()

    def get(self, request):
        """Get a list of employees in a company"""
        param = self.request.query_params.get('company')
        if not param:
            response = {"message": "Either company name or index required."}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        if param.isnumeric():
            self.queryset = self.queryset.filter(index__exact=int(param))
        else:
            self.queryset = self.queryset.filter(name__icontains=param)

        if self.queryset.count() != 1:
            response = {"message": "Please provide accurate company info."}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        return super(EmployeesView, self).get(request)


class FruitVegetalbeView(generics.ListAPIView):
    """An APIView for listing fruit and vegetable individual likes"""
    serializer_class = serializers.FruitVegetableSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = People.objects.all()

    def get(self, request):
        param = self.request.query_params.get('index')
        if not param:
            response = {"message": "Please enter people index as query parameter."}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.queryset = self.queryset.filter(index__exact=int(param))
        except ValueError:
            response = {"message": "Invalid query parameter"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        if self.queryset.count() != 1:
            response = {"message": "Records do not exist."}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        return super(FruitVegetalbeView, self).get(request)


class CommonFriendsView(generics.ListAPIView):
    """An APIView for listing 2 people in commond"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        """Get the details of 2 people and their common friends"""
        index1 = request.query_params.get('index1')
        index2 = request.query_params.get('index2')

        if not index1 or not index2 or index1 == index2:
            response = {"message": "Two people should be provided."}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        try:
            people1 = People.objects.get(index=int(index1))
            people2 = People.objects.get(index=int(index2))
        except People.DoesNotExist:
            response = {"message": "Incorrect query parameters provided."}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            response = {"message": "Incorrect query parameters provided."}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        options = {'eye_color': 'blue', 'has_died': False}
        objs_dict = {
            'people1': people1,
            'people2': people2,
            'common_friends': people1.get_common_friends(people2, **options)
        }

        return Response(serializers.CommonFriendsSerializer(objs_dict).data)
