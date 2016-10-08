from qiq.test import TestCase


class TestFakeCommand(TestCase):
    def test_fake(self):
        self.qiq('manage', 'fake', '1')
