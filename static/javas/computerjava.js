// after a lag time show computer move and go to user_turn page
document.addEventListener('DOMContentLoaded', function() {
    var move = document.getElementsByTagName('var');
    var cell = document.getElementById(move[0].innerHTML);
    cell.style.fontSize = '6vh';
    var x = "/user_turn/" + move[0].innerHTML;
    setTimeout(() => {
        cell.innerHTML = 'O';
    }, 1000);
    setTimeout(() => {
        window.location.replace(x);
    }, 2000);
}, false);
