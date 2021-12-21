from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.choices import Currency
from utils.snippets import autoslugFromUUID


class DashboardSetting(models.Model):

    class Skin(models.TextChoices):
        LIGHT_LAYOUT = 'light-layout', _('Light')
        BORDERED_LAYOUT = 'bordered-layout', _('Bordered')
        DARK_LAYOUT = 'dark-layout', _('Dark')
        SEMI_DARK_LAYOUT = 'semi-dark-layout', _('Semi Dark')

    class LayoutWidth(models.TextChoices):
        FULL_WIDTH = 'full-width', _('Full Width')
        BOXED = 'boxed', _('Boxed')

    class NavbarColor(models.TextChoices):
        INHERIT = 'inherit', _('Inherit')
        PRIMARY = 'bg-primary', _('Primary')
        SECONDARY = 'bg-secondary', _('Secondary')
        SUCCESS = 'bg-success', _('Success')
        DANGER = 'bg-danger', _('Danger')
        INFO = 'bg-info', _('Info')
        WARNING = 'bg-warning', _('Warning')
        DARK = 'bg-dark', _('Dark')

    class NavbarType(models.TextChoices):
        NAV_FLOATING = 'navbar-floating', _('Floating')
        NAV_STICKY = 'navbar-sticky', _('Sticky')
        NAV_STATIC = 'navbar-static', _('Static')
        NAV_HIDDEN = 'navbar-hidden', _('Hidden')

    class FooterType(models.TextChoices):
        FOOTER_STICKY = 'footer-fixed', _('Sticky')
        FOOTER_STATIC = 'footer-static', _('Static')
        FOOTER_HIDDEN = 'footer-hidden', _('Hidden')

    title = models.CharField(
        max_length=100, default="Dashboard", blank=True, null=True
    )
    skin = models.CharField(
        max_length=100, blank=True, null=True, choices=Skin.choices, default="dark-layout"
    )
    menu_collapsed = models.BooleanField(default=False)
    layout_width = models.CharField(
        max_length=100, choices=LayoutWidth.choices, default="full-width", blank=True, null=True
    )
    navbar_color = models.CharField(
        max_length=100, choices=NavbarColor.choices, default="inherit", blank=True, null=True
    )
    navbar_type = models.CharField(
        max_length=100, choices=NavbarType.choices, default="navbar-floating", blank=True, null=True
    )
    footer_type = models.CharField(
        max_length=100, choices=FooterType.choices, default="footer-fixed", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Dashboard Setting'
        verbose_name_plural = 'Dashboard Settings'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_navbar_class(self):
        if self.skin in ["light-layout", "bordered-layout", "semi-dark-layout"]:
            return "navbar-light"
        return "navbar-dark"

    def get_navbar_type(self):
        if self.navbar_type == "navbar-sticky":
            return "fixed-top"
        elif self.navbar_type == "navbar-static":
            return "navbar-static-top"
        elif self.navbar_type == "navbar-hidden":
            return "navbar-static-top d-none"
        return "floating-nav"

    def get_menu_class(self):
        if self.skin in ["light-layout", "bordered-layout"]:
            return "menu-light"
        return "menu-dark"

    def get_menu_collapsed(self):
        if self.menu_collapsed == True:
            return "menu-collapsed"
        return "menu-expanded"

    def get_layout_width(self):
        if self.layout_width == "boxed":
            return "content-wrapper container p-0"
        return "content-wrapper"

    def get_footer_type(self):
        if self.footer_type == "footer-fixed":
            return "footer footer-light"
        elif self.footer_type == "footer-static":
            return "footer footer-light footer-static"
        else:
            return "footer footer-light footer-static d-none"
        

@autoslugFromUUID()
class Configuration(models.Model):
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=254)
    currency = models.CharField(max_length=10, choices=Currency.choices, default=Currency.USD)
    card_page_title = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuration'
        verbose_name_plural = 'Configurations'
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.payment_amount)

    def get_fields(self):
        def get_dynamic_fields(field):
            return (field.name, field.value_from_object(self), field.get_internal_type())
        return [get_dynamic_fields(field) for field in self.__class__._meta.fields]
