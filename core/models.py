from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings



""" 
Custom manager, in this case it helps to authenticate with 
the help of email
"""
class UserManager(BaseUserManager):
    """ 
    This manager defines how to create and manage user objects. 
    We extend BaseUser Manager to create custom user manager for our user
    """

    """
    The prototype of create_user() should accept the username field, 
    plus all required fields as arguments.
    """
    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=self.normalize_email(email), **extra_fields)
        if not email:
            raise ValueError('User must have an email')
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



""" 
Custom user model (extra fields can be added) 
"""
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True);
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    """ User manager for managing the models """
    objects = UserManager()

    """ Field to be used as a unique identifier """
    USERNAME_FIELD = 'email'



"""
Each budget is related to a particular user.It means each user
can have many budgets.It will help to filter budgets according to
the user its associated with
"""
class Budget(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    def __str__(self):
        return self.name
   
    

"""
Each expense is related to a particular budget and also to a user.
It means each budget can have multiple expenses.It will help to filter
expenses according to the associated budget
"""
class Expense(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    budget = models.ForeignKey(
        Budget,
        on_delete=models.CASCADE,
        related_name='expenses'
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name
    