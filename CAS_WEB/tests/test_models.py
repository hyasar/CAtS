from django.test import TestCase
from cas.models import *
import datetime


# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        self.users = build_test_users('./tests/resource/Test_Users.csv')

    def test_User(self):
        """Animals that can speak are correctly identified"""
        with open('./tests/resource/Test_Users.csv') as f:
            user_data = f.readlines()
        f.close()
        user_data = user_data[1:]

        for i in range(len(self.users)):
            user = self.users[i]
            username, first_name, last_name, email, password = user_data[i].split(',')

            self.assertTrue(isinstance(user, User))
            self.assertEqual(user.username, username)
            self.assertEqual(user.first_name, first_name)
            self.assertEqual(user.last_name, last_name)
            self.assertEqual(user.email, email)


class ProjectTestCase(TestCase):
    def setUp(self):
        self.users = build_test_users('./tests/resource/Test_Users.csv')
        self.projects = build_test_projects('./tests/resource/Test_Projects.csv', self.users)

    def test_project(self):
        with open('./tests/resource/Test_Projects.csv') as f:
            project_data = f.readlines()
        f.close()
        project_data = project_data[1:]

        for i in range(len(self.projects)):
            project = self.projects[i]
            name, description, index = project_data[i].split(',')

            self.assertTrue(isinstance(project, Project))
            self.assertEqual(project.name, name)
            self.assertEqual(project.description, description)
            self.assertEqual(project.user, self.users[int(index)])


def build_test_users(user_file):
    with open(user_file) as f:
        user_data = f.readlines()
    f.close()
    user_data = user_data[1:]

    users = []
    for i in user_data:
        username, first_name, last_name, email, password = i.split(',')
        user = User.objects.create_user(username=username,
                                        password=password,
                                        email=email,
                                        first_name=first_name,
                                        last_name=last_name)
        users.append(user)
    return users


def build_test_projects(project_file, users):
    with open(project_file) as f:
        project_data = f.readlines()
    f.close()
    project_data = project_data[1:]

    projects = []
    for i in project_data:
        name, description, index = i.split(',')
        user = users[int(index)]
        project = Project(name=name, description=description, user=user,
                          created_time=datetime.datetime.now(), \
                          updated_time=datetime.datetime.now())
        projects.append(project)

    return projects


# def buildTestControls(control_file):
#     with open(control_file) as f:
#         control_data = f.readlines()
#     f.close()
#
#     controls = []
#     for i in control_data:
#         cid, gid, title, parameters, properties, links, parts, \
#         class_info, pid, high, moderate, low, iid = i
#
#         control = Control(id=iid, cid=cid, gid=gid, title=title, \
#                           parameters=parameters, properties=properties, \
#                           links=links, parts=parts, class_info=class_info, \
#                           pid=pid, high=high, moderate=moderate, low=low)
#
#         # control.save()
#         controls.append(control)
#
#     return controls
