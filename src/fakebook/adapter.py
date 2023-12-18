
from allauth.account.adapter import DefaultAccountAdapter

from configuration.models import get_the_config

class NoSignUpAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        return get_the_config().registration_enabled
