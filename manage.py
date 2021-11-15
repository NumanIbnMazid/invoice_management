#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv
from pathlib import Path

""" *** Read Project Environment File *** """
BASE_DIR = Path(__file__).resolve().parent
env_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=env_path)


def main():
    """Run administrative tasks."""
    if eval(str(os.environ.get('IS_PRODUCTION'))):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
    elif eval(str(os.environ.get('IS_STAGING'))):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.staging')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
        
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
