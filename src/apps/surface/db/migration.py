import os
from django.core.management import execute_from_command_line
from asgiref.sync import sync_to_async


@sync_to_async
def migrate():
    execute_from_command_line([
        os.path.abspath(__file__),
        "makemigrations",
        "surface"
    ])
    execute_from_command_line([
        os.path.abspath(__file__),
        "migrate"
    ])

