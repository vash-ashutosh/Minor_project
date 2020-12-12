import React from "react";
import history from '../../history';

const initialState={
    custid:"",
    retid:"",
    country:"",
    custidError:"",
    retidError:"",
    countryError:"",
    //LoggedInUser:""
}
export default class Datainput extends React.Component {
   
   state=initialState
   handlelogin = () => {
     this.props.history.push("/Retailerpage");
   }
   validate = () => {
    let custidError = "";
    let retidError = "";
    let countryError = "";

    if (!this.state.custid) {
      custidError = "Customer ID cannot be blank";
    }

    if (!this.state.retid) {
        retidError = "Retailer ID cannot be blank";
      }
    
    if (!this.state.country) {
      countryError = "Country cannot be blank";
    }

    if (custidError || retidError || countryError) {
      this.setState({ custidError, retidError, countryError });
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
      // clear form
      this.setState(initialState);
    }
  };
 
   render() {
     return (
       <div className="base-container" ref={this.props.containerRef}>
         <div className="header">Invoice details</div>
         <form >
         <div className="content">
           <div className="form">
             <div className="form-group">
               <label htmlFor="custid">CustomerID*</label>
               <input type="text" name="custid" placeholder="Customer ID" value={this.state.custid} onChange={this.handleChange} />
               <div style={{ fontSize: 12, color: "red" }}>
                {this.state.custidError}
          </div>
             </div>
             <div className="form-group">
               <label htmlFor="retid">RetailerID*</label>
               <input type="text" name="retid" placeholder="Retailer ID" value={this.state.retid} onChange={this.handleChange}/>
               <div style={{ fontSize: 12, color: "red" }}>
            {this.state.retidError}
          </div>
             </div>
             <div className="form-group">
               <label htmlFor="country">Country*</label>
               <input type="text" name="country" placeholder="Country" value={this.state.country} onChange={this.handleChange}/>
               <div style={{ fontSize: 12, color: "red" }}>
            {this.state.countryError}
          </div>
             </div>

          
           </div>
         </div>
         <div className="footer">
           <button type="submit" className="btn" style={{color:'#2ECE7E'}} onClick={this.handleSubmit}>
             Submit
           </button>
         </div>
         
         </form>
       </div>
     );
   }
 }