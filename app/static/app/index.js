document.addEventListener('DOMContentLoaded', function () {

    const overlay = document.querySelector('#overlay');
    overlay.style.visibility = 'hidden';
    const timer = new Timer();

    document.querySelector('#start').addEventListener('click', () => {

        display_overlay(overlay, timer);
    })

    document.querySelector('#cancel').addEventListener('click', () => {

        display_overlay(overlay, timer)
        play_sound(document.querySelector('#whoosh'))
    })

    document.addEventListener('keydown', event => {

        if (event.code === 'Space' && overlay.style.visibility === 'hidden') {
            display_overlay(overlay, timer);

        } else if (event.code === 'Escape' && overlay.style.visibility === 'visible') {
            display_overlay(overlay, timer);
            play_sound(document.querySelector('#whoosh'))
        }
    })
})

function display_overlay(overlay, timer, hide=false) {

    // Reset timer to 25 minutes in the background
    if (hide === true) {
        document.querySelector('#minute').innerHTML = '25';
        stop_animation();
        // reset_timer()
        overlay.style.visibility = 'hidden';
        overlay.style.opacity = 0;
    }
    else if (overlay.style.visibility === 'hidden') {
        start_animation()
        overlay.style.visibility = 'visible';
        overlay.style.opacity = 0.97;
        render_timer(timer);

    } else {
        alert('Sure?');
        play_sound(document.querySelector('#whoosh'))
        stop_animation();
        // reset_timer();
        overlay.style.visibility = 'hidden';
        overlay.style.opacity = 0;
    }
}

function render_timer(timer) {
    console.log(timer)

    // Execute function if clicking timer is turned on
   // play_sound('clicking')

    const minutes = document.querySelector('#minute');
    const seconds = document.querySelector('#second');

    // Change clock when finished
    if (minutes.innerHTML === '00' && seconds.innerHTML === '00') {
        play_sound(document.querySelector('#ding'));
        clearTimeout(timer.interval);
        change_timer(minutes, timer)
        timer.phase === 'focus' ? timer.phase = 'break' : timer.phase = 'focus'
    }

    [minutes.innerHTML, seconds.innerHTML]  = format_time(minutes.innerHTML, seconds.innerHTML);
    timer.interval = setTimeout(render_timer, 1000, timer);
}

function change_timer(minutes, timer) {


    if (timer.phase === 'focus') {
        const cycle = document.querySelector('#today').innerHTML

        if (parseInt(cycle) % 4 === 0) {
            minutes.innerHTML = '15';
        } else minutes.innerHTML = '02';

        document.querySelector('.focus').innerHTML = 'Break';

        // Stop timer from counting
        clearInterval(timer.interval)

        const user_logged = document.querySelector('#user-logged')

        // Check if user is logged in to save the pomodoro
        if (user_logged.innerHTML === 'Sign Out') {
            save_pomodoro();
        }
    } else {
        display_overlay(document.querySelector('#overlay'), hide=true)
    }
}

function save_pomodoro() {
    // Show tag input form
    console.log('ahora si, al final, save_pomodoro')

    // Save pomodoro to the API

    // Hide tag input form

    // Start over break timer countdown
    //render_timer(timer)
}

function play_sound(sound) {
    sound.play()
}

function format_time(minutes, seconds) {
    minutes = parseInt(minutes);
    seconds = parseInt(seconds);

    if (seconds === 0) {
        minutes -= 1
        seconds = 60
    }

    seconds -= 1
    minutes = check_format(minutes);
    seconds = check_format(seconds);
    return [minutes, seconds]
}

function check_format(time) {

    if (time < 10) {
        return ('0' + time.toString())
    }

    return time.toString()
}

function start_animation(time, color) {
    const sheet = window.document.styleSheets[0];
    sheet.insertRule('svg circle.meter { animation: prog 61s linear forwards, glow 1s 61s ease-in-out forwards; }', sheet.cssRules.length);
}

function stop_animation() {
    return true
}

class Timer {
    constructor() {
        this.interval = null;
        this.phase= 'focus';
    }
}