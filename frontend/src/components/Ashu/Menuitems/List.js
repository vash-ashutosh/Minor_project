import React, { Component  } from "react";
import Navigation from "../Navbar";
import './List.css';

export default class Inventory extends Component {
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
    <div className="Container">
      <Navigation />
      <div className="InventoryList">
          
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
              <i className="fa fa-search" area-hidden="true" />
          </label>
          <div className="ilist">
              <ul>
                <li>WHITE HANGING HEART T-LIGHT HOLDER</li>
                <li>WHITE METAL LANTERN</li>
                <li>CREAM CUPID HEARTS COAT HANGER</li>
                <li>KNITTED UNION FLAG HOT WATER BOTTLE</li>
                <li>RED WOOLLY HOTTIE WHITE HEART</li>
                <li>SET 7 BABUSHKA NESTING BOXES</li>
                <li>GLASS STAR FROSTED T-LIGHT HOLDER</li>
                <li>HAND WARMER UNION JACK</li>
                <li>HAND WARMER RED POLKA DOT</li>
                <li>ASSORTED COLOUR BIRD ORNAMENT</li>
                <li>POPPY'S PLAYHOUSE BEDROOM</li>
                <li>FELTCRAFT PRINCESS CHARLOTTE DOLL</li>
                <li>BOX OF 6 ASSORTED COLOUR TEASPOONS</li>
                <li>LOVE BUILDING BLOCK WORD</li>
              </ul>
          </div>
      </div>
      </div>
    );
  }
}