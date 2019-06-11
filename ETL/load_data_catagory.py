import sqlalchemy as db
import psycopg2
import json
import collections

engine = db.create_engine('postgresql://cats:miao@54.162.139.224:5432/cats')
connection = engine.connect()
metadata = db.MetaData()
groups_table = db.Table('groups', metadata, autoload=True, autoload_with=engine)
controllers_table = db.Table('controllers', metadata, autoload=True, autoload_with=engine)

input_dir = "/home/ubuntu/CAtS/ETL/nist80053_rev4/"
input_file = input_dir + "NIST_SP-800-53_rev4_catalog-min.json"

with open(input_file, 'r') as fin:
    data = json.load(fin)
    controller_groups = data['catalog']['groups']
    for group in controller_groups:
        gid = group.get('id')
        gtitle = group.get('title')
        insert_group_query = db.insert(groups_table).values(gid=gid, title=gtitle)
        IGResProxy = connection.execute(insert_group_query)
        controllers = group['controls']
        dq = collections.deque(controllers)
        while len(dq) > 0:
            controller = dq.popleft()
            cid = controller.get('id')
            classinfo = controller.get('class', None)
            ctitle = controller.get('title')
            params = controller.get('parameters', None)
            props = controller.get('properties', None)
            links = controller.get('links', None)
            parts = controller.get('parts', None)
            pid = controller.get('pid', None)
            subcontrollers = controller.get('subcontrols', [])
            for sid in subcontrollers:
                subcontrol = subcontrollers[sid]
                subcontrol['pid'] = cid
                dq.append(subcontrol)
            insert_controller_query = db.insert(controllers_table)\
                .values(cid=cid, gid=gid, title=ctitle, pid=pid,
                        parameters=params, properties=props,
                        links=links, parts=parts, classinfo=classinfo)
            ICResProxy = connection.execute(insert_controller_query)
