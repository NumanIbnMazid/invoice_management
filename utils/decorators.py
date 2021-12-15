from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings


# has dashboard permission required


has_dashboard_permission = user_passes_test(
    lambda user: user.is_superuser == True or user.is_staff == True, login_url=settings.HOME_URL
)


def has_dashboard_permission_required(view_func):
    decorated_view_func = login_required(has_dashboard_permission(view_func))
    return decorated_view_func


# has payment permission


has_payment_permission = user_passes_test(
    # lambda user: user.is_authenticated and user.payment_permission, login_url=settings.HOME_URL
    lambda user: user.is_authenticated, login_url=settings.HOME_URL
)


def has_payment_permission_required(view_func):
    decorated_view_func = login_required(has_payment_permission(view_func))
    return decorated_view_func
