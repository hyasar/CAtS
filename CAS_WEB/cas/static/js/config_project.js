var selected = new Set()

// class ShowControl extends React.Component {
//   render() {
//     if(selected.size == 0)
//     {
//       return <div>No controls</div>
//     }
//     else
//     {
//       var str = '';
//       let array_selected = Array.from(selected);

//       for(let i = 0; i<array_selected.length; i++)
//       {
//         str += " <li> "+array_selected[i]+" </li> "
//       }

//       return(
//         <ul>
//           {str}
//         </ul>
//       );
//     }
//   }
// }

class Control extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      items: [],
      page: 1,
      select: new Set()
    };
  }

  componentDidMount() {
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

  checkboxClick = ({ target }) => {
    if (target.checked == true) {
      // selected.add(parseInt(target.getAttribute("cid")));
      this.setState({
        select: this.state.select.add(parseInt(target.getAttribute("cid")))
      });
    }
    else {
      // selected.delete(parseInt(target.getAttribute("cid")));
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
    console.log(newPage);
    this.setState({
      isLoaded: false,
      page: newPage
    }, () => { this.componentDidMount(); })
  }

  deleteClick = ({ target }) => {
    var newSet = this.state.select;
    newSet.delete(parseInt(target.getAttribute("cid")));
    this.setState({
      select: newSet
    });
  }

  render() {
    const { error, isLoaded, items, page, select } = this.state;
    if (error) {
      return (
        <div>Error: {error.message}</div>
      );
    } else if (!isLoaded) {
      return (
        <div class="row">
          <div class="col-6">
            <div class="container">
              <div class="mb-2">
                <ul class="list-group">
                  <div>Loading...</div>
                </ul>
              </div>
            </div>
          </div>
          <div class="col-6">
            <div class="container">
              <div class="mb-2">
                <p>List of added controls</p>
                <ul class="list-group">
                  {Array.from(select).map(item => (
                    <li class="list-group-item">
                      <div class="custom-control">
                        <label>{item}</label>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
            <button type="button" class="btn btn-secondary btn-block">Add Controllers</button>
          </div>
        </div>
      );
    } else {
      return (
        <div class="row">
          <div class="col-6">
            <div class="container">
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
                    <a class="page-link" onClick={this.setPage.bind(this, 1)} aria-label="first">
                      <span aria-hidden="true">First</span>
                    </a>
                  </li>
                  <li class="page-item">
                    <a class="page-link" onClick={this.setPage.bind(this, page - 10)} aria-label="first">
                      <span aria-hidden="true">&laquo;</span>
                    </a>
                  </li>
                  <li class="page-item">
                    <a class="page-link" onClick={this.setPage.bind(this, page - 1)} aria-label="previous">
                      <span aria-hidden="true">previous</span>
                    </a>
                  </li>
                  <li class="page-item">
                    <a class="page-link" aria-label="next">
                      <span aria-hidden="true">{page}</span>
                    </a>
                  </li>
                  <li class="page-item">
                    <a class="page-link" onClick={this.setPage.bind(this, page + 1)} aria-label="next">
                      <span aria-hidden="true">next</span>
                    </a>
                  </li>
                  <li class="page-item">
                    <a class="page-link" onClick={this.setPage.bind(this, page + 10)} aria-label="last">
                      <span aria-hidden="true">&raquo;</span>
                    </a>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <div class="col-6">
            <div class="container">
              <div class="mb-2">
                <p>List of added controls</p>
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
            <button type="button" class="btn btn-secondary btn-block">Add Controllers</button>
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

// ReactDOM.render(
//   <ShowControl />,
//   document.getElementById('show_controls')
// );