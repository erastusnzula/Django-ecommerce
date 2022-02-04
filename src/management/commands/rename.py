import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Renames Django Project."

    def add_arguments(self, parser):
        parser.add_argument('current', type=str, nargs='+', help='The current Django project name')
        parser.add_argument('new_project_name', type=str, nargs='+', help='The new Django Project name.')

    def handle(self, *args, **kwargs):
        current_project_name = kwargs['current'][0]
        new_project_name = kwargs['new_project_name'][0]

        # Renaming files
        files_to_rename = [f'{current_project_name}/settings.py', f'{current_project_name}/wsgi.py', 'manage.py']

        for f in files_to_rename:
            with open(f, 'r') as file:
                file_data = file.read()
            file_data = file_data.replace(current_project_name, new_project_name)

            with open(f, 'w') as file:
                file.write(file_data)

        os.rename(current_project_name, new_project_name)
        self.stdout.write(self.style.SUCCESS(f'Successfully renamed to {new_project_name}'))
