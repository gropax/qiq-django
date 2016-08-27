import django
from django.core.management import call_command
from io import StringIO


class TestCase(django.test.TestCase):
    def assert_status(self, sts, *cmd):
        try:
            out = StringIO()
            call_command(*cmd, stdout=out)
        except SystemExit as err:
            self.assertEqual(sts, err.code)
