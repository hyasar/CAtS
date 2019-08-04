from ..models import *
import re
from django.core import serializers

COMA_SPACE = re.compile('[,|\\s|_]')
REX = re.compile('[^a-z0-9]+')

def parseReport(csv_file, project, report_version):

    report = Report(project=project, report_version=report_version)
    report.save()

    with open(csv_file, 'r') as f:
        data = f.readlines()
    f.close()

    data = data[1:]

    for i in data:
        _, issue_id, created_time, updated_time, severity, \
        status, cwe, raw_rule, tool, location, element, \
        path, line = i.strip('\n').split(',')

        raw_rules = re.split(COMA_SPACE, raw_rule)
        rule = set()
        for j in raw_rules:
            temp = REX.sub("", j.lower())
            rule.add(temp)

        issue = CSVIssue(report=report, created_time=created_time, \
                         updated_time=updated_time, severity=severity, \
                         status=status, cwe=cwe, rule=rule, tool=tool, \
                         location=location, element=element, path=path, \
                         line=line)
        issue.save()

    return report


def searchIssue(ControlConfigure, report):
    all_issues = CSVIssue.objects.filter(report=report)

    issues = []
    for issue in all_issues:
        count = 0
        for word in issue.rule:
            if word in ControlConfigure.keywords:
                count += 1
            if count == 3:
                issue_json = serializers.serialize('json', issue)
                issues.append(issue_json)
                break

    return issues
