from django.db import models
from utils.snippets import autoslugWithFieldAndUUID
from company.models import Company


@autoslugWithFieldAndUUID(fieldname="name")
class Service(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_services')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=254)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    registration_date = models.DateField()
    due_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
    
    def get_fields(self):
        def get_dynamic_fields(field):
            if field.name == 'company':
                return (field.name, self.company.name, field.get_internal_type())
            else:
                return (field.name, field.value_from_object(self), field.get_internal_type())
        return [get_dynamic_fields(field) for field in self.__class__._meta.fields]
