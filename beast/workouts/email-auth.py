from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class BasicBackend:
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class EmailBackend(BasicBackend):
    def authenticate(self, username=None, password=None):
        # Try to use an email address, if given one
        if self.valid_email(username):
            try:
                user = User.objects.get(email__iexact=username)
            except User.DoesNotExist:
                return None
        else:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        
        if user.check_password(password):
            return user
        return None

    def valid_email(self, email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False
