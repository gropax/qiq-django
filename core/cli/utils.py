import sys
from termcolor import colored
from qiq.common import SUCCESS, INVALID, EXISTS, NOT_FOUND


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


    def success(self, string, interactive=False):
        self.stdout.write(colored(string, 'green', attrs=['bold']))
        if not interactive:
            sys.exit(SUCCESS)

    def warning(self, string, interactive=False):
        self.stdout.write(colored(string, 'yellow', attrs=['bold']))
        if not interactive:
            sys.exit(SUCCESS)

    def error(self, string, code, interactive=False):
        self.stdout.write(colored(string, 'red', attrs=['bold']))
        if not interactive:
            sys.exit(code)

    def not_found(self, string):
        self.error(string, NOT_FOUND)

    def already_exists(self, string):
        self.error(string, EXISTS)

    def invalid(self, string, interactive=False):
        self.error(string, INVALID, interactive)


    def error_no_match(self):
        self.not_found("No match")

    def warning_nothing_to_do(self):
        self.warning("Nothing to do")

    def warning_operation_aborted(self):
        self.warning("Operation aborted")
