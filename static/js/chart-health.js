$(document).ready(function() {
  setInterval(function() {
    $.ajax({
      url: '/live/health/' + group_id,
      success: function(data) {
        $('#health-container').text(data+"%");
      },
    });
  }, 3000);
});
