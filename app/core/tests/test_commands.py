"""
Test custom Django management commands.
"""

# Importing necessary modules and classes for testing
from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# Patching the 'check' method in the 'wait_for_db.Command' class
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    # Test case for when the database is ready
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database is ready."""
        # Mocking the 'check' method to return True
        patched_check.return_value = True

        # Calling the 'wait_for_db' management command
        call_command('wait_for_db')

        # Asserting that the 'check' method was called once with the default database
        patched_check.assert_called_once_with(databases=['default'])

    # Test case for waiting for the database with delays due to OperationalErrors
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        # Setting up the side effect for 'check' method:
        # - First two calls raise Psycopg2Error
        # - Next three calls raise Django OperationalError
        # - Last call returns True to simulate success
        patched_check.side_effect = ([Psycopg2Error] * 2 +
                                     [OperationalError] * 3 + [True])

        # Calling the 'wait_for_db' management command
        call_command('wait_for_db')

        # Asserting that the 'check' method was called a total of 6 times
        self.assertEqual(patched_check.call_count, 6)

        # Asserting that the 'check' method was called with the default database
        patched_check.assert_called_with(databases=['default'])
