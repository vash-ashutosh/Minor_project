import React, { Component } from "react";
//import { Button } from 'react-bootstrap';
//import history from '../../history';
import Navigation from './Navbar';

export default class Customerpage extends Component {
  render() {
    return (
      <div className="Customerpage">
        <div className="lander" >
          <div className="Nbar">
            <Navigation />
          </div>
          {/*<form>
            <Button variant="btn btn-success" onClick={() => history.push('/Retailerpage')}>Retailer side</Button>
          </form>*/}
          
        </div>
      </div>
    );
  }
}