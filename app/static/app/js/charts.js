import { focusColor, username, theme } from './user_settings.js';

google.charts.load('current', {'packages':['corechart']});

let cacheDataPomos = null;


async function renderCharts() {
  //google.charts.setOnLoadCallback(drawTimeline1);
  google.charts.setOnLoadCallback(drawBarChart1);
  google.charts.setOnLoadCallback(drawBarChart2);
}

let path_username = window.location.pathname.split('/')[1];
if (path_username === 'charts') {
  path_username = username;
}

// Timeline tags
async  function drawTimeline1() {
  const pomos = await aggregatedPomosByTag()
    .then((pomos) => {
      const data = new google.visualization.DataTable();
      data.addColumn({ type: 'string', id: 'Tag' });
      data.addColumn({ type: 'date', id: 'Start' });
      data.addColumn({ type: 'date', id: 'End' });




      const chart = new google.visualization.PieChart(document.getElementById('timeline-chart'));
      chart.draw(data, options);
    });
}

// Pomodoros per Hour
function drawBarChart1() {
  const pomos = pomosPerHour()
  const data = new google.visualization.DataTable();
  data.addColumn('string', 'Hour');
  data.addColumn('number', 'Count');
  data.addRows(pomos);

  const options = {
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
      fill: 'transparent',
    },
    bar: { groupWidth: '75%' },
    chartArea: {
      width: '85%',
      height: '75%'
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

  const chart = new google.visualization.ColumnChart(document.getElementById('bar-chart-first'));
  chart.draw(data, options);
}

// Pomodoros per Day
function drawBarChart2() {
  const pomos = pomosPerDay()
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
      fill: 'transparent',
    },
    bar: { groupWidth: "90%" },
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
  };

    var chart = new google.visualization.ColumnChart(document.getElementById('bar-chart-second'));
    chart.draw(data, options);
}

async function drawPieChart1() {
  const pomos = await aggregatedPomosByTag()
  .then((pomos) => {
    const data = new google.visualization.DataTable();
    data.addColumn('string', 'Tag');
    data.addColumn('number', 'Count');
    data.addRows(pomos);

    const options = {
        title: 'Pomodoros by Tag',
        fontName: 'Roboto',
        titleTextStyle: {
          color: fontColor(),
          fontSize: 22,
          bold: false,
        },
        legend: {
          position: 'none',
          textStyle: {
            color: fontColor(),
          },
        },
        backgroundColor: {
          fill:'transparent',
        },
        chartArea: {
          width: "87%",
          height: "87%",
          left: 40,
          right: 40,
        },
        is3D: true,
        sliceVisibilityThreshold: 0.01,
        pieSliceText: 'label',
        tooltip: {
          showColorCode: true,
          ignoreBounds: true,
        },
      }

    const chart = new google.visualization.PieChart(document.getElementById('pie-chart'));
    chart.draw(data, options);
  });
}

function pomosPerHour() {
  let aggregated = {};

  const pomos = cacheDataPomos;

  // initialize the 24 hours
  for (let i = 0; i < 24; i++) {
    aggregated[i] = 0;
  }

  for (let i = 0; i < pomos.length; i++) {

    const hour = parseInt(getHour(pomos[i]["created_at"]));

    if (aggregated[hour]) {
      aggregated[hour] += 1;
    } else {
      aggregated[hour] = 1;
    }
  }
  return aggregateToChart(aggregated);
}

function getHour(dateString) {
  const date = new Date(dateString);
  return `${date.getHours()}:${date.getMinutes()}`
}

function pomosPerDay() {
  let aggregated = {};
  const pomos = cacheDataPomos;


  for (let i = 0; i < pomos.length; i++) {
    const date = new Date(getDate(pomos[i]["created_at"]));
    console.log(date);

    if (aggregated[date]) {
      aggregated[date] += 1;
    } else {
      aggregated[date] = 1;
    }
  }
  return aggregateToChart(aggregated, true);
}

function getDate(dateString) {
  const date = new Date(dateString);
  // Format the date to "YYYY-MM-DD"
  return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
}

async function loadCacheData() {
  if (document.getElementById('pie-chart')) {
    google.charts.setOnLoadCallback(drawPieChart1);
  }
  fetch(`/api/${path_username}/allpomodoros`)
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    cacheDataPomos = data;
    renderCharts(data);
  });
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

async function aggregatedPomosByTag() {
  let aggregated = {};
  const response = await fetch(`/api/${path_username}/alltags`);
  await response.json().then((data) => {
      aggregated = data;
    });
  return aggregateToChart(aggregated);
}

function fontColor() {
  if (theme === 'white') {
    return '#121212';
  } else {
    return '#efefef';
  }
}

loadCacheData();