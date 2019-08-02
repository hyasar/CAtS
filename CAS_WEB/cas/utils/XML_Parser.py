from ..models import *
from xml.etree import ElementTree as ET

def parseReportXML(csv_file, project, report_version):

    report = Report(project=project, report_version=report_version)
    report.save()

    tree = ET.parse('test.xml')
    root = tree.getroot()

    date_info = root.attrib['package_version']
    date = date_info[13:23]

    for bug in root:
        method, location, group, code, severity, message, _ = bug
        location = location[0]
        sourcefile, startLine, endLine = location.find('SourceFile'), \
                                         location.find('StartLine'), location.find('EndLine')

        rule = message.text.strip('.').split(' ')
        issue = XMLIssue(report=report, version=report_version, created_time=date, sourcefile=sourcefile.text, \
                         startLine=startLine.text, endLine=endLine.text, group=group.text, code=code.text, \
                         severity=severity.text, rule=rule)
        issue.save()

    return report


def searchIssueXML(ControlConfigure, version):
    target_report = Report.objects.filter(project=ControlConfigure.project, version=version)
    all_issues = Issue.objects.filter(report=target_report)

    issues = []
    for issue in all_issues:
        count = 0
        for word in issue.rule:
            if word in ControlConfigure.keywords:
                count += 1
            if count == 3:
                issue.controls.add(ControlConfigure.control)
                issues.append(issue)
                break

    return issues