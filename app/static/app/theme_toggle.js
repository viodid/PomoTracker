export function switchDarkMode() {
  const token = document.querySelector('#token').value;

  const bodyclass = document.querySelector('body').classList;
  let submit;
  if (bodyclass.value.includes('white')) {
    bodyclass.remove('white');
    submit = 'default';
  } else {
    bodyclass.add('white');
    submit = 'white';
  }
  fetch(`/api/${token}/settings`, {
    method: 'PUT',
    body: JSON.stringify({
      white_theme: submit,
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
