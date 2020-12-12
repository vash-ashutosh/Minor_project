import React from "react";
import history from '../../history';

const initialState={
    custid:"",
    retid:"",
    country:"",
    stockcode:"",
    description:"",
    price:"",
    quantity:"",
    stockcodeError:"",
    descriptionError:"",
    priceError:"",
    quantityError:"",
    custidError:"",
    retidError:"",
    countryError:""
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
    let stockcodeError="";
    let descriptionError="";
    let priceError="";
    let quantityError="";

    if (!this.state.custid) {
      custidError = "Customer ID cannot be blank";
    }

    if (!this.state.retid) {
        retidError = "Retailer ID cannot be blank";
      }
    
    if (!this.state.country) {
      countryError = "Country cannot be blank";
    }
    
    if (!this.state.stockcode) {
      stockcodeError = "Stockcode cannot be blank";
    }

    if (!this.state.description) {
      descriptionError = "Description cannot be blank";
    }
    if (!this.state.price) {
      priceError = "Price cannot be blank";
    }
    if (!this.state.quantity) {
      quantityError = "Quantity cannot be blank";
    }

    if (custidError || retidError || countryError || stockcodeError || descriptionError || quantityError||priceError) {
      this.setState({ custidError, retidError, countryError, stockcodeError ,descriptionError ,quantityError , priceError});
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
             <div className="form-group">
               <label htmlFor="stockcode">Stockcode*</label>
               <input type="text" name="stockcode" placeholder="Enter..." value={this.state.stockcode} onChange={this.handleChange}/>
               <div style={{ fontSize: 12, color: "red" }}>
            {this.state.stockcodeError}
          </div>
             </div>
             <div className="form-group">
               <label htmlFor="description">Description*</label>
               <input type="text" name="description" placeholder="Enter description" value={this.state.description} onChange={this.handleChange}/>
               <div style={{ fontSize: 12, color: "red" }}>
            {this.state.descriptionError}
          </div>
             </div>
             <div className="form-group">
               <label htmlFor="price">Price*</label>
               <input type="text" name="price" placeholder="Price" value={this.state.price} onChange={this.handleChange}/>
               <div style={{ fontSize: 12, color: "red" }}>
            {this.state.priceError}
          </div>
             </div>
             <div className="form-group">
               <label htmlFor="quantity">Quantity*</label>
               <input type="text" name="quantity" placeholder="Enter Quantity" value={this.state.quantity} onChange={this.handleChange}/>
               <div style={{ fontSize: 12, color: "red" }}>
            {this.state.quantityError}
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