const url = new URL(window.location.href);
const query = new URLSearchParams(url.search);

class Matches extends React.Component {
	constructor(props) {
        super(props);
        this.state = {
        	lname: "",
        	rid: -1,
        	lid: -1,
        	rname: ""
        };
    }

    componentDidMount() {
        this.matchNameToId();
        this.matchIdToName();
    }

    matchNameToId = () => {
    	fetch("/get_id_by_name?name=" + this.state.lname)
    		.then(res => res.json())
	    	.then(
	    		(result) => {
	    			let lname = result.name;
	    			let rid = result.id;
	    			this.setState({
	    				lname : lname,
	    				rid : rid
	    			});
	    		},
	    		(error) => {
	    			this.setState({
	    				error
	    			});
	    		}
	    	)
    }

    matchIdToName = () => {
    	fetch("/get_name_by_id?id=" + this.state.lid)
    		.then(res => res.json())
	    	.then(
	    		(result) => {
	    			let rname = result.name;
	    			let lid = result.id;
	    			this.setState({
	    				rname : rname,
	    				lid : lid
	    			});
	    		},
	    		(error) => {
	    			this.setState({
	    				error
	    			});
	    		}
	    	)
    }

    setName(event) {
        this.setState({
            lname: event.target.value,
        });
    }

    setId(event) {
        this.setState({
            lid: event.target.value,
        });
    }

    render() {
    	let {lname, rid, lid, rname} = this.state;

    	return (
    		<div>
    			<p><form>Enter username: 
    				<input type="text" name="name" placeholder={lname} onChange={this.setName.bind(this)}/>
    				, user Id is {rid}
    				<button type="button" onClick={this.matchNameToId.bind(this)}>Match Id</button>
    			</form></p>

    			<p><form>Enter user Id: 
    				<input type="text" name="id" placeholder={lid} onChange={this.setId.bind(this)}/>
    				, username is {rname}
    				<button type="button" onClick={this.matchIdToName.bind(this)}>Match Name</button>
    			</form></p>
    		</div>
    	);
    }
}

ReactDOM.render(
    <Matches/>,
    document.getElementById('matches')
);