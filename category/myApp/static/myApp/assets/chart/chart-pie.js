// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: ['해운대구','기장군','영도구','동래구','수영구','사상구','금정구','사하구','나머지 구'],
    datasets: [{
      data: [1017,358,231,203,100,92,50,38,169],
      backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745','#663399','#34dddd','#663300','#ff6600','#ff0080'],
    }],
  },
});
