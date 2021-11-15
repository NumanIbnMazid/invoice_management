from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import os
from django.conf import settings
from dotenv import load_dotenv

env_path = os.path.join(settings.BASE_DIR, ".env")
load_dotenv(dotenv_path=env_path)


class Command(BaseCommand):

    def handle(self, *args, **options):
        
        print('Creating superuser admin account...')
        
        if not get_user_model().objects.filter(
            email=os.environ.get('DJANGO_SU_EMAIL')
        ).exists():
            get_user_model().objects.create_superuser(
                email=os.environ.get('DJANGO_SU_EMAIL'),
                username=os.environ.get('DJANGO_SU_NAME'),
                password=os.environ.get('DJANGO_SU_PASSWORD')
            )
        else:
            print(f"Admin ({os.environ.get('DJANGO_SU_EMAIL')}) already exists!")
