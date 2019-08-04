from django.test import TestCase
from ..models import *

# Create your tests here.
class ControlConfigureTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='yueqi', first_name='Yue', \
                                   last_name='Qi', password='1234')
        self.control1 = Control.objects.create(id=15, cid='yinpan', gid='jingze', \
                                          title='qiyue de yinpan')
        self.project = Project.objects.create(user=self.user, name='my first project')

        self.keywords1 = set('check', 'django', 'link')
        self.cc = ControlConfigure.objects.create(project=self.project, \
                                                  control=self.control1, keywords=self.keywords1)

    def test_Control_configure(self):
        """Animals that can speak are correctly identified"""
        project_check = self.cc.project
        self.assertIn(project_check.name, 'my first project')
