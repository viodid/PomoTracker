import { focusColor, username, whiteTheme } from './user_settings.js';

google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawBarChart1);
google.charts.setOnLoadCallback(drawBarChart2);
google.charts.setOnLoadCallback(drawPieChart1);

// Pomodoros per Hour
async function drawBarChart1() {
  const pomos = await pomosPerHour()
    .then((pomos) => {
      var data = new google.visualization.DataTable();
      data.addColumn('string', 'Hour');
      data.addColumn('number', 'Count');
      data.addRows(pomos);

      var options = {
        colors: [focusColor],
        title: 'Pomodoros per Hour',
        titleTextStyle: {
          color: fontColor(),
          fontSize: 22,
          bold: false,
        },
        legend: { position: 'none' },
        fontName: 'Roboto',
        backgroundColor: { 
          fill:'transparent',
        },
        bar: { groupWidth: "90%" },
        chartArea: {
          width: "85%",
          height: "75%"
        },
        hAxis: {
          title: 'Hour',
          titleTextStyle: {
            color: fontColor(),
            fontSize: 15,
            italic: false,
          },
          textStyle: {
            color: fontColor(),
          },
        },
        vAxis: {
          title: 'Count',
          titleTextStyle: {
            color: fontColor(),
            fontSize: 15,
            italic: false,
          },
          textStyle: {
            color: fontColor(),
          },
          minorGridlines: {
            count: 0
          },
          baselineColor: fontColor(),
        },
        animation: {
          duration: 1000,
          easing: 'out',
          startup: true,
        },
      };

      var chart = new google.visualization.ColumnChart(document.getElementById('bar-chart-left'));
      chart.draw(data, options);
    });
}

// Pomodoros per Day
function drawBarChart2() {
  const pomos = pomosPerDay()
  .then((pomos) => {
    var data = new google.visualization.DataTable();
    data.addColumn('date', 'Date');
    data.addColumn('number', 'Count');
    data.addRows(pomos);

    var options = {
      colors: [focusColor],
      title: 'Pomodoros per Day',
      titleTextStyle: {
        color: fontColor(),
        fontSize: 22,
        bold: false,
      },
      legend: { position: 'none' },
      fontName: 'Roboto',
      backgroundColor: { 
        fill:'transparent',
      },
      bar: { groupWidth: "75%" },
      chartArea: {
        width: "85%",
        height: "75%"
      },
      hAxis: {
        title: 'Date',
        titleTextStyle: {
          color: fontColor(),
          fontSize: 15,
          italic: false,
        },
        textStyle: {
          color: fontColor(),
        },
        minorGridlines: {
          count: 0
        },
        gridlines: {
          count: 0
        },
      },
      vAxis: {
        title: 'Count',
        titleTextStyle: {
          color: fontColor(),
          fontSize: 15,
          italic: false,
        },
        textStyle: {
          color: fontColor(),
        },
        minorGridlines: {
          count: 0
        },
        baselineColor: fontColor(),
      },
      animation: {
        duration: 1000,
        easing: 'out',
        startup: true,
      },
      trendlines: {
        0: {
          color: 'red',
          lineWidth: 3,
          opacity: 0.5,
        },
      },
    };

    var chart = new google.visualization.ColumnChart(document.getElementById('bar-chart-right'));
    chart.draw(data, options);

  });
}

async function drawPieChart1() {
  const pomos = await aggregatedPomosByTag()
  .then((pomos) => {
    console.log(pomos);
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Tag');
    data.addColumn('number', 'Count');
    data.addRows(pomos);

    var options = {
        title: 'Pomodoros by Tag',
        fontName: 'Roboto',
        titleTextStyle: {
          color: fontColor(),
          fontSize: 22,
          bold: false,
        },
        legend: {
          position: 'right',
          textStyle: {
            color: fontColor(),
          },
        },
        backgroundColor: { 
          fill:'transparent',
        },
        chartArea: {
          width: "100%",
          height: "75%",
          bottom: 20,
          left: 40,
        },
      }

    var chart = new google.visualization.PieChart(document.getElementById('pie-chart'));
    chart.draw(data, options);
  });
}

async function aggregatedPomosByTag() {
  let aggregated = {};
  const response = await fetch(`/api/${username}/tag`);
  await response.json().then((data) => {
      aggregated = data;
    });
  return aggregateToChart(aggregated);
}



async function pomosPerHour() {
  let aggregated = {};
  const response = await fetch(`/api/${username}/get`);
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
  });
  return aggregateToChart(aggregated);
}

function aggregateToChart(aggregated, date = false) {
  let output = [];
  const keys = Object.keys(aggregated);
  for (let i = 0; i < keys.length; i++) {
    if (date) {
      const date = new Date(keys[i]);
      output.push([date, aggregated[keys[i]]]);
    } else {
      output.push([keys[i], aggregated[keys[i]]]);
    }
  }
  return output;
}

function fontColor() {
  return (whiteTheme) ? '#121212' : '#efefef';
}

async function pomosPerDay() {
  let aggregated = {};
  const response = await fetch(`/api/${username}/get`);
  await response.json().then((pomos) => {
    if (!pomos.length) {
      return [0];
    }

    const keys = Object.keys(pomos);
    let firstDate = new Date();
    firstDate = parseDate(firstDate);
    let lastDate = new Date(pomos[pomos.length - 1]["created_at"]);
    lastDate = parseDate(lastDate);

    // initialize the days
    while (firstDate > lastDate) {
      aggregated[firstDate] = 0;
      firstDate = new Date(firstDate);
      firstDate.setDate(firstDate.getDate() - 1);
      firstDate = parseDate(firstDate);
    }


    for (let i = 0; i < pomos.length; i++) {

      let date = new Date(Date.parse(pomos[i]["created_at"]));
      date = parseDate(date);
      const pomo = pomos[i];

      if (aggregated[date]) {
        aggregated[date] += 1;
      } else {
        aggregated[date] = 1;
      }
    }
  });
  return aggregateToChart(aggregated, true);
}

function parseDate(date) {
  const year = date.getFullYear();
  let month = date.getMonth() + 1; // Month is 0-indexed
  let day = date.getDate();
  return `${year}-${month}-${day}`;
}


