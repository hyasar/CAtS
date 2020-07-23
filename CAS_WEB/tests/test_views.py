from django.test import TestCase, Client
from cas.models import *
from django.utils.encoding import force_text
import json

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
        response = self.client.get('/projects', {"page":"2"})
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
                               {"cid": "ac-2", "id": 2, "title": "Account Management",
                                   "keywords": "account"},
                               {"cid": "ac-6", "id": 6, "title": "Least Privilege",
                                   "keywords": "privilege"}
                               ]
                              })

    def test_create_project_get(self):
        response = self.client.get('/new_project')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cas/new_project.html')

    def test_create_project_post(self):
        response = self.client.post(
            '/new_project', {"name": "test_create_project", "description": "it is a test for creating new projects in cas"})
        self.assertEqual(response.status_code, 302)
        # self.assertRedirects(response, '/config_project?id=')

    def test_search_projects(self):
        response = self.client.get('/search_projects', {"name": "pet"})
        self.assertEqual(response.status_code, 200)

    def test_search_controls(self):
        response = self.client.get('/controls', {"page": "2"})
        self.assertEqual(response.status_code, 200)

    def test_get_control_by_id(self):
        response = self.client.get('/get_control_by_id', {"id": "2"})
        self.assertEqual(response.status_code, 200)

    def test_search_controls_by_name(self):
        response = self.client.get('/searchControls', {"key": "Access"})
        self.assertEqual(response.status_code, 200)

    def test_update_project_get(self):
        response = self.client.get('/update/4/')
        self.assertEqual(response.status_code, 200)

    def test_update_project_post(self):
        response = self.client.post(
            '/update/4/', {"name": "CAtS", "description": "updated description"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/projects')

    def test_delete(self):
        response = self.client.post('/delete', {"project_id": "4"})
        self.assertEqual(response.status_code, 200)

    def test_setcontrols(self):
        controls_dict = {
            "id": "2",
            "controlconfigs":
            [
                {"id": "1", "keywords": "access,accessor,field,private"},
                {"id": "2", "keywords": "account"},
                {"id": "6", "keywords": "privilege"}
            ]}
        response = self.client.post('/setcontrols',json.dumps(controls_dict), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_project_dashboard(self):
        response = self.client.get('/project_dashboard', {"id": "3"})
        self.assertEqual(response.status_code, 200)

    def test_parse_report(self):
        with open('tests/resource/Assessment-petclinic-build-3-date-2019-07-13-22-01-04-Ubuntu_16.04_64-bit-checkstyle.xml') as fp:
            response = self.client.post(
                '/parse_report', {"username": "yueqi", "password": "yueqi", "projectId" : "3" , "buildNumber" : "97", "testingReport" : fp})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.content), "b'Report parsed successfully'")

    def test_get_controlconfig_by_id(self):
        response = self.client.get('/get_controlconfig_by_id', {"project_id": "3", "control_id": "1"})
        self.assertEqual(response.status_code, 200)


    def test_logout(self):
        response = self.client.get('/logout')
        self.assertRedirects(response, '/')
    
    def test_get_issues_not_exist(self):
        response = self.client.get('/get_issues', {"report_id" : "-1", "project_id":"3"})
        self.assertEqual(response.status_code, 404)
    
    def test_get_issues(self):
        response = self.client.get('/get_issues', {"report_id" : "19", "project_id":"3"})
        self.assertEqual(response.status_code, 200)

    def test_get_profile(self):
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cas/profile.html')

    def test_get_setting(self):
        response = self.client.get('/setting')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cas/setting.html')

    def test_change_ps_get(self):
        response = self.client.get('/change_password/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cas/change_password.html')

    def test_change_ps_post(self):
        response = self.client.post('/change_password/1/', {"password": "newpswd"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/projects')

        response = self.client.post('/change_password/1/', {"password": "yueqi"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/projects')

    def test_update_profile_get(self):
        response = self.client.get('/update_profile')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cas/update_profile.html')

    def test_update_profile_post(self):
        response = self.client.post('/update_profile', 
            {"firstName": "newFN", "lastName": "newLN", "email": "new@new.com"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/profile')

        response = self.client.post('/update_profile', 
            {"firstName": "Yue", "lastName": "Qi", "email": "qyigakki@gmail.com"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/profile')

    def test_get_shared_pj_list(self):
        response = self.client.get('/shared_projects')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cas/shared_projects.html')

    def test_share_pj_get(self):
        response = self.client.get('/share_project/3/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cas/share.html')

    def test_stop_share_get(self):
        response = self.client.get('/stop_share_project/3/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cas/share.html')

    def test_share_and_stop_share_pj_post(self):
        response = self.client.post('/share_project/3/', 
            {"newSharedUser": "xiaotong"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cas/share.html')

        response = self.client.post('/stop_share_project/3/', 
            {"stopSharedUser": "xiaotong"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cas/share.html')

    def test_get_id_from_name(self):
        response = self.client.get('/get_id_by_name', 
            {"name": "xiaotong"})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(force_text(response.content),
                             {"name": "xiaotong", "id": 4})

    def test_get_name_from_id(self):
        response = self.client.get('/get_name_by_id', 
            {"id": 4})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(force_text(response.content),
                             {"name": "xiaotong", "id": '4'})

    def test_get_details(self):
        response = self.client.get('/detail', {'rid': 19, 'pid': 3})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cas/report_detail.html')

    def test_enter_credentials_get(self):
        response = self.client.get('/enter_credential', {'rid': 19, 'pid': 3})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cas/enter_credential.html')
