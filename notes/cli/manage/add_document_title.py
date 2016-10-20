from .document_tasks import DocumentTasks
from core.cli.management.field_task import FieldTask, field_task


@field_task('title', DocumentTasks)
class AddDocumentTitle(FieldTask):
    description = "Complete document's title"

    @classmethod
    def check(cls, doc):
        if not doc.description:
            return cls(doc)


    def __init__(self, doc):
        self.document = doc

    def perform(self):
        # @fixme interactions
        title = input("Enter a title for `%s`  (pass) " % self.document.full_name())
        if title:
            self.document.description = title
            self.document.save()
