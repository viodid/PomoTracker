document.addEventListener('DOMContentLoaded', function () {

    const overlay = document.querySelector('#overlay');
    overlay.style.visibility = 'hidden';
    const timer = new Timer();

    document.querySelector('#start').addEventListener('click', () => {
        display_overlay(overlay);
        render_timer(timer);
    })

    document.querySelector('#cancel').addEventListener('click', () => {
        display_overlay(overlay)
        clearInterval(timer.interval)
    })

    document.addEventListener('keydown', event => {
        if (event.code === 'Space' && overlay.style.visibility === 'hidden') {
            display_overlay(overlay);
            render_timer(timer);
        } else if (event.code === 'Escape' && overlay.style.visibility === 'visible') {
            display_overlay(overlay);
            clearInterval(timer.interval)
        }
    })
})

function display_overlay(element, hide=false) {
    if (hide === true) {
        document.querySelector('#minute').innerHTML = '25';
        element.style.visibility = 'hidden';
        element.style.opacity = 0;
    }
    if (element.style.visibility === 'hidden') {
        element.style.visibility = 'visible';
        element.style.opacity = 0.97;
    } else {
        alert('Sure?');
        element.style.visibility = 'hidden';
        element.style.opacity = 0;
    }
}

function render_timer(timer) {

    const minutes = document.querySelector('#minute');
    const seconds = document.querySelector('#second');

    // Change clock when finished
    if (minutes.innerHTML === '00' && seconds.innerHTML === '00') {
        clearTimeout(timer.interval);
        change_time(minutes, timer)
        timer.phase === 'focus' ? timer.phase = 'break' : timer.phase = 'focus'
        return
    }

    [minutes.innerHTML, seconds.innerHTML]  = format_time(minutes.innerHTML, seconds.innerHTML);
    timer.interval = setTimeout(render_timer, 1000, timer);
}

function change_time(minutes, timer) {

    play_sound(document.querySelector('#ding'));

    if (timer.phase === 'focus') {
        const cycle = document.querySelector('#today').innerHTML

        if (parseInt(cycle) % 4 === 0) {
            minutes.innerHTML = '15';
        } else minutes.innerHTML = '05';

        document.querySelector('.focus').innerHTML = 'Break';
        const user_logged = document.querySelector('#user-logged')

        // Check if user is logged in to save the pomodoro
        if (user_logged.innerHTML === 'Sign Out') {
            save_pomodoro(timer);
        }
    } else {
        display_overlay(element=document.querySelector('#overlay'), hide=true)
    }
}

function save_pomodoro(timer) {
    // Show tag input form
    console.log('ahora si, al final, save_pomodoro')

    // Save pomodoro to the API

    // Hide tag input form

    // Start over break timer countdown
    render_timer(timer)
}

function play_sound(sound) {
    sound.play()
}

function format_time(minutes, seconds) {
    console.log(minutes, seconds)
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



class Timer {
    constructor() {
        this.interval = null;
        this. phase= 'focus';
    }
}