import React, { Component } from "react";

import Content from './RetailComp/Content'
import Footer from './RetailComp/Footer'
import Header from './RetailComp/Header'
import Menu from './RetailComp/Menu'

export default class Retailerpage extends Component {
  render() {
    return (
      <div>
      <Header/>
      <Menu/>
      <Content/>
      <Footer/>
    </div>
    );
  }
}