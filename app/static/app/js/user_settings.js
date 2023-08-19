/* eslint-disable no-multi-spaces */
const htmlToken = document.querySelector('#token').value;

function getSettings(tokenParam) {
  if (!tokenParam) return null;
  const settings = fetch(`/api/${tokenParam}/getSettings`)
    .then((response) => {
      if (response.status !== 200) return null;
      return response.json();
    })
    .then((data) => data);
  return settings;
}

let bColor    = '#ADFF2F';
let fColor    = '#f1c232';
let bTime     = 5;
let fTime     = 25;
let lBreak    = 15;
let staSound  = '#ding';
let stoSound  = '#whoosh';
let user      = null;
let preTheme  = 'default';
let img       = 'default';
let tkn       = htmlToken;

const settings = getSettings(htmlToken);

if (settings) {
  bColor    = await settings.then((result) => result.breakColor);
  fColor    = await settings.then((result) => result.focusColor);
  bTime     = await settings.then((result) => result.shortBreak);
  fTime     = await settings.then((result) => result.focusTime);
  lBreak    = await settings.then((result) => result.longBreak);
  staSound  = await settings.then((result) => result.startSound);
  stoSound  = await settings.then((result) => result.stopSound);
  user      = await settings.then((result) => result.user);
  preTheme  = await settings.then((result) => result.theme);
  img       = await settings.then((result) => result.image);
  tkn       = await settings.then((result) => result.token);
}

const breakColor = bColor;
const focusColor = fColor;
const shortBreak = bTime;
const focusTime = fTime;
const longBreak = lBreak;
const startSound = staSound;
const stopSound = stoSound;
const username = user;
const theme = preTheme;
const image = img;
const token = tkn;


export {
  breakColor,
  focusColor,
  shortBreak,
  focusTime,
  longBreak,
  startSound,
  stopSound,
  username,
  theme,
  image,
  token,
};
