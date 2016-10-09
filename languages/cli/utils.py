from core.cli.utils import Utils as Base
from languages.models import Language
import languages.utils as lang


class Utils(Base):
    def success_language_created(self, language):
        self.success('Created language `%s`' % language.code)

    def error_invalid_language_code(self, code, interactive=False):
        self.invalid("Invalid language code: %s" % code, interactive=False)

    def error_language_already_exists(self, code):
        self.already_exists("Language `%s` already exists" % code)

    def error_language_does_not_exist(self, code):
        self.not_found("Language `%s` does not exists" % code)

    def check_language_code_is_valid(self, code):
        if not lang.code_is_valid(code):
            self.error_invalid_language_code(code)

    def check_language_exists(self, code):
        if not Language.objects.filter(code=code).count():
            self.error_language_does_not_exist(code)

    def check_language_does_not_exist(self, code):
        if Language.objects.filter(code=code).count():
            self.error_language_already_exists(code)

