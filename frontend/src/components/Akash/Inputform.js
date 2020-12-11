import React from "react";
import "../components/login.scss";
import history from '../history';

const initialState={
    username:"",
    password:"",
    usernameError:"",
    passwordError:"",
    //LoggedInUser:""
}
function postdata(username,pass){
  var xmlhttp = new XMLHttpRequest();
  var url = "http://127.0.0.1:5000/handle_data";
  xmlhttp.open("POST",url,true);
  xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  let params = "email=${username}&pass=${password}"; 
  xmlhttp.send(params);

}
export default class Datainput extends React.Component {
   
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
    
    let resp = postdata(this.state.username,this.state.password)
    if (resp){
      return true
    }
  
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
         <div className="header">Login</div>
         <form >
         <div className="content">
         <div className="image">
              <img src={"https://raw.githubusercontent.com/vash-ashutosh/Project_SmartRetailer/9ea96ce060f477fafb3b297554477ab53eab561e/src/login.svg"} />
         </div>
           <div className="form">
             <div className="form-group">
               <label htmlFor="username">Username</label>
               <input type="text" name="username" placeholder="username" value={this.state.username} onChange={this.handleChange} />
               <div style={{ fontSize: 12, color: "red" }}>
                {this.state.usernameError}
          </div>
             </div>
             <div className="form-group">
               <label htmlFor="password">Password</label>
               <input type="password" name="password" placeholder="password" value={this.state.password} onChange={this.handleChange}/>
               <div style={{ fontSize: 12, color: "red" }}>
            {this.state.passwordError}
          </div>
             </div>
           </div>
         </div>
         <div className="footer">
           <button type="submit" className="btn" style={{color:'#2ECE7E'}} onClick={this.handleSubmit}>
             Login
           </button>
           <button type="submit" className="btn" style={{color:'#2ECE7E'}}onClick={() => history.push('/Register')} >
             Register
           </button>
         </div>
         
         </form>
       </div>
     );
   }
 }