from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


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

    def save(self, *args, **kwargs):
        """Save company name as lowercase strings"""
        if self.name:
            self.name = self.name.lower()

        return super(Company, self).save(*args, **kwargs)


FRUIT_LIST = [
    'Apple', 'Watermelon', 'Orange', 'Pear', 'Cherry', 'Strawberry', 'Nectarine', 'Grape',
    'Mango', 'Blueberry', 'Pomegranate', 'Carambola', 'starfruit', 'Plum', 'Banana', 'Raspberry',
    'Mandarin', 'Jackfruit', 'Papaya', 'Kiwi', 'Pineapple', 'Lime', 'Lemon', 'Apricot', 'Grapefruit',
    'Melon', 'Coconut', 'Avocado', 'Peach'
]


class Food(models.Model):
    """Model class for favorite foods"""
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        choices=(('fruit', 'Fruit'), ('vegetable', 'Vegetable'))
    )

    def __str__(self):
        """Return string representation of object"""
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.title()
            if self.name in FRUIT_LIST:
                self.type = 'fruit'
            else:
                self.type = 'vegetable'

        return super(Food, self).save(*args, **kwargs)


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
    balance = models.IntegerField(default=0)
    picture = models.URLField(max_length=200, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    eye_color = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, choices=(('male', 'Male'), ('female', 'Female')), default='female')
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
        return '{}-{}'.format(self.index, self.name)
