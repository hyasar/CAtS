from ..models import *
from xml.etree import ElementTree as ET
from django.forms.models import model_to_dict


def parse_report_xml(file, project, report_version):
    report = Report(project=project, version=report_version)
    report.save()

    #tree = ET.parse(file)
    #root = tree.getroot()
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
