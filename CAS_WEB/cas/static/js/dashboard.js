const url = new URL(window.location.href);
const query = new URLSearchParams(url.search);

class Reports extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            pid: query.get("id"),
            reports: [],
            selectedReportId: -1,
            issues: {}
        };
    }

    componentDidMount() {
        this.loadReports();
    }

    loadReports = () => {
        fetch("/get_reports?id=" + query.get('id'))
            .then(res => res.json())
            .then(
                (result) => {
                    let newReport = -1;
                    let reports = result.reports;
                    if (reports.length > 0) {
                        newReport = reports[0].id
                    }
                    this.setState({
                        reports: reports,
                        selectedReportId: newReport
                    });
                    this.loadIssues(newReport)
                },
                (error) => {
                    this.setState({
                        error
                    });
                }
            )
    }

    loadIssues(report_id) {
        fetch("/get_issues?project_id=" + query.get("id") + "&report_id=" + report_id)
            .then(res => res.json())
            .then(
                (result) => {
                    let newIssues = []
                    for (let cid in result.issues) {
                        let issuelst = result.issues[cid]
                        for (let issue of issuelst) {
                            issue.cid = cid
                            newIssues.push(issue)
                        }
                    }
                    this.setState({
                        issues: newIssues,
                    });
                },
                (error) => {
                    this.setState({
                        error
                    });
                }
            )

    }

    selectReportAction = ({target}) => {
        let report_id = target.getAttribute("report_id")
        this.setState({
            selectedReportId: report_id
        });
        this.loadIssues(report_id)
    }


    render() {
        let {pid, reports, selectedReportId, issues} = this.state;
        let link;
        if (selectedReportId == -1) {
            link = <p></p>
        }
        else {
            link = 
            <div>
            <a href={"/detail?pid=" + pid + "&rid=" + selectedReportId} class="btn btn-secondary btn-block">
                            View Details
                </a>
            <a href={"/enter_credential?pid=" + pid + "&rid=" + selectedReportId} class="btn btn-secondary btn-block">
                            Create Issues
                </a>
            </div>
        }

        return (
            <div className="row justify-content-between mt-3">
                <div className="card col-2">
                    <div className="card-body">
                        <p className="card-title">Test History</p>
                        <table className="table">
                            <tbody>
                            {
                                reports.map(report => (
                                    <tr>
                                        <td>
                                            <a href="#" onClick={this.selectReportAction.bind(this)} report_id={report.id}>Test-{report.date}</a>
                                        </td>
                                    </tr>)
                                )
                            }
                            </tbody>
                        </table>
                    </div>
                </div>
                <div className="card col-10">
                    <div className="card-body">

                        <p className="card-title">Issues Found</p>
                        <table className="table" id='issuetable'>
                            <thead>
                            <tr>
                                <th>Control</th>
                                <th>Message</th>
                                <th >Source</th>
                                <th>Start line</th>
                                <th>End line</th>
                            </tr>
                            </thead>
                            <tbody>
                            {Object.values(issues).map(item => {
                                return (
                                    <tr>
                                        <td>{item.cid}</td>
                                        <td>{item.rule}</td>
                                        <td >{item.sourcefile}</td>
                                        <td>{item.startLine}</td>
                                        <td>{item.endLine}</td>
                                    </tr>
                                )}
                            )}

                            </tbody>
                        </table>
                        
                        {link}

                    </div>
                </div>
            </div>
        );
    }
}

ReactDOM.render(
    <Reports/>,
    document.getElementById('reports')
);

