from django.contrib.auth.models import UserManager
from django.db.models import Q


class ProfileManager(UserManager):

    def get_by_natural_key(self, username):
        return self.get(
            Q(**{self.model.USERNAME_FIELD: username}) |
            Q(**{self.model.EMAIL_FIELD: username})
        )
