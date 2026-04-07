import { editTag } from './api_calls.js';
import { token } from './user_settings.js';

const tags = document.querySelectorAll('#tag');
tags.forEach((tag) => {
  const id = tag.querySelector('#tag-id').value;

  tag.querySelector('#edit-tag').addEventListener('click', () => {
    tag.querySelector('#edit-tag').style.display = 'none';
    tag.querySelector('#save-tag').style.display = 'initial';
    tag.querySelector('#tag-display').style.display = 'none';
    tag.querySelector('#text-input').style.display = 'initial';
  });

  tag.querySelector('#save-tag').addEventListener('click', () => {
    let tag_val = tag.querySelector('#text-input').value;
    if (tag_val.length > 0) {
      editTag(token, id, tag_val);
      tag_val = tag_val.toUpperCase();
      tag_val = tag_val.replaceAll(' ', '_');
      tag.querySelector('#tag-display').textContent = tag_val;
    }
    tag.querySelector('#edit-tag').style.display = 'initial';
    tag.querySelector('#save-tag').style.display = 'none';
    tag.querySelector('#tag-display').style.display = 'initial';
    tag.querySelector('#text-input').style.display = 'none';
  });
})

// Sound preview playback
document.querySelectorAll('.sound-preview-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const selectName = btn.dataset.target;
    const select = document.querySelector(`[name="${selectName}"]`);
    if (!select) return;
    const audioId = select.value.replace('#', '');
    const audio = document.getElementById(audioId);
    if (audio) {
      audio.currentTime = 0;
      audio.play();
    }
  });
});

// Image preview on file select
const imageInput = document.querySelector('.settings-file-input');
if (imageInput) {
  imageInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (ev) => {
        const preview = document.getElementById('avatar-preview');
        if (preview) preview.src = ev.target.result;
      };
      reader.readAsDataURL(file);
    }
  });
}

// Live theme preview
const themeSelect = document.getElementById('theme-select');
if (themeSelect) {
  const originalTheme = document.body.className;
  themeSelect.addEventListener('change', () => {
    document.body.className = themeSelect.value === 'default' ? '' : themeSelect.value;
  });
}

// Timezone search filter
const tzSelect = document.getElementById('timezone-select');
if (tzSelect) {
  const allOptions = Array.from(tzSelect.options).map(opt => ({
    value: opt.value,
    text: opt.text,
    selected: opt.selected
  }));

  const searchInput = document.createElement('input');
  searchInput.type = 'text';
  searchInput.placeholder = 'Search timezone...';
  searchInput.className = 'settings-input tz-search-input';
  tzSelect.parentNode.insertBefore(searchInput, tzSelect);

  searchInput.addEventListener('input', () => {
    const query = searchInput.value.toLowerCase();
    const currentValue = tzSelect.value;
    tzSelect.innerHTML = '';
    allOptions.forEach(opt => {
      if (opt.text.toLowerCase().includes(query)) {
        const option = document.createElement('option');
        option.value = opt.value;
        option.text = opt.text;
        option.selected = opt.value === currentValue;
        tzSelect.appendChild(option);
      }
    });
  });
}
