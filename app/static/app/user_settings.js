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

let bColor = '#ADFF2F';
let fColor = '#f1c232';
let bTime = 5;
let fTime = 25;
let staSound = '#ding';
let stoSound = '#whoosh';
let user = null;
let theme = false;
let tkn = htmlToken;

const settings = getSettings(htmlToken);

if (settings) {
  bColor =    await settings.then((result) => result.breakColor);
  fColor =    await settings.then((result) => result.focusColor);
  bTime =     await settings.then((result) => result.breakTime);
  fTime =     await settings.then((result) => result.focusTime);
  staSound =  await settings.then((result) => result.startSound);
  stoSound =  await settings.then((result) => result.stopSound);
  user =      await settings.then((result) => result.user);
  theme =     await settings.then((result) => result.white_theme);
  tkn =     await settings.then((result) => result.token);
}

const breakColor = bColor;
const focusColor = fColor;
const breakTime = bTime;
const focusTime = fTime;
const startSound = staSound;
const stopSound = stoSound;
const username = user;
const whiteTheme = theme;
const token = tkn;

export {
  breakColor,
  focusColor,
  breakTime,
  focusTime,
  startSound,
  stopSound,
  username,
  whiteTheme,
  token,
};
