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

async function aggregatedPomosByTag() {
  let aggregated = {};
  const response = await fetch(`/api/${path_username}/alltags`);
  await response.json().then((data) => {
      aggregated = data;
    });
  return aggregateToChart(aggregated);
}


function pomosPerHour() {
  let aggregated = {};

  const pomos = cacheDataPomos;

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
  if (theme === 'white') {
    return '#121212';
  } else {
    return '#efefef';
  }
}

function pomosPerDay() {
  let aggregated = {};

  const pomos = cacheDataPomos;
  console.log(pomos);

  if (!pomos.length) {
    return [0];
  }

  const keys = Object.keys(pomos);
  let firstDate = pomos[0]["created_at"];
  firstDate = formatDate(firstDate);
  let lastDate = pomos[pomos.length - 1]["created_at"];
  lastDate = formatDate(lastDate);
  console.log(lastDate, pomos[pomos.length - 1]["created_at"]);

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

  return aggregateToChart(aggregated, true);
}

function parseDate(date) {
  const year = date.getFullYear();
  let month = date.getMonth() + 1; // Month is 0-indexed
  let day = date.getDate();
  return `${year}-${month}-${day}`;
}

function formatDate(inputDate) {
  const parts = inputDate.split('T')[0].split('-');
  const year = parts[0];
  const month = parts[1];
  const day = parts[2];

  console.log(year, month, day);

  return `${year}-${month}-${day}`;
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

loadCacheData();