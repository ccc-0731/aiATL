// select toggle button
const toggleButton = document.createElement('button');
toggleButton.textContent = 'Toggle Dark Mode';
toggleButton.className = 'btn btn-custom';
toggleButton.style.position = 'fixed';
toggleButton.style.bottom = '20px';
toggleButton.style.right = '20px';
toggleButton.style.zIndex = '1000';
document.body.appendChild(toggleButton);

// load user's theme from localstorage
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    document.body.classList.add(savedTheme);
}


// add event listener to toggle button
toggleButton.addEventListener('click', () => {
    if (document.body.classList.contains('dark-mode')) {
        document.body.classList.remove('dark-mode');
        localStorage.setItem('theme', '');
    } else {
        document.body.classList.add('dark-mode');
        localStorage.setItem('theme', 'dark-mode');
    }
});