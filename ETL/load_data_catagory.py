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
input_catalog = input_dir + "NIST_SP-800-53_rev4_catalog-min.json"
input_high = input_dir + "NIST_SP-800-53_rev4_HIGH-baseline_profile-min.json"
input_moderate = input_dir + "NIST_SP-800-53_rev4_MODERATE-baseline_profile-min.json"
input_low = input_dir + "NIST_SP-800-53_rev4_LOW-baseline_profile-min.json"


def get_controller_priority(input_file):
    ids_res = set()
    with open(input_file, 'r') as f:
        controllers_data = json.load(f)
        ids = controllers_data['profile']['imports'][0]['include']['id-selectors']
        for item in ids:
            id = item.get('control-id', item.get('subcontrol-id'))
            ids_res.add(id)
    return ids_res


controllers_high = get_controller_priority(input_high)
controllers_moderate = get_controller_priority(input_moderate)
controllers_low = get_controller_priority(input_low)

with open(input_catalog, 'r') as fin:
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
            high = cid in controllers_high
            moderate = cid in controllers_moderate
            low = cid in controllers_low
            subcontrollers = controller.get('subcontrols', [])
            for sid in subcontrollers:
                subcontrol = subcontrollers[sid]
                subcontrol['pid'] = cid
                dq.append(subcontrol)
            insert_controller_query = db.insert(controllers_table)\
                .values(cid=cid, gid=gid, title=ctitle, pid=pid,
                        parameters=params, properties=props,
                        links=links, parts=parts, classinfo=classinfo,
                        high=high, moderate=moderate, low=low)
            ICResProxy = connection.execute(insert_controller_query)
