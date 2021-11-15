from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.http import Http404
from utils.snippets import autoslugFromUUID, generate_unique_username_from_email


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            last_login=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def all(self):
        return self.get_queryset()

    def get_by_id(self, id):
        try:
            instance = self.get_queryset().get(id=id)
        except User.DoesNotExist:
            raise Http404("User Not Found!")
        except User.MultipleObjectsReturned:
            qs = self.get_queryset().filter(id=id)
            instance = qs.first()
        except:
            raise Http404("Something went wrong!")
        return instance

    def get_by_slug(self, slug):
        try:
            instance = self.get_queryset().get(slug=slug)
        except User.DoesNotExist:
            raise Http404("User Not Found!")
        except User.MultipleObjectsReturned:
            qs = self.get_queryset().filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404("Something went wrong!")
        return instance


@autoslugFromUUID()
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=254, unique=True)
    """ Additional Fields Starts """
    name = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=254)
    updated_at = models.DateTimeField(auto_now=True)
    is_company = models.BooleanField(default=False)
    """ Additional Fields Ends """
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = ("User")
        verbose_name_plural = ("Users")
        ordering = ["-date_joined"]

    def get_absolute_url(self):
        return f"/users/{self.get_dynamic_username()}-{self.slug}/"

    # def get_absolute_url(self):
    #     return reverse("profile_details", kwargs={"slug": self.slug})

    def __str__(self):
        return self.get_dynamic_username()

    def get_dynamic_username(self):
        """ Get a dynamic username for a specific user instance. if the user has a name then returns the name, if the user does not have a name but has a username then return username, otherwise returns email as username """
        if not self.name == None and not self.name == "":
            return self.name
        elif not self.username == None and not self.username == "":
            return self.username
        return self.email


@receiver(pre_save, sender=User)
def update_username_from_email(sender, instance, **kwargs):
    """ Generates and updates username from user email on User pre_save hook """
    instance.username = generate_unique_username_from_email(instance=instance)
