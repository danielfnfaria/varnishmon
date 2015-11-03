var charthit;

/**
 * Request data from the server, add it to the graph and set a timeout
 * to request again
 */
function requestHitData() {
  $.ajax({
    url: '/live/hit/' + group_id,
    success: function(point) {
      var series = charthit.series[0],
      shift = series.data.length > 10; // shift if the series is
      charthit.series[0].addPoint(point, true, shift);
      setTimeout(requestHitData, 3000);
    },
  cache: false
  });
}

$(document).ready(function() {
  charthit = new Highcharts.Chart({
    chart: {
      renderTo: 'hit-container',
      defaultSeriesType: 'area',
      events: {
        load: requestHitData
      }
    },
    colors: ['#99FFCC'],
    title: {
      text: 'Hit'
    },
    xAxis: {
      type: 'datetime',
      tickPixelInterval: 150,
      maxZoom: 100
    },
    yAxis: {
    },
    series: [{
      name: 'Hit',
      data: []
    }]
  });
});
