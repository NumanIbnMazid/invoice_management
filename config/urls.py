from django.conf import settings
from django.contrib import admin
from django.urls import path, include
import debug_toolbar
# views
from .user_panel_views import HomepageView
from .dashboard_views import DashboardView


THIRD_PARTY_URL_PATTERNS = [
    # Third Party URL Patterns
    path('', HomepageView.as_view(), name='home'),
]

END_USER_URL_PATTERNS = [
    # User panel URLs
]

ADMIN_URL_PATTERNS = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # ==============================*** UTILS URLS ***==============================
    path("utils/", include(("utils.urls", "utils"), namespace="utils")),
]

urlpatterns = [
    path('admin/', admin.site.urls),
] + THIRD_PARTY_URL_PATTERNS + END_USER_URL_PATTERNS + ADMIN_URL_PATTERNS


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        # Django Debug Toolbar
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
