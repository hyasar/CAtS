class Project extends React.Component {
  render() {
    return (
      <div>
        Hello {this.props.name}
      </div>
    );
  }
}

ReactDOM.render(
  <Project name="Taylor" />,
  document.getElementById('hello-example')
);

