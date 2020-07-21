from ..models import *
from xml.etree import ElementTree as ET
from django.forms.models import model_to_dict
import json
import requests

def parse_report_xml(file, project, report_version):
    report = Report(project=project, version=report_version)
    report.save()

    root = ET.fromstring(file)

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


def create_issues(project, report, report_version, username, password, reponame):

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
            
            body += (cid + ": ")
            body += issue["title"]
    
            body += "\n--------------------------------------------------\n"

            for item in issue["items"]:
                for col, msg in item.items():
                    body += ("**" + col + ":** ")
                    body += ("{}\n".format(msg))
                body += "\n"

            body += "\n\n"

        make_github_issue("Project " + project.name + " Pipeline Test", username, password, reponame, body)


def make_github_issue(title, user_name, pass_word, repo_name, body=None):
    '''Create an issue on github.com using the given parameters.'''
    # Our url to create issues via POST
    url = 'https://api.github.com/repos/%s/%s/issues' % (user_name, repo_name)
    # Create an authenticated session to create the issue
    session = requests.Session()
    session.auth = (user_name, pass_word)
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