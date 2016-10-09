import sys
from argparse import ArgumentParser


# @decorator to register a sub command
#
def command(name, parent=None):
    def decorator(cls):
        cls.name = name
        if parent:
            parent.register(name, cls)
        return cls
    return decorator


class Command(object):

    aliases = []

    @classmethod
    def register(cls, name, subcmd):
        if not hasattr(cls, 'subcommands'):
            cls.subcommands = {}
        cls.subcommands[name] = subcmd


    def __init__(self, parent=None, stdout=sys.stdout):
        self.parent = parent
        self.stdout = stdout
        self.name = self.__class__.name

        # Initialize parser
        if self.parent:
            self.parser = self.parent.subparsers.add_parser(self.name,
                                                            aliases=self.__class__.aliases)
        else:
            self.parser = ArgumentParser(description="@TODO")

        self.add_arguments(self.parser)

        # Initialize subcommands
        if hasattr(self.__class__, 'subcommands'):
            self.subparsers = self.parser.add_subparsers(dest=self.subcmds_arg())

            self.subcommands = {}
            for name, klass in self.__class__.subcommands.items():
                cmd = klass(parent=self, stdout=self.stdout)
                self.subcommands[name] = cmd


    def subcmds_arg(self):
        cmd, names = self, []
        while cmd.parent:
            names.insert(0, cmd.name)
            cmd = cmd.parent
        return "_".join(names + ['subcmd'])

    def execute(self, args=None, test=None):
        if not args:
            if test:
                args = self.parser.parse_args(test)
            else:
                args = self.parser.parse_args()

        if hasattr(self.__class__, 'subcommands'):
            name = getattr(args, self.subcmds_arg())
            if name:
                #print(args)
                return self.find_subcommand(name).execute(args)

        return self.action(args)

    def find_subcommand(self, name):
        if name in self.subcommands:
            return self.subcommands[name]
        else:
            for cmd in self.subcommands.values():
                if name in cmd.aliases:
                    return cmd


    # @abstract
    #   to be implemented by subclasses
    #
    def add_arguments(self, parser):
        pass
    #
    # The default behaviour if action is not specified is printing help.
    #
    def action(self, args):
        self.parser.print_help()
