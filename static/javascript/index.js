
const colors = ['#ffecd6', '#d6f5ff', '#ffd6f5', '#f5ffd6', '#d6d6ff', '#ffd6d6'];

function getRandomColor() {
    return colors[Math.floor(Math.random() * colors.length)];
}

// Change background color on page load
document.addEventListener('DOMContentLoaded', function() {
    document.body.style.backgroundColor = getRandomColor();
});