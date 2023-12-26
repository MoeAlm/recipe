"""
Django command to wait for the database to be available.
"""
import time

from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for the command."""

        # Inform the user that the command is waiting for the database
        self.stdout.write('Waiting for the database...')

        # Flag to track whether the database is up
        db_up = False

        # Continue looping until the database is up
        while db_up is False:
            try:
                # Attempt to check the database, using the check method
                self.check(databases=['default'])
                # If successful, set the flag to True to exit the loop
                db_up = True
            except (Psycopg2Error, OperationalError):
                # If an exception is caught (indicating the database is unavailable),
                # inform the user and wait for 1 second before retrying
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        # Once the loop exits, inform the user that the database is available
        self.stdout.write(self.style.SUCCESS('Database available!'))
