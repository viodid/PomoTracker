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
  let output;

  // Format hours to 12 time format
  if (hour > 12) {
    hour -= 12;
    if (minute < 10) minute = `0${minute.toString()}`;
    if (hour < 10) hour = `0${hour.toString()}`;
    output = `${hour.toString()}:${minute.toString()} PM`;
  } else {
    if (hour < 10) hour = `0${hour.toString()}`;
    if (minute < 10) minute = `0${minute.toString()}`;
    output = `${hour.toString()}:${minute.toString()} AM`;
  }

  return output;
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

  const { title } = document;

  if (sec <= 0 && min <= 0) {
    // Change title to 00:00 
    document.title = `00:00 | ${title.slice(title.length - 11, title.length)}`;
    return ['00', '00'];
  }

  sec -= 1;
  min = checkFormat(min);
  sec = checkFormat(sec);

  // Change title dynamically
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

function checkNoPomodoros() {
  const node = document.querySelector('.today');
  const child = node.querySelector('.right');
  if (child.innerHTML === '0') {
    return true;
  }
  return false;
}

function appendPomodoro(tag) {
  const hour = formatHour();

  const parent = document.querySelector('#todays-index');
  const node = parent.lastElementChild.cloneNode(true);
  parent.lastElementChild.classList.remove('last');
  node.lastElementChild.innerHTML = tag.toUpperCase();
  node.firstElementChild.innerHTML = hour;
  parent.appendChild(node);
  if (checkNoPomodoros()) {
    const title = parent.firstElementChild;
    title.nextElementSibling.remove();
  }
  parent.lastElementChild.classList.add('last');

  sumCountPomodoros(['.today', '.week', '.month', '.year']);
}

function renderTimer(time, color) {
  const timeToSeconds = time * 60;

  const sheet = window.document.styleSheets[0];
  sheet.insertRule(`svg circle.meter {
    filter: drop-shadow(0 0 3px ${color});
    stroke: ${color};
    stroke-dashoffset: 49px;
    stroke-dasharray: 300px;
    animation: ${timeToSeconds}s linear 0s 1 normal forwards running prog,
    1s ease-in-out ${timeToSeconds}s 1 normal forwards running glow;
    }`, sheet.cssRules.length);
  // console.log(sheet.cssRules.length, sheet, timeToSeconds, color);
}

export {
  appendPomodoro,
  changeLabels,
  formatTime,
  renderTimer,
};
