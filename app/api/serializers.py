from rest_framework import serializers

from core.models import Company, Food, Tag, People


class CompanySerializer(serializers.ModelSerializer):
    """Serializer for Company objects"""

    class Meta:
        model = Company
        fields = ('index', 'name')
        read_only_fields = ('index',)


class FoodSerializer(serializers.ModelSerializer):
    """Serializer for Food objects"""
    category = serializers.ReadOnlyField()

    class Meta:
        model = Food
        fields = '__all__'
        read_only_fields = ('id',)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag objects"""

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('id',)


class PeopleSerializer(serializers.ModelSerializer):
    """Serializer for People objects"""
    address = serializers.ReadOnlyField()

    class Meta:
        model = People
        fields = ('name', 'age', 'address', 'phone')
        read_only_fields = ('name', 'age', 'address', 'phone')


class FruitVegetableSerializer(serializers.ModelSerializer):
    """Serializer for People object with fruits and vegetables"""
    username = serializers.CharField(source='name')
    fruits = serializers.ReadOnlyField()
    vegetables = serializers.ReadOnlyField()

    class Meta:
        model = People
        fields = ('username', 'age', 'fruits', 'vegetables')
        read_only_fields = ('username', 'age', 'fruits', 'vegetables')


class CommonFriendsSerializer(serializers.BaseSerializer):
    """Serializer for 2 People's common friend People objects"""

    def to_representation(self, objs_dict):
        return {
            "people1": PeopleSerializer(objs_dict['people1']).data,
            "people2": PeopleSerializer(objs_dict['people2']).data,
            "common_friends": PeopleSerializer(
                objs_dict['common_friends'],
                many=True
            ).data
        }


class EmployeesSerializer(serializers.ModelSerializer):
    """Serializer for all employees in a company"""
    employees = serializers.ReadOnlyField()

    class Meta:
        model = Company
        fields = ('employees',)
