from ..models import *
from xml.etree import ElementTree as ET
from django.forms.models import model_to_dict
import json
import requests

USERNAME = ''
PASSWORD = ''

# The repository to add this issue to
REPO_OWNER = ''
REPO_NAME = ''

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def parse_report_xml(file, project, report_version):
    report = Report(project=project, version=report_version)
    report.save()

    tree = ET.parse(file)
    root = tree.getroot()

    for bug in root:
        if bug.tag != 'BugInstance':
            continue
        method, location, group, code, severity, message, _ = bug

        location = location[0]
        sourcefile, start_line, end_line = location.find('SourceFile'), \
                                         location.find('StartLine'), location.find('EndLine')

        rule = message.text
        issue = XMLIssue(report=report, sourcefile=sourcefile.text, \
                         startLine=start_line.text, endLine=end_line.text, group=group.text, code=code.text, \
                         severity=severity.text, rule=rule)
        issue.save()

    # create_issues(project, report, report_version)

    return report


def search_issue_xml(controlconfig, report):
    try:
        all_issues = XMLIssue.objects.filter(report=report)
        issues = []
        for issue in all_issues:
            count = 0
            rule = ' '.join(issue.rule)
            for word in rule.strip('.').split(' '):
                if word in controlconfig.keywords:
                    count += 1
                if count == 1:
                    dict_issue = model_to_dict(issue, fields=['severity', 'sourcefile', 'startLine', 'endLine', 'code', 'group'])
                    dict_issue['rule'] = rule
                    dict_issue['created_time'] = issue.created_time
                    issues.append(dict_issue)
                    break
    except XMLIssue.DoesNotExist:
        issues = []

    return issues


def create_issues(project, report, report_version):
    # issues = {}
    try:
        controlconfigs = ControlConfigure.objects.filter(project=project)
        issues = {}
        for controlconfig in controlconfigs:
            issues_tmp = search_issue_xml(controlconfig, report)
            if len(issues_tmp) > 0:
                issues[controlconfig.control.cid] = {
                    "title": controlconfig.control.title,
                    "items": issues_tmp,
                    "length": len(issues_tmp),
                }
    except ControlConfigure.DoesNotExist:
        issues = {}

    if len(issues) > 0:
        # build issue body string
        body = ""
        for cid, issue in issues.items():
            body += color.BOLD
            body += (cid + ": ")
            body += issue["title"]
            body += color.END
            body += "\n"

            for item in issue["items"]:
                for col, msg in item.items():
                    body += (col + ": ")
                    body += ("{}\n".format(msg))
                body += "\n"

            body += "\n\n"

        make_github_issue("Project " + project.name + " Pipeline Test", body)


def make_github_issue(title, body=None):
    '''Create an issue on github.com using the given parameters.'''
    # Our url to create issues via POST
    url = 'https://api.github.com/repos/%s/%s/issues' % (REPO_OWNER, REPO_NAME)
    # Create an authenticated session to create the issue
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    # Create our issue
    issue = {'title': title,
             'body': body
             }
    # Add the issue to our repository
    r = session.post(url, json.dumps(issue))
    if r.status_code == 201:
        print("Successfully created Issue :", title)
    else:
        print("Could not create Issue :", title)
        print("Response: ", r.content)