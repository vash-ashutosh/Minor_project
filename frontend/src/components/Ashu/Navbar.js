import React from 'react';
//import { Navbar, Nav, Form, Button } from 'react-bootstrap';
import { withRouter } from 'react-router-dom';
import './Navbar.css';

class Navigation extends React.Component {
    render(){
        return (
                    <nav className="Navbaritems" >
                        <h1 className="Navbarheading" > 
                            Welcome to SRMS
                        </h1>
                            <ul className="Menuitems">
                                <li>
                                    <a href="/Offers" style={{color: '#fff',padding: "0.5rem 1rem", textDecoration:"none"}}>Offers</a>
                                </li>
                                <li>
                                    <a href="/Wallet" style={{color: '#fff',padding: "0.5rem 1rem", textDecoration:"none"}}>Wallet</a>
                                </li>
                                <li>
                                    <a href="/List" style={{color: '#fff',padding: "0.5rem 1rem", textDecoration:"none"}}>Inventory</a>
                                </li>
                                <li>
                                    <a href="/" style={{color: '#fff',padding: "0.5rem 1rem", textDecoration:"none"}}>Logout</a>
                                </li>
                            </ul>
                    </nav>
        )
    }
}

export default withRouter(Navigation);