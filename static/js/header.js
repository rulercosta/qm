var CSbody = document.querySelector("body");
const CSnavbarMenu = document.querySelector("#cs-navigation");
const CShamburgerMenu = document.querySelector("#cs-navigation .cs-toggle");
CShamburgerMenu.addEventListener('click', function() {
    CShamburgerMenu.classList.toggle("cs-active");
    CSnavbarMenu.classList.toggle("cs-active");
    CSbody.classList.toggle("cs-open");
    ariaExpanded();
});
function ariaExpanded() {
    const csUL = document.querySelector('#cs-expanded');
    const csExpanded = csUL.getAttribute('aria-expanded');
    if (csExpanded === 'false') {
        csUL.setAttribute('aria-expanded', 'true');
    } else {
        csUL.setAttribute('aria-expanded', 'false');
    }
}

document.addEventListener('scroll', (e) => { 
    const scroll = document.documentElement.scrollTop;
    if(scroll >= 100){
document.querySelector('body').classList.add('scroll')
    } else {
    document.querySelector('body').classList.remove('scroll')
    }
});
const dropDowns = Array.from(document.querySelectorAll('#cs-navigation .cs-dropdown'));
    for (const item of dropDowns) {
        const onClick = () => {
        item.classList.toggle('cs-active')
    }
    item.addEventListener('click', onClick)
    }

function enableDarkMode() {
	document.body.classList.add('dark-mode');
	localStorage.setItem('theme', 'dark');
}
function disableDarkMode() {
	document.body.classList.remove('dark-mode');
	localStorage.setItem('theme', 'light');
}
function detectColorScheme() {
	let theme = 'light';
	if (localStorage.getItem('theme')) {
		theme = localStorage.getItem('theme');
	}
	else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
		theme = 'dark';
	}
	theme === 'dark' ? enableDarkMode() : disableDarkMode();
}
detectColorScheme();
document.getElementById('dark-mode-toggle').addEventListener('click', () => {
	localStorage.getItem('theme') === 'light' ? enableDarkMode() : disableDarkMode();
});
document.addEventListener('DOMContentLoaded', function () {
  const currentUrl = window.location.pathname;
  const navLinks = document.querySelectorAll('.cs-nav a');
  navLinks.forEach(link => link.classList.remove('cs-active'));

  navLinks.forEach(link => {
    if (link.href.includes(currentUrl)) {
      link.classList.add('cs-active');
    }
  });
});
