from PIL.ImageShow import Viewer
from django.test import TestCase


class TestViewer(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('setUpTestData')

    def setUp(self):
        self.viewer = Viewer()
        print('setUp')
