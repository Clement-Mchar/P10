import uuid
import datetime
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models import UniqueConstraint
from django.conf import settings
from django.db import models
from .managers import UserManager
from django.core.exceptions import ValidationError
# Create your models here.

def validate_age(birthdate):
    if birthdate :
        age = datetime.date.today() - birthdate
        check_age = int((age).days/365.25)
        if check_age <= 15:
            raise ValidationError("Users must have at least 15 to register.")

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        max_length=40, unique=True, verbose_name="username"
    )
    birthdate = models.DateField(null=True, validators=[validate_age])
    is_active = models.BooleanField(("active"), default=True)
    is_staff = models.BooleanField(("staff"), default=False)
    is_superuser = models.BooleanField(("superuser"), default=False)
    can_be_contacted = models.BooleanField(("contactable"), default=False)
    can_data_be_shared = models.BooleanField(("shareable"), default=False)
    time_created = models.DateTimeField(auto_now=True)

    BIRTHDATE_FIELD = "birthdate"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        db_table = "auth_user"

class Contributor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default=None)
    project = models.ForeignKey(to="project.Project", on_delete=models.CASCADE, default=None)
    issue = models.ForeignKey(to="project.Issue", on_delete=models.CASCADE, null=True, default=None)
    time_created = models.DateTimeField(auto_now=True)
