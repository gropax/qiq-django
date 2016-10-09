import sys
from termcolor import colored
from qiq.common import SUCCESS, INVALID, EXISTS, NOT_FOUND, NOT_IMPLEMENTED
from core.cli.config import read_config_file


class Utils(object):
    def config(self):
        if not hasattr(self, '_config'):
            self._config = read_config_file()
        return self._config


    def ask(self, msg, default='yes'):
        while True:
            ans = input('%s (%s) ' % (msg, default))
            if ans == '':
                return True if default == 'yes' else False
            elif ans.lower() in ['y', 'ye', 'yes']:
                return True
            elif ans.lower() in ['n', 'no']:
                return False
            else:
                self.error("Invalid answer")


    def success(self, msg, interactive=False):
        msg = colored(msg.strip(), 'green', attrs=['bold'])
        self.stdout.write(msg + "\n")
        if not interactive:
            sys.exit(SUCCESS)

    def warning(self, msg, interactive=False):
        msg = colored(msg.strip(), 'yellow', attrs=['bold'])
        self.stdout.write(msg + "\n")
        if not interactive:
            sys.exit(SUCCESS)

    def error(self, msg, code, interactive=False):
        msg = colored(msg.strip(), 'red', attrs=['bold'])
        self.stdout.write(msg + "\n")
        if not interactive:
            sys.exit(code)

    def not_found(self, msg):
        self.error(msg, NOT_FOUND)

    def already_exists(self, msg):
        self.error(msg, EXISTS)

    def invalid(self, msg, interactive=False):
        self.error(msg, INVALID, interactive)

    def not_implemented(self):
        msg = colored('Not implemented', 'magenta', attrs=['bold'])
        self.stdout.write(msg + "\n")
        sys.exit(NOT_IMPLEMENTED)


    def error_no_match(self):
        self.not_found("No match")

    def warning_nothing_to_do(self):
        self.warning("Nothing to do")

    def warning_operation_aborted(self):
        self.warning("Operation aborted")
