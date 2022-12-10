export function switchDarkMode() {
  document.body.classList.toggle('white-theme');
  const token = document.querySelector('#token').value;
  let white = document.querySelector('body').classList;
  // eslint-disable-next-line no-unused-expressions
  white.value === 'white-theme' ? white = true : white = false;

  fetch(`/api/${token}/settings`, {
    method: 'PUT',
    body: JSON.stringify({
      white_theme: white,
    }),
  });
}

// Change image: lightbulb/moon
export function changeLightbulb() {
  const lightbulb = document.querySelector('#lightbulb');
  const moon = document.querySelector('#moon');
  if (lightbulb.style.display === 'block') {
    lightbulb.style.display = 'none';
    moon.style.display = 'block';
  } else {
    lightbulb.style.display = 'block';
    moon.style.display = 'none';
  }
}
