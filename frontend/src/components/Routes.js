import React, { Component } from "react";
import { Router, Switch, Route } from "react-router-dom";
import Customerpage from "./Ashu/customerpage";
import Retailerpage from "./Akash/retailerpage";
import Login from "./login";
import history from "../history";
import Inventory from "./Ashu/Menuitems/List";
import wallet from "./Ashu/Menuitems/Wallet";
import offers from "./Ashu/Menuitems/Offers";


export default class Routes extends Component {
    render() {
        return (
            <Router history={history}>
                <Switch>
                    <Route path="/" exact component={Login} />
                    <Route path="/Customerpage" component={Customerpage} />
                    <Route path="/Retailerpage" component={Retailerpage} />
                    <Route path="/List" component={Inventory} />
                    <Route path="/Wallet" component={wallet} />
                    <Route path="/Offers" component={offers} />
                </Switch>
            </Router>
        )
    }
}