from django.conf import settings  # import the settings file


def is_open_for_signup(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'IS_OPEN_FOR_SIGNUP': settings.IS_OPEN_FOR_SIGNUP}
