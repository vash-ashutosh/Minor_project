import React, { Component  } from "react";
import Navigation from "../Navbar";

export default class offers extends Component {
    constructor(props){
        super(props);

        this.state={
            query:"",
            results:{},
            message:""
        }
    }
  render() {
    return (
      <div className="InventoryList">
          <Navigation />
          <h1 className='Heading'>
              Inventory list
          </h1>
          <h2 className="Search">
              Search for items
          </h2>
          <label className="search-label" htmlFor="search-input">
              <input
                  type="text"
                  value=""
                  id="search-input"
                  placeholder="Search..."
              />
          </label>
      </div>
    );
  }
}