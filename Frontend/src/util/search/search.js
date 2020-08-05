import _ from "lodash";
import React, { Component } from "react";
import { Search, Grid } from "semantic-ui-react";
import axios from 'axios';
import "./search.css";

var source = {};
class SearchBar extends Component {
  constructor() {
    super();
    this.state = {
      data: [],
      ticker:'',
      tag:"",
    };
  }
  componentWillMount() {
    this.resetComponent();
  }
    search=async (value)=> { 
    await axios.get(`https://47314105.ngrok.io/all_ticker`)
    .then(res => {
        const data = res.data;
        source = data;
      })
     console.log(source);
  
  }

  resetComponent = () => {
    this.setState({ isLoading: false, results: [], value: "" });
  };

  handleResultSelect =  async (e, { result }) => {   
      console.log(result);
      await axios.get('https://47314105.ngrok.io/ticker', {
        params: {
          ticker: result
        }
      })
      .then(function (response) {
        console.log(response);
      })
   
    console.log(this.state.ticker);
    

  };

  handleSearchChange = (e, { value }) => {
    console.log(e.target.value);
      
    this.search(e.target.value);
    this.setState({ isLoading: true, value });
    console.log(source);
    
    setTimeout(() => {
      if (this.state.value.length < 1) return this.resetComponent();

      const re = new RegExp(_.escapeRegExp(this.state.value), "i");
      const isMatch = result => re.test(result);

      this.setState({
        isLoading: false,
        results: _.filter(source, isMatch)
      });
    }, 300);
  };

  render() {
    const { isLoading, value, results } = this.state;
    return (
        <div style={{"display": "flex", "justify-content": "flex-end"}}>
        <Grid>
          <Grid.Column width={6}>
            <Search
              className="searchbox"
              placeholder="Looking for a Stock?"
              loading={isLoading}
              onResultSelect={this.handleResultSelect}
              onSearchChange={_.debounce(this.handleSearchChange, 500, {
                leading: true
              })}
              results={results}
              value={value}
            />
          </Grid.Column>
        </Grid>
      </div>
    );
  }
}

export default SearchBar;
