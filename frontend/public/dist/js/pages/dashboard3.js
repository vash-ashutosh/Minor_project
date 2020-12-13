function getdata(){
  var xmlhttp = new XMLHttpRequest();
  var url = "http://127.0.0.1:5000/show_data";
  xmlhttp.open("GET",url,false);
  xmlhttp.send();
  return JSON.parse(xmlhttp.responseText);

}
function custdata(){
  var xmlhttp = new XMLHttpRequest();
  var url = "http://127.0.0.1:5000/customer_data";
  xmlhttp.open("GET",url,false);
  xmlhttp.send();
  return JSON.parse(xmlhttp.responseText);

}

function forcastdata(){
  var xmlhttp = new XMLHttpRequest();
  var url = "http://127.0.0.1:5000/forcast";
  xmlhttp.open("GET",url,false);
  xmlhttp.send();
  return JSON.parse(xmlhttp.responseText);

}

var customerdata = custdata()
var respdata = getdata()
var forcast = forcastdata()
console.log(forcast)
$(function () {
  'use strict'

  var ticksStyle = {
    fontColor: '#495057',
    fontStyle: 'bold'
  }

  var mode      = 'index'
  var intersect = true

  var $weeklysaleschart = $('#weekly-sales-chart')
  var $weeklysaleschart  = new Chart($weeklysaleschart, {
    type   : 'bar',
    data   : {
      labels  : respdata.weekly_sales_days.map(String),
      datasets: [
        {
          backgroundColor: '#007bff',
          borderColor    : '#007bff',
          data           : respdata.weekly_sales_price
        }
      ]
    },
    options: {
      maintainAspectRatio: false,
      tooltips           : {
        mode     : mode,
        intersect: intersect
      },
      hover              : {
        mode     : mode,
        intersect: intersect
      },
      legend             : {
        display: false
      },
      scales             : {
        yAxes: [{
          // display: false,
          gridLines: {
            display      : true,
            lineWidth    : '4px',
            color        : 'rgba(0, 0, 0, .2)',
            zeroLineColor: 'transparent'
          },
          ticks    : $.extend({
            beginAtZero: true,

            // Include a dollar sign in the ticks
            callback: function (value, index, values) {
              if (value >= 1000) {
                value /= 1000
                value += 'k'
              }
              return '$' + value
            }
          }, ticksStyle)
        }],
        xAxes: [{
          display  : true,
          gridLines: {
            display: false
          },
          ticks    : ticksStyle
        }]
      }
    }
  })

  

//Pie chart for country wise price
var $forcastchart = $('#forcast-chart')
var forcastchart  = new Chart($forcastchart, {
  type:'line',
  data   : {
    labels  : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85],
    
    
    datasets : [{
      data:forcast.previous_sales.concat([0,0,0,0,0]),
      
    },{
      data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0].concat(forcast.predictions),
      backgroundColor:['#424ef5']
    }]
  },
  options: {
    maintainAspectRatio: false,
    tooltips           : {
      mode     : mode,
      intersect: intersect
    },
    hover              : {
      mode     : mode,
      intersect: intersect
    },
    legend             : {
      display: false
    },
    scales             : {
      yAxes: [{
        // display: false,
        gridLines: {
          display      : true,
          lineWidth    : '4px',
          color        : 'rgba(0, 0, 0, .2)',
          zeroLineColor: 'transparent'
        },
        ticks    : $.extend({
          beginAtZero : true,
          suggestedMax: 200
        }, ticksStyle)
      }],
      xAxes: [{
        display  : true,
        gridLines: {
          display: false
        },
        ticks    : ticksStyle
      }]
    }
  }
})

