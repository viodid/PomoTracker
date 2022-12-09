const minutes = document.querySelector('#minute');
const seconds = document.querySelector('#second');

function checkFormat(time) {
  if (time < 10) {
    return (`0${time.toString()}`);
  }

  return time.toString();
}

function formatHour() {
  const date = new Date();
  let hour = date.getHours();
  let minute = date.getMinutes();

  // Format hours to 12 time format
  if (hour > 12) {
    hour -= 12;

    if (hour < 10) {
      hour = `0${hour.toString()}`;
    } else if (minute < 10) minute = `0${minute.toString()}`;

    hour = `${hour.toString()}:${minute.toString()} PM`;
  } else hour = `${hour.toString()}:${minute.toString()} AM`;

  return hour.toString();
}

function formatTime(atStart, time) {
  const now = performance.now();
  const milliseconds = now - atStart;

  const secondsLeft = Math.ceil((time * 60) - milliseconds / 1000);

  let min = Math.floor(secondsLeft / 60);
  let sec = secondsLeft % 60;
  if (sec === 0) {
    min -= 1;
    sec = 60;
  }

  if (sec <= 0 && min <= 0) {
    return ['00', '00'];
  }

  sec -= 1;
  min = checkFormat(min);
  sec = checkFormat(sec);

  // Change title dynamically
  const { title } = document;
  document.title = `${min}:${sec} | ${title.slice(title.length - 11, title.length)}`;

  return [min, sec];
}

function changeLabels(change) {
  const parent = document.querySelector('.fill-data');
  if (change) {
    parent.querySelector('#cancel').style.display = 'none';
    parent.querySelector('#save').style.display = 'block';
    parent.querySelector('.last-text').innerHTML = 'or press enter';
    parent.querySelector('.focus').style.display = 'none';
    parent.querySelector('.text-input').style.display = 'block';
    parent.querySelector('.text-input').focus();
  } else {
    parent.querySelector('#cancel').style.display = 'block';
    parent.querySelector('#save').style.display = 'none';
    parent.querySelector('.last-text').innerHTML = 'or press ESC';
    parent.querySelector('.focus').style.display = 'block';
    parent.querySelector('.text-input').style.display = 'none';
  }
}

function sumCountPomodoros(classes) {
  classes.forEach((c) => {
    const node = document.querySelector(c);
    const child = node.querySelector('.right');
    child.innerHTML = (parseInt(child.innerHTML, 10) + 1).toString();
  });
}

function appendPomodoro(tag) {
  const hour = formatHour();

  const parent = document.querySelector('.todays-pomodoros');
  const node = parent.lastElementChild.cloneNode(true);
  parent.lastElementChild.classList.remove('last');
  node.lastElementChild.innerHTML = tag.toUpperCase();
  node.firstElementChild.innerHTML = hour;
  parent.appendChild(node);

  sumCountPomodoros(['.today', '.week', '.month', '.year']);
}

function renderTimer(time, color) {
  minutes.innerHTML = time.toString();
  seconds.innerHTML = '00';

  const timeToSeconds = time * 60;

  const sheet = window.document.styleSheets[0];
  sheet.insertRule('svg circle.meter {'
    + `filter: drop-shadow(0 0 3px ${color});`
    + `stroke: ${color};`
    + `animation: prog ${timeToSeconds}s linear forwards`
    + '}', sheet.cssRules.length);
}

export {
  appendPomodoro,
  changeLabels,
  formatTime,
  renderTimer,
};
