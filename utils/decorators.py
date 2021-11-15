from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings


# has dashboard permission required


has_dashboard_permission = user_passes_test(
    lambda user: user.is_superuser == True or user.is_staff == True, login_url=settings.HOME_URL
)


def has_dashboard_permission_required(view_func):
    decorated_view_func = login_required(has_dashboard_permission(view_func))
    return decorated_view_func
