import React from "react";
import "../components/Register.scss";
import PhoneInput from 'react-phone-input-2'

const initialState={
    username:"",
    password:"",
    user:"",
    number:"",
    usernameError:"",
    passwordError:"",
    userError:"",
    numberError:""
}

export default class Register extends React.Component {
   
   state=initialState
   handlelogin = () => {
     this.props.history.push("/Retailerpage");
   }
   validate = () => {
    let usernameError = "";
    let passwordError = "";

    if (!this.state.username) {
      usernameError = "Username cannot be blank";
    }

    if (!this.state.password) {
        passwordError = "Password cannot be blank";
      }

    if (!this.state.user) {
        usernameError = "User info cannot be blank";
    }

    if (!this.state.username.includes("@")) {
      usernameError = "invalid email";
    }

    if (!this.state.username.includes(".")) {
        usernameError = "invalid email";
      }

    if (passwordError || usernameError) {
      this.setState({ passwordError, usernameError });
      return false;
    }

    return true;
  };

  handleChange = event => {
    const isCheckbox = event.target.type === "checkbox";
    this.setState({
      [event.target.name]: isCheckbox
        ? event.target.checked
        : event.target.value
    });
  };

  handleSubmit = event => {
    event.preventDefault();
    const isValid = this.validate();
    if (isValid) {
      console.log(this.state);
      this.handlelogin();
      // clear form
      this.setState(initialState);
    }
  };
 
   render() {
     return (
       <div className="base-container" ref={this.props.containerRef}>
         <div className="header">Register</div>
         <form >
         <div className="content">
         <div className="image">
              <img src={"https://raw.githubusercontent.com/vash-ashutosh/Project_SmartRetailer/9ea96ce060f477fafb3b297554477ab53eab561e/src/login.svg"} />
         </div>
           <div className="form">
             <div className="form-group">
               <label htmlFor="username">Username*</label>
               <input type="text" name="username" required="True" placeholder="username" value={this.state.username} onChange={this.handleChange} />
               <div style={{ fontSize: 12, color: "red" }}>
                {this.state.usernameError}
          </div>
             </div>
             <div className="form-group">
               <label htmlFor="password">Password*</label>
               <input type="password" name="password" required="True" placeholder="password" value={this.state.password} onChange={this.handleChange}/>
               <div style={{ fontSize: 12, color: "red" }}>
            {this.state.passwordError}
          </div>
             </div>
             <div className="form-group">
               {/*<label htmlFor="phone">Phone</label>*/}
               <PhoneInput
                    name="number"
                    country={''}
                    value={this.state.number}
                    onChange={phone => this.setState({ phone })}
                    required='True'
                />
               <div style={{ fontSize: 12, color: "red" }}>
            {/*{this.state.numberError}*/}
          </div>
             </div>
             <div className="form-group">
               <label htmlFor="user">Retailer or Customer?*</label>
               <input type="user" name="user" required="True" placeholder="Customer/Retailer" value={this.state.user} onChange={this.handleChange}/>
               <div style={{ fontSize: 12, color: "red" }}>
            {this.state.userError}
          </div>
             </div>
           </div>
         </div>
         <div className="footer">
           <button type="submit" className="btn" style={{color:'#2ECE7E'}} onClick={this.handleSubmit}>
             Register
           </button>
         </div>
         </form>
       </div>
     );
   }
 }