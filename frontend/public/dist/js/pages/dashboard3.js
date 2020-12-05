function getdata(){
  var xmlhttp = new XMLHttpRequest();
  var url = "http://127.0.0.1:5000/get_data";
  xmlhttp.open("GET",url,false);
  xmlhttp.send();
  return JSON.parse(xmlhttp.responseText);

}


$(function () {
  'use strict'

  var ticksStyle = {
    fontColor: '#495057',
    fontStyle: 'bold'
  }

  var mode      = 'index'
  var intersect = true

  var $salesChart = $('#sales-chart')
  var salesChart  = new Chart($salesChart, {
    type   : 'bar',
    data   : {
      labels  : ['JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'],
      datasets: [
        {
          backgroundColor: '#007bff',
          borderColor    : '#007bff',
          data           : [1000, 2000, 3000, 2500, 2700, 2500, 3000]
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

  var $visitorsChart = $('#visitors-chart')
  var visitorsChart  = new Chart($visitorsChart, {
    data   : {
      labels  : ['18th', '20th', '22nd', '24th', '26th', '28th', '30th'],
      
      datasets : getdata()
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
//Line graph for aman -1
var $visitorsChart = $('#AmansLine1')
  var visitorsChart  = new Chart($visitorsChart, {
    type:'line',
    data   : {
      labels  : ['18th', '20th', '22nd', '24th', '26th', '28th', '30th'],
      
      datasets : getdata()
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
var $coutrywiseprice = $('#AmansBar1-chart')
var coutrywiseprice  = new Chart($coutrywiseprice, {
  type   : 'bar',
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
  
var $coutrywiseprice = $('#Invoice')
var coutrywiseprice  = new Chart($coutrywiseprice, {
  type   : 'bar',
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

})



