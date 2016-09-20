from cli.management.commands._subcommand import Subcommand


class ModifyCommand(Subcommand):
    def add_arguments(self, parser):
        parser.add_argument('name_or_id', type=str, help='the name or the id of the document')
        parser.add_argument('-d', '--description', type=str,
                            help='the description of the document')
        parser.add_argument('-n', '--new-name', type=str,
                            help='the new name of the document')

    def execute(self, args, options):
        name_or_id = options['name_or_id']
        doc = self.find_document_by_name_or_id_or_error(name_or_id)

        old_name, desc_mod = None, None

        new_name = options['new_name']
        if new_name and new_name != doc.name:
            self.check_document_name_is_valid(new_name)
            old_name = doc.name
            doc.name = new_name

        desc = options['description']
        if desc and desc != doc.description:
            desc_mod = True
            doc.description = desc

        if old_name or desc_mod:
            doc.save()
            self.success_document_modified(doc, old_name, desc_mod)
        else:
            self.warning_nothing_to_do()
