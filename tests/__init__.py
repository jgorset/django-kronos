from django.core.management import setup_environ
from django.test.utils import setup_test_environment
from project import settings

setup_environ(settings)
setup_test_environment()