//Pie chart for country wise price
var $coutrywiseprice = $('#coutrywiseprice-chart')
var coutrywiseprice  = new Chart($coutrywiseprice, {
  type   : 'pie',
  data   : {
    labels  : respdata.country_best_count.map(String),
    datasets : [
      {
          label:'Country wise sales',
          data:respdata.country_best_price,
          backgroundColor:['#25DC80','#15C80','#415F80','#55AC80','#153A20','#73CC4F','#4FCCA6','#C0CC4F','#C0CC4F','#541BF3','#AF3DD4','#B99EC1','#91D6D6','#6BA71D','#656375','#7F6EE0','#03D22C','#037F1B','#B7EB48','#DC6D2D']
      }
  ]
  },
  options: {
    maintainAspectRatio: false
    
  }
})
//Line graph for aman -1
var $invoiceChart = $('#Invoicechart')
  var invoiceChart  = new Chart($invoiceChart, {
    type:'line',
    data   : {
      labels  : respdata.months.map(String) ,
      
      datasets : [{
        data:respdata.invoice_counts
      }]
    },
    options: {
      maintainAspectRatio: false,
      tooltips           : {
        mode     : mode,
        intersect: intersect
      },
      hover              : {
        mode     : mode,
        intersect: intersect
      },
      legend             : {
        display: false
      },
      scales             : {
        yAxes: [{
          // display: false,
          gridLines: {
            display      : true,
            lineWidth    : '4px',
            color        : 'rgba(0, 0, 0, .2)',
            zeroLineColor: 'transparent'
          },
          ticks    : $.extend({
            beginAtZero : true,
            suggestedMax: 200
          }, ticksStyle)
        }],
        xAxes: [{
          display  : true,
          gridLines: {
            display: false
          },
          ticks    : ticksStyle
        }]
      }
    }
  })
  //Amans bar-1
var $weeklysalesprice = $('#Weekly-sales')
var $weeklysalesprice  = new Chart($weeklysalesprice, {
  type   : 'bar',
  data   : {
    labels  : respdata.weekly_sales_days,
    datasets : [
      {
          label:'Country wise sales',
          data:respdata.weekly_sales_price,
          backgroundColor:['#25DC80','#15C80','#415F80','#55AC80','#153A20','#73CC4F','#4FCCA6']
      }
  ]
  },
  options: {
    maintainAspectRatio: false
    
  }
})
  
var $hourlysales = $('#hourly-sales')
var $hourlysales  = new Chart($hourlysales, {
  type   : 'bar',
  data   : {
    labels  : respdata.hourly_sales.map(String),
    datasets : [
      {
          label:'Hour wise sales',
          data:respdata.hourly_sales_price,
          backgroundColor:['#25DC80','#15C80','#415F80','#55AC80','#153A20','#73CC4F','#4FCCA6','#C0CC4F','#C0CC4F','#541BF3','#AF3DD4','#B99EC1','#91D6D6','#6BA71D','#656375']
      }
  ]
  },
  options: {
    maintainAspectRatio: false
    
  }
})


// var $segchart = $('#seg-chart')
// var $segchart  = new Chart($segchart, {
//   type   : 'bar',
//   data   : {
//     labels  : ['Lost','Potential loyalist','At risk','Promising','Loyal customers','About to sleep','Needing attention','Cant loose them','New customers'],
//     datasets : [
//       {
//           label:'Segmentation Chart',
//           data:[customerdata["Lost"][1],customerdata["Potential layalist"][1],customerdata["At risk"][1],customerdata["Promising"][1],customerdata["Loyal customers"][1],customerdata["About to sleep"][1],customerdata["Need attention"][1],customerdata["Cant loose them"][1],customerdata["New customers"][1]],
//           // backgroundColor:['#25DC80','#15C80','#415F80','#55AC80','#153A20','#73CC4F','#4FCCA6']
//       }
//   ]
//   },
//   options: {
//     maintainAspectRatio: false
    
//   }
// })

var $hourlysales = $('#seg-chart')
var $hourlysales  = new Chart($hourlysales, {
  type   : 'bar',
  data   : {
    labels  : ['Lost','Potential loyalist','At risk','Promising','Loyal customers','About to sleep','Needing attention','Cant loose them','New customers'],
    datasets : [
      {
          // label:'Segmentation chart',
          data:[customerdata["Lost"][1],customerdata["Potential loyalist"][1],customerdata["At risk"][1],customerdata["Promising"][1],customerdata["Loyal customers"][1],customerdata["About to sleep"][1],customerdata["Needing attention"][1],customerdata["Cant loose them"][1],customerdata["New customers"][1]],
          backgroundColor:['#25DC80','#15C80','#415F80','#55AC80','#153A20','#73CC4F','#4FCCA6','#C0CC4F','#C0CC4F']
      }
  ]
  },
  options: {
    maintainAspectRatio: false
    
  }
})




})


  