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

function key2TR(key, value) {
  return (<tr>
    <td scope="col">{key}</td>
    <td scope="col">{value}</td>
  </tr>)
}

function array2TR(array, key, id) {
  if (key != "parts")
    return (
      <tr>
        <td colspan={2}>
          <a data-toggle="collapse" data-target={"#child-collapese-array" + key + id} href="#">{key}</a>
          <div id={"child-collapese-array" + key + id} class="collapse">
            <table class="table">
              <thead>
              </thead>
              <tbody>
                {
                  array.map((item) => {
                    if (typeof (item) != "string")
                      return (<tr><td>{JSON.stringify(item)}</td></tr>)
                    else
                      return (<tr><td>{item}</td></tr>)
                  })
                }
              </tbody>
            </table>
          </div>
        </td>
      </tr>
    )
}

function replaceDot(str) {
  if (typeof str != "string") {
    return str;
  }
  return str.toString().replace(new RegExp("\\.", 'g'), "_")
}

class Description extends React.Component {

  render() {
    return (
      <table class="table">
        <thead>
        </thead>
        <tbody>
          {this.props.parts.map(
            part => (
              <tr>
                <td>
                  <a data-toggle="collapse" data-target={"#child-collapese" + replaceDot(part.id)} href="#">{part.id ? part.id : part.name}</a>
                  <div id={"child-collapese" + replaceDot(part.id)} class="collapse">
                    <table class="table">
                      <thead>
                      </thead>
                      <tbody>
                        {
                          Object.keys(part).map((key) => { // map all the key-value pairs with string value
                            if (typeof part[key] == "string")
                              return key2TR(key, part[key])
                          })
                        }
                        {
                          Object.keys(part).map((key) => { // map all the key-value pairs with array value (except parts)
                            if (Array.isArray(part[key]))
                              return array2TR(part[key], key, replaceDot(part.id))
                          })
                        }
                        {
                          Object.keys(part).map((key) => { // map the child parts
                            if (key == "parts")
                              return (
                                <tr>
                                  <td colspan={2}>
                                    <div>
                                      <a data-toggle="collapse" data-target={"#collapseControls-" + replaceDot(part.id)} href="#">parts</a>
                                    </div>
                                    <div class="collapse" id={"collapseControls-" + replaceDot(part.id)}>
                                      <div class="card card-body">
                                        <Description parts={part[key]} />
                                      </div>
                                    </div>
                                  </td>
                                </tr>
                              )
                          })
                        }
                      </tbody>
                    </table>
                  </div>
                </td>
              </tr>
            )
          )}
        </tbody>
      </table>
    );
  }
}

