// if there is a winner or tie make background blue
document.addEventListener('DOMContentLoaded', function() {
    var mess = document.getElementById('message');
    if (mess.innerHTML !== 'x') {
        var cell = document.getElementById('all');
        cell.style.backgroundColor = 'SkyBlue';
    }
}, false);


// put user's token in cell after click then disable all other buttons
// after a pause go to computer_turn
function printx(event) {
    var button = event.srcElement;
    button.style.backgroundColor = 'white';
    button.innerHTML = 'X';
    button.style.fontSize = '6vh';
    button.style.border = 'None';

    var buttons = document.getElementsByTagName('button');
    for (var x = 0; x < buttons.length; x++) {
        buttons[x].setAttribute("disabled", true);
    }

    x = "/computer_turn/" + button.id
    setTimeout(() => {
        window.location.replace(x);
    }, 800);

}
