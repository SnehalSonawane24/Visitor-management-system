from django.contrib.auth.base_user import BaseUserManager


class UserAccountManager(BaseUserManager):
    """
    Organization Registration and login
    """

    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        if not email:
            raise ValueError("Superusers must have an email address")
        if not name:
            raise ValueError("Superusers must have a name")

        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user
