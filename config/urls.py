from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
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
    path("company/", include(("company.urls", "company"), namespace="company")),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    # ==============================*** UTILS URLS ***==============================
    path("utils/", include(("utils.urls", "utils"), namespace="utils")),
] + THIRD_PARTY_URL_PATTERNS + END_USER_URL_PATTERNS + ADMIN_URL_PATTERNS


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        # Django Debug Toolbar
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns = urlpatterns + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
