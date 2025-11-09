// theme toggle button
const toggleButton = document.createElement('button');
toggleButton.innerHTML = '🌙'; // default icon
toggleButton.className = 'theme-toggle';
document.body.appendChild(toggleButton);

// theme toggle styles
const style = document.createElement('style');
style.textContent = `
.theme-toggle {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  font-size: 1.3rem;
  font-weight: bold;
  color: #fff;
  background-color: var(--accent-light);
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  transition: all 0.3s ease;
  z-index: 1000;
}
.theme-toggle:hover {
  transform: scale(1.1);
  filter: brightness(1.1);
}
body.darkmode .theme-toggle {
  background-color: var(--accent-dark);
}

/* === SMOOTH THEME TRANSITION === */
body {
  transition: background 0.6s ease, color 0.6s ease, filter 0.6s ease;
}
.container, h1, h2, input, .btn, footer {
  transition: background 0.6s ease, color 0.6s ease, border-color 0.6s ease;
}
`;
document.head.appendChild(style);

// load saved theme from localStorage
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'darkmode') {
    document.body.classList.remove('lightmode');
    document.body.classList.add('darkmode');
    toggleButton.innerHTML = '☀️';
} else {
    document.body.classList.remove('darkmode');
    document.body.classList.add('lightmode');
    toggleButton.innerHTML = '🌙';
}

// toggle theme on click
toggleButton.addEventListener('click', () => {
    document.body.classList.add('fade-theme');
    if (document.body.classList.contains('darkmode')) {
        document.body.classList.remove('darkmode');
        document.body.classList.add('lightmode');
        localStorage.setItem('theme', 'lightmode');
        toggleButton.innerHTML = '🌙';
    } else {
        document.body.classList.remove('lightmode');
        document.body.classList.add('darkmode');
        localStorage.setItem('theme', 'darkmode');
        toggleButton.innerHTML = '☀️';
    }
    setTimeout(() => document.body.classList.remove('fade-theme'), 600);
});
