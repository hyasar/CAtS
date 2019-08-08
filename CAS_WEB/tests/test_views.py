from django.test import TestCase, Client
from cas.models import *
from django.utils.encoding import force_text


class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username='yueqi', password='yueqi')

    def test_login_get(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cas/login.html')

    def test_get_project_list(self):
        response = self.client.get('/projects')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cas/projects.html')

    def test_get_project_configuration(self):
        response = self.client.get('/config_project', {'id': 3})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cas/config_project.html')

    def test_get_project_controls(self):
        response = self.client.get('/get_project_controlls', {'id': 3})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(force_text(response.content),
                             {"controls":
                                  [{"cid": "ac-1", "id": 1, "title": "Access Control Policy and Procedures", "keywords": "access,accessor,field,private"},
                                   {"cid": "ac-2", "id": 2, "title": "Account Management", "keywords": "account"},
                                   {"cid": "ac-6", "id": 6, "title": "Least Privilege", "keywords": "privilege"}
                                   ]
                              })

    def test_create_project_get(self):
        response = self.client.get('/new_project')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cas/new_project.html')

    # def test_create_project_post(self):
    #     response = self.client.post('/new_project', {"name": "test_create_project", "description": "it is a test for creating new projects in cas"})
    #     self.assertEqual(response.status_code, 200)
    #     print("location: ", response["location"])

