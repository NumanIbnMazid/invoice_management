from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):

    # validate username
    def clean_username(self, username, shallow=False):
        if len(username) >= 50:
            raise ValidationError('Please enter a username less than 50 characters')
        # For other default validations.
        return DefaultAccountAdapter.clean_username(self, username)

    # disable/enable account signup
    def is_open_for_signup(self, request):
        """
        Checks whether or not the site is open for signups.

        Next to simply returning True/False you can also intervene the
        regular flow by raising an ImmediateHttpResponse

        (Comment reproduced from the overridden method.)
        """
        return settings.IS_OPEN_FOR_SIGNUP
