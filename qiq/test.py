import django
from django.core.management import call_command
from io import StringIO
from core.cli.commands.qiq import QiqCommand
from qiq.common import SUCCESS, INVALID, EXISTS, NOT_FOUND
from io import StringIO
import tempfile



class TestCase(django.test.TestCase):
    def assert_status(self, sts, *cmd):
        try:
            out = StringIO()
            call_command(*cmd, stdout=out)
        except SystemExit as err:
            self.assertEqual(sts, err.code)

    def qiq(self, *cmd):
        try:
            cmd = [str(x) for x in cmd]
            QiqCommand(stdout=StringIO()).execute(test=cmd)
        except SystemExit as err:
            return err.code
        return 0

    def assert_success(self, *cmd):
        self.assertEqual(SUCCESS, self.qiq(*cmd))

    def assert_exists(self, *cmd):
        self.assertEqual(EXISTS, self.qiq(*cmd))

    def assert_invalid(self, *cmd):
        self.assertEqual(INVALID, self.qiq(*cmd))

    def assert_not_found(self, *cmd):
        self.assertEqual(NOT_FOUND, self.qiq(*cmd))

    def dummy_file(self, text='abc'):
        _, path = tempfile.mkstemp()
        with open(path, 'w') as f:
            f.write(text)
        return path
