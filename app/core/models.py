from django.db import models
import uuid
import os
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings

def recipe_image_file_path(instance, filename):
    '''Generate file path for new recipe image'''
    ext = filename.split('.')[-1] #return extension of file name
    filename = f'{uuid.uuid4()}.{ext}'

    # join
    return os.path.join('upload/recipe/', filename)

# create user manager class
class UserManager(BaseUserManager):
    
    # extra_fields, pass extra functions and add it to user
    def create_user(self, email, password=None, **extra_fields):
        '''creates and saves a new user'''
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email),**extra_fields) #normalize to remove uppercase for @test.com
        user.set_password(password)
        user.save(using=self._db)

        return user
    def create_superuser(self, email, password):
        '''creates and saves a new superuser'''
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

    # create the model
class User(AbstractBaseUser, PermissionsMixin):
    '''custom user model tht supports using email instead of user name'''
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # assign user manager to objects attribute
    objects = UserManager()

    USERNAME_FIELD = 'email' #making the default email instead of username

class Tag(models.Model):
    '''Tag to be used for a recipe'''
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    '''Ingredient to be used in a recipe'''
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class Recipe(models.Model): 
    '''Recipe object'''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)

    # add ingredient and tags
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title


