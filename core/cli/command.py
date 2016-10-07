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
    @classmethod
    def register(cls, name, subcmd):
        if not hasattr(cls, 'subcommands'):
            cls.subcommands = {}
        cls.subcommands[name] = subcmd


    def __init__(self, parent=None):
        self.parent = parent
        self.name = self.__class__.name

        # Initialize parser
        if self.parent:
            self.parser = self.parent.subparsers.add_parser(self.name)
        else:
            self.parser = ArgumentParser(description="@TODO")

        self.add_arguments(self.parser)

        # Initialize subcommands
        if hasattr(self.__class__, 'subcommands'):
            self.subparsers = self.parser.add_subparsers(dest=self.subcmds_arg())

            self.subcommands = {}
            for name, klass in self.__class__.subcommands.items():
                cmd = klass(self)
                self.subcommands[name] = cmd


    def subcmds_arg(self):
        cmd, names = self, []
        while cmd.parent:
            names.insert(0, self.name)
            cmd = cmd.parent
        return "_".join(names + ['subcmd'])

    def execute(self, args=None):
        if not args:
            args = self.parser.parse_args()

        if hasattr(self.__class__, 'subcommands'):
            name = getattr(args, self.subcmds_arg())
            if name:
                return self.subcommands[name].execute(args)

        return self.action(args)


    # @abstract
    #   to be implemented by subclasses
    #
    def add_arguments(self, parser):
        pass
    #
    def action(self, args):
        pass
