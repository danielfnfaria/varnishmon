var chartmiss;

/**
 * Request data from the server, add it to the graph and set a timeout
 * to request again
 */
function requestMissData() {
  $.ajax({
    url: '/live/miss/' + group_id,
    success: function(point) {
      var series = chartmiss.series[0],
      shift = series.data.length > 10; // shift if the series is
      chartmiss.series[0].addPoint(point, true, shift);
      setTimeout(requestMissData, 3000);
    },
  cache: false
  });
}

$(document).ready(function() {
  chartmiss = new Highcharts.Chart({
    chart: {
      renderTo: 'miss-container',
      defaultSeriesType: 'area',
      events: {
        load: requestMissData
      }
    },
    colors: ['#CC6633'],
    title: {
      text: 'Miss'
    },
    xAxis: {
      type: 'datetime',
      tickPixelInterval: 150,
      maxZoom: 100
    },
    yAxis: {
    },
    series: [{
      name: 'Miss',
      data: []
    }]
  });
});
