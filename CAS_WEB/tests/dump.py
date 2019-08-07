from ..models import *

with open('your.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    # write your header first
    for obj in YourModel.objects.all():
        row = ""
        for field in fields:
             row += getattr(obj, field.name) + ","
        writer.writerow(row)



def buildTestDB():
    user1 = User.objects.create(username='yueqi', first_name='Yue', \
                                    last_name='Qi', password='1234')

    user2 = User.objects.create(username='jingze', fist_name='Ze', )
    self.control1 = Control.objects.create(id=15, cid='yinpan', gid='jingze', \
                                           title='qiyue de yinpan')
    self.project = Project.objects.create(user=self.user, name='my first project')

    self.keywords1 = set('check', 'django', 'link')
    self.cc = ControlConfigure.objects.create(project=self.project, \
                                              control=self.control1, keywords=self.keywords1)