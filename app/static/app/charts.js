import { focusColor, token } from './user_settings.js'
google.charts.load("current", {packages:["corechart"]});
google.charts.setOnLoadCallback(drawChart);
async function drawChart() {
  const pomos = await pomosPerHour()
    .then((pomos) => {
      console.log(pomos);
      var data = google.visualization.arrayToDataTable(pomos);

      var options = {
        title: 'Count of pomodoros, per hour',
        legend: { position: 'top' },
        colors: [focusColor],
        hAxis: {
          ticks: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 , 14, 15, 16, 17, 18, 19 , 20, 21, 22, 23]
        },
        histogram: {
          bucketSize: 0.02,
          maxNumBuckets: 24,
          minValue: 0,
          maxValue: 23
        }
      };

      var chart = new google.visualization.Histogram(document.getElementById('chart_div'));
      chart.draw(data, options);
    });
}


async function pomosPerHour() {
  let output = [['Hour']];
  const response = await fetch(`/api/${token}/get`);
  await response.json().then((pomos) => {

    const keys = Object.keys(pomos);

    for (let i = 0; i < pomos.length; i++) {

      const current = new Date();
      const pomo = pomos[i];
      const hour = parseInt(pomo["created_at"].split('T')[1].split(':')[0]);

      output.push([hour]);
    }
  });
  return output;
}



