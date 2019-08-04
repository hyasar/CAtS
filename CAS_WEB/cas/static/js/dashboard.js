const url = new URL(window.location.href);
const query = new URLSearchParams(url.search);

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

class Dashboard extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      report_id: this.props.report_id
      issues: []
    };
  }

  loadIssues = () => {
    fetch("/get_issues?report_id=" + this.report_id)
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            issues: result.issues,
          });
        },
        (error) => {
          this.setState({
            error
          });
        }
      )
  }

  render() {
    return (
      <div className="card-body">
        <p className="card-title">Test Report</p>
        <table className="table">
          <thead>
          <tr>
            <th>Control</th>
            <th>Message</th>
          </tr>
          </thead>
          <tbody>
          <tr>
            <td>ac-1</td>
            <td>ldkjsfoeiw</td>
          </tr>
          </tbody>
        </table>
      </div>
    );
  }
}

class Reports extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      reports: [],
      selctedReport: null
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
          this.setState({
            reports: result.reports,
          });
        },
        (error) => {
          this.setState({
            error
          });
        }
      ).then(res =>
          this.selctedReport = this.report[0] || null
      )
  }


  render() {
    const { reports, selctedReport } = this.state

    return (
      <div className="row justify-content-between mt-3">
        <div className="card col-4">
          <div className="card-body">
            <p className="card-title">Test History</p>
            <table className="table">
              <tbody>
              {
                reports.map(report => (
                  <tr>
                    <td><a href="#">Test-{report.date}</a></td>
                  </tr>)
                )
              }
              </tbody>
            </table>
          </div>
        </div>
        <div className="card col-8">
          <Dashboard report_id={selctedReport.id}/>
        </div>
      </div>
    );
  }
}

ReactDOM.render(
  <Reports />,
  document.getElementById('reports')
);

