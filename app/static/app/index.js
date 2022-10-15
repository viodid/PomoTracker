document.addEventListener('DOMContentLoaded', function () {

    const overlay = document.querySelector('#overlay')
    overlay.style.visibility = 'hidden'

    document.querySelector('#start').addEventListener('click', () => {
        display_overlay(overlay);
    })

    document.querySelector('#cancel').addEventListener('click', () => {
        display_overlay(overlay)
        //reset_timer()
    })

    document.addEventListener('keydown', event => {
        if (event.code === 'Space' && overlay.style.visibility === 'hidden') {
            display_overlay(overlay);
        } else if (event.code === 'Escape' && overlay.style.visibility === 'visible') {
            display_overlay(overlay);
            //reset_timer()
        }
    })
})

function display_overlay(element) {
    if (element.style.visibility === 'hidden') {
        element.style.visibility = 'visible';
        element.style.opacity = 0.97;
    } else {
        alert('Sure?');
        element.style.visibility = 'hidden';
        element.style.opacity = 0;
    }
}