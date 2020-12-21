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
export function postdata(username,pass){

  var formdata = new FormData();
  formdata.append("email", username);
  formdata.append("pass", pass);

  var requestOptions = {
    method: 'POST',
    body: formdata,
    redirect: 'follow'
  };
  var a = fetch("http://127.0.0.1:5000/handle_data", requestOptions)
    .then(response => response.json())
    // .then(result => console.log(result))
    .catch(error => console.log('error', error));
  return a
  }


export default class Login extends React.Component {
   
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
    if(  !(this.state.username === 'sonu@gmail.com' || this.state.username === 'nigam@gmail.com' || this.state.username === 'rahul@gmail.com' || this.state.username === 'aman.r1298@gmail.com')){
      usernameError = "Invalid User";

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
    
    let  httpresp = postdata(this.state.username,this.state.password)
                    .then(data => console.log(data))
    // console.log(httpresp)
    if (httpresp){
      return true
    }
    return httpresp
  
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
               <label htmlFor="username">Email</label>
               <input type="text" name="username" placeholder="Email" value={this.state.username} onChange={this.handleChange} />
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
           {/* <button type="submit" className="btn" style={{color:'#2ECE7E'}}onClick={() => history.push('/Register')} >
             Register
           </button> */}
         </div>
         
         </form>
       </div>
     );
   }
 }