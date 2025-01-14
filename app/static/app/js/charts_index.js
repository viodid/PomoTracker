import { username } from './user_settings.js';
import { getAllPomodoros } from './api_calls.js';
const date = new Date();
const keys = [
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
if (isLeapYear(date.getFullYear())) {
  keys[1].days = 29;
}
// Add squares
const squares = document.querySelector('.squares'); const desctiptor = document.querySelector('.tag-squares');
const selectedYear = document.querySelectorAll('.buttons-index-graph>span');
const currentYear = (new Date()).getFullYear();
createSquares(currentYear);


selectedYear.forEach((year) => {
  year.addEventListener('click', () => {
    const getYear = year.getAttribute('data-year');
    createSquares(getYear);
  });
});

function createSquares(year) {

  convertPomosToJSON(year).then((data) => {
    // check any childs and remove them
    while (squares.firstChild) {
      squares.removeChild(squares.firstChild);
    }
    // add empty cells for each day before January 1st
    const days_from_previous_year = (new Date(currentYear, 0, 1)).getDay();
    for (let i = 0; i < days_from_previous_year; i++) {
      squares.insertAdjacentHTML('beforeend', '<li data-level="0"></li>');
    }

    for (let i = 0; i < keys.length; i++) {
      const month = keys[i];
      for (let day = 1; day <= month.days; day++) {
        let count = data[month.name][day];
        if (typeof count === "undefined") count = 0;
        const level = convertToLevel(count);
        squares.insertAdjacentHTML('beforeend', `<li data-level="${level}"
        data-date="${month.name} ${day}" data-count="${count}"></li>`);
      }
    }
  })
    .then(() => {
      const tag_squares = document.querySelector('.tag-squares');
      const squares = document.querySelectorAll('.squares li');
      squares.forEach((square) => {
        square.addEventListener('mouseover', () => {
          const date = square.getAttribute('data-date');
          const count = square.getAttribute('data-count');
          if (!date) { tag_squares.innerHTML = ''; return };
          if (count > 0) {
            tag_squares.innerHTML = `${count} pomodoros on ${date}, ${year}`;
          } else {
            tag_squares.innerHTML = `No pomodoros on ${date}, ${year}`;
          }
        });
      });
    });
}




async function convertPomosToJSON(selectedYear) {

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

  toggleLoading(true);

  const response = await fetch(`/api/${username}/alldates`)

  await response.json().then((pomos) => {

    toggleLoading(false);

    const keys = Object.keys(output);

    for (let i = 0; i < pomos.length; i++) {

      const date = pomos[i];
      const year = date.split('-')[0];
      const month = parseInt(date.split('-')[1] - 1);
      const day = parseInt(date.split('-')[2].split('T')[0]);

      if (year == selectedYear) {
        if (output[keys[month]][day]) {
          output[keys[month]][day] += 1;
        } else {
          output[keys[month]][day] = 1;
        }
      }
    }
  });
  return output;
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

function isLeapYear(year) {
  if (year % 4 !== 0) {
    return false;
  }
  if (year % 100 === 0 && year % 400 !== 0) {
    return false;
  }
  return true;
}

function toggleLoading(show) {
  if (show === true) {
    document.querySelector('#loading-container').style.visibility = 'visible';
    document.querySelector('#loading-container').style.opacity = '1';
  } else {
    document.querySelector('#loading-container').style.visibility = 'hidden';
    document.querySelector('#loading-container').style.opacity = '0';
  }
}