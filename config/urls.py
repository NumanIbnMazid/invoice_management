from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.static import serve
import debug_toolbar
# views
from .user_panel_views import HomepageView
from .dashboard_views import DashboardView
from django.conf.urls import handler404, handler500


THIRD_PARTY_URL_PATTERNS = [
    # Django Allauth URLs
    path('accounts/', include('allauth.urls')),
    # Django Select2
    path("select2/", include("django_select2.urls")),
]

END_USER_URL_PATTERNS = [
    # User panel URLs
    path('', DashboardView.as_view(), name='home'),
]

ADMIN_URL_PATTERNS = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # ==============================*** User URLS ***==============================
    path("users/", include(("users.urls", "users"), namespace="users")),
    # ==============================*** Company URLS ***==============================
    path("company/", include(("company.urls", "company"), namespace="company")),
    # ==============================*** Service URLS ***==============================
    path("service/", include(("service.urls", "service"), namespace="service")),
    # ==============================*** Deals URLS ***==============================
    path("deals/", include(("deals.urls", "deals"), namespace="deals")),
    # ==============================*** Invoice URLS ***==============================
    path("invoice/", include(("invoice.urls", "invoice"), namespace="invoice")),
    # ==============================*** Cards URLS ***==============================
    path("server-service-payment/", include(("cards.urls", "cards"), namespace="cards")),
]

urlpatterns = [
    # For handling Static Files in Debug False Mode
    # url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    # ==============================*** UTILS URLS ***==============================
    path("utils/", include(("utils.urls", "utils"), namespace="utils")),
] + THIRD_PARTY_URL_PATTERNS + END_USER_URL_PATTERNS + ADMIN_URL_PATTERNS


# Exception Handlers
handler500 = 'config.user_panel_views.server_error'

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
