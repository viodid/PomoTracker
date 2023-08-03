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
