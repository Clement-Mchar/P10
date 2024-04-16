from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):
        extra_fields = {"is_staff": False, "is_superuser": False, **extra_fields}
        if username is None:
            raise TypeError("Users must have a username.")

        user = self.model(username=username)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields = {"is_staff": True, "is_superuser": True, **extra_fields}
        if password is None:
            raise TypeError("Superusers must have a password.")
        user = self.create_user(username, password, **extra_fields)
        user.birthdate = None
        user.is_superuser = True
        user.is_staff = True
        user.can_data_be_shared = True
        user.can_be_contacted = True
        user.save()

        return user
