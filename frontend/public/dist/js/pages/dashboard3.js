function getdata(){
  var xmlhttp = new XMLHttpRequest();
  var url = "http://127.0.0.1:5000/show_data";
  xmlhttp.open("GET",url,false);
  xmlhttp.send();
  return JSON.parse(xmlhttp.responseText);

}

var respdata = getdata()
console.log(respdata)
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
var $coutrywiseprice = $('#cwprice-chart')
var coutrywiseprice  = new Chart($coutrywiseprice, {
  type   : 'radar',
  data   : {
    labels  : ['Australia','Austria','Bahrain','Belgium','Brazil','Canada','Channel Islands','Cyprus','Czech Republic','Denmark','Eire','European community','Finland','France','Germany','Greece','Iceland','Israel','Italy','Japan'],
    datasets : [
      {
          label:'Country wise sales',
          data:[169968.110,23613.010,1354.370,65753.420,1411.870,4883.040,44996.760,24980.130,826.740,69862.190,621631.110,1300.250,29925.540,355257.470,431262.461,19096.190,5633.320,10421.090,32550.420,47138.390],
          backgroundColor:['#25DC80','#15C80','#415F80','#55AC80','#153A20','#73CC4F','#4FCCA6','#C0CC4F','#C0CC4F','#541BF3','#AF3DD4','#B99EC1','#91D6D6','#6BA71D','#656375','#7F6EE0','#03D22C','#037F1B','#B7EB48','#DC6D2D']
      }
  ]
  },
  options: {
    maintainAspectRatio: false
    
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

})


