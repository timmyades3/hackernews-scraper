import os
import sys
from subprocess import Popen

def run_celery():
    celery_worker = Popen(["celery", "-A", "core", "worker", "--pool=solo --loglevel=info"])
    celery_beat = Popen(["celery", "-A", "core", "beat", "--loglevel=info"])
    return celery_worker, celery_beat

if __name__ == "__main__":
    if "runserver" in sys.argv:
        run_celery()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

#!/usr/bin/env python
# """Django's command-line utility for administrative tasks."""
# import os
# import sys


# def main():
#     """Run administrative tasks."""
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc
#     execute_from_command_line(sys.argv)


# if __name__ == '__main__':
#     main()
