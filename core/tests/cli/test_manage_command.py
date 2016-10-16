from qiq.test import TestCase


class ManageCommand(TestCase):
    def test_created(self):
        self.assert_success('project', 'new', 'bougle')
        self.assert_success('manage')
