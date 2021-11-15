from django.db import models
from utils.snippets import autoslugWithFieldAndUUID
from django.contrib.auth import get_user_model
from utils.image_upload_helpers import upload_company_logo_image_path


@autoslugWithFieldAndUUID(fieldname='name')
class Company(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='company')
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, max_length=254)
    logo = models.ImageField(upload_to=upload_company_logo_image_path, null=True, blank=True)
    registration_date = models.DateField()
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
    
    def get_fields(self):
        def get_dynamic_fields(field):
            if field.name == 'user':
                return (field.name, self.user.get_dynamic_username(), field.get_internal_type())
            else:
                return (field.name, field.value_from_object(self), field.get_internal_type())
        return [get_dynamic_fields(field) for field in self.__class__._meta.fields]
