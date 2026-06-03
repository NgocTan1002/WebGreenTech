import os
from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings

class Command(BaseCommand):
    help = "Loads all PostgreSQL functions from the function/ directory into the database"

    def handle(self, *args, **kwargs):
        functions_dir = os.path.join(settings.BASE_DIR, 'function')
        
        if not os.path.exists(functions_dir):
            self.stdout.write(self.style.ERROR(f"Directory not found: {functions_dir}"))
            return

        sql_files = [f for f in os.listdir(functions_dir) if f.endswith('.sql')]
        sql_files.sort()

        if not sql_files:
            self.stdout.write(self.style.WARNING("No .sql files found in function directory."))
            return

        success_count = 0
        error_count = 0

        with connection.cursor() as cursor:
            for filename in sql_files:
                filepath = os.path.join(functions_dir, filename)
                self.stdout.write(f"Executing {filename}...")
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        sql_content = f.read()
                        cursor.execute(sql_content)
                    self.stdout.write(self.style.SUCCESS(f"  -> Success: {filename}"))
                    success_count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"  -> Error in {filename}: {str(e)}"))
                    error_count += 1

        if error_count == 0:
            self.stdout.write(self.style.SUCCESS(f"\nSuccessfully loaded {success_count} functions."))
        else:
            self.stdout.write(self.style.WARNING(f"\nLoaded {success_count} functions with {error_count} errors."))
