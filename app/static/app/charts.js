import { token } from './user_settings.js';
import { getAllPomodoros } from './api_calls.js';

const months = [
  { name: "January", days: 31 },
  { name: "February", days: 28 },
  { name: "March", days: 31 },
  { name: "April", days: 30 },
  { name: "May", days: 31 },
  { name: "June", days: 30 },
  { name: "July", days: 31 },
  { name: "August", days: 31 },
  { name: "September", days: 30 },
  { name: "October", days: 31 },
  { name: "November", days: 30 },
  { name: "December", days: 31 }
];
// Add squares
const squares = document.querySelector('.squares');
const desctiptor = document.querySelector('.tag-squares');
const pomosData = await convertPomosToJSON().then((data) => {

  for (let i = 0; i < months.length; i++) {
    const month = months[i];
    for (let day = 1; day <= month.days; day++) {
      const count = pomosData[month][day];
      const level = convertToLevel(count);
      squares.insertAdjacentHTML('beforeend', `<li data-level="${level}"
      data-date="${month}-${day}" data-count="${count}"></li>`);
    }
  }
});

async function convertPomosToJSON() {

  const response = await fetch(`/api/${token}/get`)

  await response.json().then((pomos) => {


    let output = {
      January: {},
      February: {},
      March: {},
      April: {},
      May: {},
      June: {},
      July: {},
      August: {},
      September: {},
      October: {},
      November: {},
      December: {}
    };
    for (let i = 0; i < pomos.length; i++) {
      const pomo = pomos[i];
      console.log(pomo);
      const date = formatPythonDatetime(pomo.date);
      const month = date.split('-')[1];
      const day = date.split('-')[2].split('T')[0];
      if (output[date.month][date.day]) {
        output[month][day] += 1;
      } else {
        output[month][day] = 1;
      }
    }
    console.log(output);
    return output;
  });
}


function convertToLevel(pomos) {
  if (pomos === 0) {
    return 0;
  } else if (pomos < 4) {
    return 1;
  } else if (pomos < 7) {
    return 2;
  } else if (pomos < 10) {
    return 3;
  } else {
    return 4;
  }
}

function formatPythonDatetime(datetimeString) {
  const date = new Date(Date.parse(datetimeString));
  return serializeDate(date);
}

function serializeDate(date) {
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  const hours = date.getHours();
  const minutes = date.getMinutes();
  const seconds = date.getSeconds();

  return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
}



