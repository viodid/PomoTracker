import { focusColor, token } from './user_settings.js'
google.charts.load('current', {'packages':['bar']});
google.charts.setOnLoadCallback(drawStuff);

async function drawStuff() {
  const pomos = await pomosPerHour()
    .then((pomos) => {
      console.log(pomos);

      var data = new google.visualization.arrayToDataTable(pomos);

      var options = {
        title: 'Count of pomodoros, per hour',
        width: 800,
        legend: { position: 'none' },
        colors: [focusColor],
        hAxis: {
          ticks: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 , 14, 15, 16, 17, 18, 19 , 20, 21, 22, 23]
        },
        bar: { groupWidth: "90%" }
      };

      var chart = new google.charts.Bar(document.getElementById('top_x_div'));
      chart.draw(data, google.charts.Bar.convertOptions(options));
    });
}

async function pomosPerHour() {
  let aggregated = {};
  const response = await fetch(`/api/${token}/get`);
  await response.json().then((pomos) => {

    const keys = Object.keys(pomos);

    // initialize the 24 hours
    for (let i = 0; i < 24; i++) {
      aggregated[i] = 0;
    }

    for (let i = 0; i < pomos.length; i++) {

      const current = new Date();
      const pomo = pomos[i];
      const hour = parseInt(pomo["created_at"].split('T')[1].split(':')[0]);

      if (aggregated[hour]) {
        aggregated[hour] += 1;
      } else {
        aggregated[hour] = 1;
      }
    }
    console.log(aggregated);
  });
  return aggregateToChart(aggregated);
}

function aggregateToChart(aggregated) {
  let output = [['Hour', 'Count']];
  const keys = Object.keys(aggregated);
  for (let i = 0; i < keys.length; i++) {
    output.push([keys[i], aggregated[keys[i]]]);
  }
  return output;
}



