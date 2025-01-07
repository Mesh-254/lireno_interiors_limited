from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in with their email or username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Attempt to fetch the user by username or email
            user = User.objects.filter(email=username).first() or User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        # Verify the password
        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
