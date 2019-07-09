// var selected = new Set()

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

class Control extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      items: [],
      page: 1,
      select: new Set(),
      search: false,
      searchPage: 1
    };
  }

  componentDidMount() {
    // this.loadControls.bind(this);
    this.loadControls();
    this.loadSelectedControls();
  }

  loadControls = () => {
    fetch("/controls?page=" + this.state.page)
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            items: result.controls
          });
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
  }

  searchControls = () => {
    if (!this.state.search) {
      this.setState({
        searchPage: 1,
        search: true
      })
    }
    fetch("/searchControls?page=" + this.state.searchPage + "&key=" + $("#searchKey").val())
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            items: result.controls
          });
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
  }

  loadSelectedControls = () => {
    fetch("/get_project_controlls?id=" + query.get("id"))
      .then(res => res.json())
      .then(
        (result) => {
          var selectedSet = new Set();
          for (var c in result.controls) {
            selectedSet.add(result.controls[c].id);
          }
          this.setState({
            select: selectedSet
          });
        },
        (error) => {
          this.setState({
            error
          });
          $("#updateControls").html("Update Error");
        }
      )
  }

  commitControls = () => {
    const csrfToken = getCookie('csrftoken');
    $("#updateControls").html("updating");
    $("#updateControls").attr("disabled", true);
    fetch("/setcontrols", {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        id: query.get('id'),
        cids: Array.from(this.state.select),
      })
    })
      .then(res => res.json())
      .then(
        (result) => {
          $("#updateControls").html("Update Controls");
          $("#updateControls").attr("disabled", false);
        },
        (error) => {
          this.setState({
            error
          })
          console.error(error);
        }
      )
  }

  checkboxClick = ({ target }) => {
    if (target.checked == true) {
      this.setState({
        select: this.state.select.add(parseInt(target.getAttribute("cid")))
      });
    }
    else {
      var newSet = this.state.select;
      newSet.delete(parseInt(target.getAttribute("cid")));
      this.setState({
        select: newSet
      });
    }
  }

  setPage = (newPage) => {
    if (newPage <= 0) {
      newPage = 1;
    }
    this.setState({
      isLoaded: false,
      page: newPage
    }, () => { this.loadControls(); })
  }

  setSearchPage = (newPage) => {
    if (newPage <= 0) {
      newPage = 1;
    }
    this.setState({
      isLoaded: false,
      searchPage: newPage
    }, () => { this.searchControls(); })
  }

  deleteClick = ({ target }) => {
    var newSet = this.state.select;
    newSet.delete(parseInt(target.getAttribute("cid")));
    this.setState({
      select: newSet
    });
  }

  render() {
    const { error, isLoaded, items, page, searchPage, select } = this.state;
    let list;
    if (isLoaded) {
      list =
        <div class="mb-2">
          <ul class="list-group">
            {items.map(item => (
              <li class="list-group-item">
                <div class="custom-control custom-checkbox">
                  <input type="checkbox" class="custom-control-input" id={item.id} cid={item.id}
                    onClick={this.checkboxClick.bind(this)} />
                  <label class="custom-control-label" for={item.id}>{item.cid}，{item.title}</label>
                </div>
              </li>
            ))}
          </ul>
          <ul class="pagination justify-content-center row">
            <li class="page-item">
              <a class="page-link" onClick={this.state.search ? this.setSearchPage.bind(this, 1) : this.setPage.bind(this, 1)} aria-label="first">
                <span aria-hidden="true">First</span>
              </a>
            </li>
            <li class="page-item">
              <a class="page-link" onClick={this.state.search ? this.setSearchPage.bind(this, searchPage-10) : this.setPage.bind(this, page-10)} aria-label="first">
                <span aria-hidden="true">&laquo;</span>
              </a>
            </li>
            <li class="page-item">
              <a class="page-link" onClick={this.state.search ? this.setSearchPage.bind(this, searchPage-1) : this.setPage.bind(this, page-1)} aria-label="previous">
                <span aria-hidden="true">previous</span>
              </a>
            </li>
            <li class="page-item">
              <a class="page-link" aria-label="next">
                <span aria-hidden="true">{this.state.search? searchPage:page}</span>
              </a>
            </li>
            <li class="page-item">
              <a class="page-link" onClick={this.state.search ? this.setSearchPage.bind(this, searchPage+1) : this.setPage.bind(this, page+1)} aria-label="next">
                <span aria-hidden="true">next</span>
              </a>
            </li>
            <li class="page-item">
              <a class="page-link" onClick={this.state.search ? this.setSearchPage.bind(this, searchPage+10) : this.setPage.bind(this, page+10)} aria-label="last">
                <span aria-hidden="true">&raquo;</span>
              </a>
            </li>
          </ul>
        </div>
    }
    else {
      list =
        <div class="mb-2">
          Loading...
    </div>
    }

    if (error) {
      return (
        <div>Error: {error.message}</div>
      );
    } else { //loading finished
      return (
        <div class="row">
          <div class="col-6">
            <div class="input-group md-form form-sm mb-2">
              <input id="searchKey" class="form-control my-0 py-1" type="text" placeholder="Search" aria-label="Search" />
              <button class="btn btn-primary" onClick={this.setSearchPage.bind(this, 1)}>Search</button>
            </div>
            <div class="container" style={{ marginTop: 5 + "px" }}>
              {list}
            </div>
          </div>
          <div class="col-6">
            <div class="container">
              <div class="mb-2">
                <p>List of controls</p>
                <ul class="list-group">
                  {Array.from(select).map(item => (
                    <li class="list-group-item">
                      <div class="custom-control">
                        <label>{item}</label>
                        <button type="botton" class="btn btn-primary float-right"
                          cid={item} onClick={this.deleteClick.bind(this)}>delete</button>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
            <button id="updateControls" type="button" class="btn btn-secondary btn-block" onClick={this.commitControls.bind(this)}>Update Controls</button>
          </div>
        </div>
      );
    }
  }
}

ReactDOM.render(
  <Control />,
  document.getElementById('controls')
);
