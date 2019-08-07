from django.test import TestCase, Client
import unittest
from cas.models import *

class LoginTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        # self.client.login(username="yueqi", password="yueqi")
        # self.credentials = {
        #     'username': 'yueqi',
        #     'password': 'yueqi'}
        # User.objects.create_user(**self.credentials)
        user = User.objects.create_user(username='username', password='password')
        self.client.login(username='username', password='password')

    def test_login_get(self):
        # Issue a GET request.
        response = self.client.get('/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'cas/login.html')

    # def test_login_valid(self):
    #     # Issue a GET request.
    #     # response = self.client.post('/', {'username': 'yueqi', 'password': 'yueqi'})
    #
    #     response = self.client.post('/', **self.credentials)
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(response.context['user'].is_active)


        # self.assertTemplateUsed(response, 'cas/projects.html')


    # def test_login_invalid(self):
    #     # Issue a GET request.
    #     response = self.client.post('/', {'username': 'yueqi', 'password': 'wrong'})
    #
    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)


    def test_projects(self):
        # Issue a GET request.
        # response = self.client.post('/', {'username': 'yueqi', 'password': 'yueqi'})

        response = self.client.post('/projects')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cas/projects.html')

    def test_config_project(self):
        # Issue a GET request.
        # response = self.client.post('/', {'username': 'yueqi', 'password': 'yueqi'})

        response = self.client.post('/config_project',{'id':'1'})

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cas/projects.html')

