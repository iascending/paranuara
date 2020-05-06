from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


COMMON_FRUIT_LIST = [
    'apple', 'watermelon', 'orange', 'pear', 'cherry', 'strawberry', 'nectarine',
    'grape', 'mango', 'blueberry', 'pomegranate', 'carambola', 'starfruit', 'plum',
    'banana', 'raspberry', 'mandarin', 'jackfruit', 'papaya', 'kiwi', 'pineapple',
    'lime', 'lemon', 'apricot', 'grapefruit', 'melon', 'coconut', 'avocado', 'peach'
]


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates a new user"""
        if not email:
            raise ValueError("A user must have an valid email")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Company(models.Model):
    """Model class for Company objects"""
    index = models.IntegerField(unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        """Return string representation of object"""
        return '{}-{}'.format(self.index, self.name)

    @property
    def employees(self):
        all_employees = People.objects.filter(company__index=self.index)
        if not all_employees:
            return "No employees in this company."
        return [{"index": el.index, "name": el.name} for el in all_employees]


class Food(models.Model):
    """Model class for favorite foods"""
    name = models.CharField(max_length=255, unique=True)

    @property
    def category(self):
        if self.name.lower() in COMMON_FRUIT_LIST:
            return 'fruit'
        else:
            return 'vegetable'

    def __str__(self):
        """Return string representation of object"""
        return self.name


class Tag(models.Model):
    """Model class of Tag objects"""
    name = models.CharField(max_length=50)

    def __str__(self):
        """Return string representation of object"""
        return self.name


class People(models.Model):
    """Model class of people object"""

    pid = models.CharField(max_length=255, unique=True)
    index = models.IntegerField(unique=True)
    guid = models.CharField(max_length=255)
    has_died = models.BooleanField(default=False)
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    picture = models.URLField(max_length=200, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    eye_color = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=50)
    gender = models.CharField(
        max_length=50,
        choices=(('male', 'Male'), ('female', 'Female')),
        default='female'
    )
    company = models.ForeignKey("Company", on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    street_name = models.CharField(max_length=255, null=True, blank=True)
    suburb = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    postcode = models.PositiveIntegerField(null=True, blank=True)
    about = models.CharField(max_length=1024, null=True, blank=True)
    registered = models.DateTimeField(null=True, blank=True)
    tags = models.ManyToManyField("Tag", verbose_name=_("Tags"), blank=True)
    friends = models.ManyToManyField("self", symmetrical=False, blank=True)
    greeting = models.CharField(max_length=255, null=True, blank=True)
    foods = models.ManyToManyField("Food", verbose_name=_("Foods"), blank=True)

    def __str__(self):
        """String representation of People object"""
        return '{}-{}'.format(self.index, self.name)

    @property
    def fruits(self):
        return self.foods.filter(
            name__in=COMMON_FRUIT_LIST
        ).values_list('name', flat=True)

    @property
    def vegetables(self):
        return self.foods.exclude(
            name__in=COMMON_FRUIT_LIST
        ).values_list('name', flat=True)

    @property
    def address(self):
        return ', '.join([
            self.street_name,
            self.suburb,
            self.state,
            str(self.postcode)
        ])

    def get_common_friends(self, other, **options):
        """Get the friends in common for 2 people"""

        seta = set(self.friends.values_list('index', flat=True))
        setb = set(other.friends.values_list('index', flat=True))

        common_friends = People.objects.filter(
            index__in=list(seta & setb)
        ).filter(
            eye_color=options['eye_color'],
            has_died=options['has_died']
        )

        return common_friends
