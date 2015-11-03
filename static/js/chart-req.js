var chartclient_req;

/**
 * Request data from the server, add it to the graph and set a timeout
 * to request again
 */
function requestClient_reqData() {
  $.ajax({
    url: '/live/client_req/' + group_id,
    success: function(point) {
      var series = chartclient_req.series[0],
      shift = series.data.length > 10; // shift if the series is
      chartclient_req.series[0].addPoint(point, true, shift);
      setTimeout(requestClient_reqData, 3000);
    },
  cache: false
  });
}

$(document).ready(function() {
  chartclient_req = new Highcharts.Chart({
    chart: {
      renderTo: 'client_req-container',
      defaultSeriesType: 'area',
      events: {
        load: requestClient_reqData
      }
    },
    colors: ['#3399FF'],
    title: {
      text: 'Client_req'
    },
    xAxis: {
      type: 'datetime',
      tickPixelInterval: 150,
      maxZoom: 100
    },
    yAxis: {
    },
    series: [{
      name: 'Client_req',
      data: []
    }]
  });
});
