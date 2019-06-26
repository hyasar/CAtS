var selected = new Set(["1"])

class ShowControl extends React.Component {
  render() {
    if(selected.size == 0)
    {
      return <div>No controls</div>
    }
    else
    {
      var str = '';
      let array_selected = Array.from(selected);
      
      for(let i = 0; i<array_selected.length; i++)
      {
        str += " <li> "+array_selected[i]+" </li> "
      }

      return(
        <ul>
          {str}
        </ul>
      );
    }
  }
}

class Control extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      items: []
    };
  }

  componentDidMount() {
    fetch("/controls")
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

  checkboxClick({target}){
    if(target.checked == true)
    {
      selected.add(target.getAttribute("cid"));
    }
    else
    {
      selected.delete(target.getAttribute("cid"));
    }
  }

  render() {
    const { error, isLoaded, items } = this.state;
    if (error) {
      return (
        <div>Error: {error.message}</div>
      );
    } else if (!isLoaded) {
      return (
        <div>Loading...</div>
      );
    } else {
      return (
        <ul>
          {items.map(item => (
            <li key={item.id}>
              <input type="checkbox" cid={item.id} onClick={this.checkboxClick}/>
              {item.cid}，{item.title}
            </li>
          ))}
        </ul>
      );
    }
  }
}

ReactDOM.render(
  <Control />,
  document.getElementById('controls')
);

ReactDOM.render(
  <ShowControl />,
  document.getElementById('show_controls')
);