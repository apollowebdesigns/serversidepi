function log(ev) {
    console.log(ev);
}

document.body.addEventListener('touchstart', log, false);
document.body.addEventListener('touchmove', log, false);
document.body.addEventListener('touchend', log, false);