class Control extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      pid: query.get("id"),
      error: null,
      isLoaded: false,
      items: [],
      page: 1,
      select: {},
      search: false,
      searchPage: 1,
      newKeywordDictAdd: {},
      newKeywordDictDel: {},
      isAdding: {}
    };
  }

  componentDidMount() {
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
          var selectedDict = {};
          for (var c in result.controls) {
            selectedDict[result.controls[c].id] = result.controls[c];
            let keywords = selectedDict[result.controls[c].id].keywords;
            if (keywords.length > 0) {
              selectedDict[result.controls[c].id].keywords = new Set(keywords.split(','))
            } else {
              selectedDict[result.controls[c].id].keywords = new Set()
            }
          }
          this.setState({
            select: selectedDict
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
    let controlconfigs = []
    let selected = this.state.select
    for (let id in selected) {
      controlconfigs.push({ 'id': id, 'keywords': Array.from(selected[id].keywords).join(',') })
    }

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
        // cids: Array.from(this.state.select),
        controlconfigs: controlconfigs
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
    let control_id = parseInt(target.getAttribute("cid"));
    if (target.checked == true) {
      let newSet = this.state.select;
      let newKeywordDictRender = this.state.newKeywordDictAdd;
      fetch("/get_controlconfig_by_id?project_id=" + query.get("id") + '&control_id=' + control_id)
        .then(res => res.json())
        .then(
          (result) => {

            newSet[control_id] = result.control;
            let keywords = newSet[control_id].keywords;
            if (keywords.length > 0) {
              newSet[control_id].keywords = new Set(keywords.split(','));
            } else {
              newSet[control_id].keywords = new Set();
            }
            newKeywordDictRender[control_id] = '';
            this.setState({
              select: newSet,
              newKeywordDictAdd: newKeywordDictRender
            });
          }
        )
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
    let newSet = this.state.select;
    delete newSet[parseInt(target.getAttribute("cid"))];
    this.setState({
      select: newSet
    });
  }

  addKeyword = (id) => {
    let keywordAdd = this.state.newKeywordDictAdd[id] || '';
    let newSet = this.state.select;
    let newKeywordDictAddRender = this.state.newKeywordDictAdd;

    if (keywordAdd.length > 0) {
      newSet[id].keywords.add(keywordAdd);
      newKeywordDictAddRender[id] = '';
    }

    let newIsAdding = this.state.isAdding;
    newIsAdding[id] = false;

    this.setState({
      select: newSet,
      newKeywordDictAdd: newKeywordDictAddRender,
      isAdding: newIsAdding
    })
  };

  addInputKeyword = ({ target }) => {
    let newKeywordDictAddRender = this.state.newKeywordDictAdd;
    newKeywordDictAddRender[parseInt(target.getAttribute("cid"))] = target.value;
    this.setState({
      newKeywordDictAdd: newKeywordDictAddRender
    });
  };

  delInputKeyword = ({ target }) => {
    let id = parseInt(target.getAttribute("cid"));
    let keywordDel = target.getAttribute("keyword");
    let newSet = this.state.select;
    if (keywordDel.length > 0) {
      newSet[id].keywords.delete(keywordDel)
    }
    this.setState({
      select: newSet
    });
  };

  sortKeywords(keywords) {
    let lstKeywords = Array.from(keywords);
    lstKeywords.sort();
    return lstKeywords;
  }

  startAddingKeyword = (id) => {
    let newIsAdding = this.state.isAdding;
    newIsAdding[id] = true
    this.setState({
      isAdding: newIsAdding
    })
  }

  render() {
    const {pid, error, isLoaded, items, page, searchPage, select, isAdding } = this.state;
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
                  <a class="btn dropdown-toggle float-right" id={"get-controls-" + item.id} data-toggle="collapse" href={"#collapseControls-" + item.id}
                    role="button" aria-expanded="false" aria-controls="collapseExample" />
                </div>
                <div class="collapse" id={"collapseControls-" + item.id}>
                  <div class="card card-body">
                    <table class="table">
                      <thead></thead>
                      <tbody>
                        {
                          Object.keys(item).map((key) => { // map all the key-value pairs with string value
                            if (typeof item[key] == "string")
                              return key2TR(key, item[key])
                          })
                        }
                        {
                          Object.keys(item).map((key) => { // map all the key-value pairs with array value (except parts)
                            if (Array.isArray(item[key]))
                              return array2TR(item[key], key, replaceDot(item.id))
                          })
                        }
                        {item.parts ?
                          (
                            <tr>
                              <td colspan={2}>
                                <div>
                                  <a data-toggle="collapse" data-target={"#collapseControlsParts-" + replaceDot(item.id)} href="#">parts</a>
                                </div>
                                <div class="collapse" id={"collapseControlsParts-" + replaceDot(item.id)}>
                                  <div class="card card-body">
                                    <Description parts={item.parts} />
                                  </div>
                                </div>
                              </td>
                            </tr>
                          )
                          :
                          (<span>NULL</span>)}
                      </tbody>
                    </table>
                  </div>
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
              <a class="page-link" onClick={this.state.search ? this.setSearchPage.bind(this, searchPage - 10) : this.setPage.bind(this, page - 10)} aria-label="first">
                <span aria-hidden="true">&laquo;</span>
              </a>
            </li>
            <li class="page-item">
              <a class="page-link" onClick={this.state.search ? this.setSearchPage.bind(this, searchPage - 1) : this.setPage.bind(this, page - 1)} aria-label="previous">
                <span aria-hidden="true">previous</span>
              </a>
            </li>
            <li class="page-item">
              <a class="page-link" aria-label="next">
                <span aria-hidden="true">{this.state.search ? searchPage : page}</span>
              </a>
            </li>
            <li class="page-item">
              <a class="page-link" onClick={this.state.search ? this.setSearchPage.bind(this, searchPage + 1) : this.setPage.bind(this, page + 1)} aria-label="next">
                <span aria-hidden="true">next</span>
              </a>
            </li>
            <li class="page-item">
              <a class="page-link" onClick={this.state.search ? this.setSearchPage.bind(this, searchPage + 10) : this.setPage.bind(this, page + 10)} aria-label="last">
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
                  {Object.keys(select).map((control_id) => (
                    <li class="list-group-item">
                      <div class="custom-control">
                        <label id={"label_" + control_id}>{select[control_id].cid}, {select[control_id].title}</label>
                        <button type="button" class="btn btn-primary float-right"
                          cid={control_id} onClick={this.deleteClick.bind(this)}>delete</button>
                        <div class="keywords my-1">
                          {this.sortKeywords(select[control_id].keywords).map((keyword) => (
                            <button
                              class="mx-1 my-1 btn btn-light"
                              keyword={keyword}
                              cid={control_id}
                              onClick={this.delInputKeyword.bind(this)}
                            >
                              {keyword} <img width='15' height='15' src="static/img/x.png" />
                            </button>
                          ))
                          }
                          <button className="btn btn-md btn-outline-primary" onClick={this.startAddingKeyword.bind(this, control_id)}>Add keyword</button>

                          <div>
                            {/*{ isAdding && <input type="text" cid={control_id} value={this.state.newKeywordDictAdd[control_id]} onChange={this.addInputKeyword}/> }*/}
                            {/*{ isAdding && <button type="button" onClick={this.addKeyword.bind(this, control_id)}>+</button> }*/}

                            {isAdding[control_id] &&
                              <div className="input-group mb-3">
                                <input type="text" className="form-control" placeholder="Keyword"
                                  aria-describedby="button-addon2" cid={control_id} value={this.state.newKeywordDictAdd[control_id]}
                                  onChange={this.addInputKeyword} />
                                <div className="input-group-append">
                                  <button className="btn btn-outline-secondary" type="button" onClick={this.addKeyword.bind(this, control_id)}
                                    id="button-addon2">Confirm</button>
                                </div>
                              </div>
                            }

                          </div>

                        </div>

                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
            <button id="updateControls" type="button" class="btn btn-secondary btn-block" onClick={this.commitControls.bind(this)}>Update Controls</button>
            <a href={"project_dashboard?id=" + pid} class="btn btn-secondary btn-block">View Project</a>
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

