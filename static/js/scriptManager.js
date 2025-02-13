class ScriptManager {
    static #menuInitialized = false;
    static #carouselInstances = [];
    static #photoCarousel = null;

    static initFaqs() {
        const faqItems = Array.from(document.querySelectorAll('.cs-faq-item'));
        for (const item of faqItems) {
            const onClick = () => {
                item.classList.toggle('active')
            }
            item.addEventListener('click', onClick)
        }
    }

    static initSkipSection() {
        const viewAllLink = document.getElementById('view-all-btn');
        if (viewAllLink) {
            viewAllLink.addEventListener('click', (event) => {
                event.preventDefault();
                const nextSection = document.getElementById('cs-contact-549');
                nextSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            });
        }
    }

    static initHeader() {
        this.cleanupHeader();
        
        const body = document.querySelector("body");
        const nav = document.querySelector("#cs-navigation");
        const toggle = document.querySelector(".cs-toggle");
        const menu = document.querySelector(".cs-ul-wrapper");
        
        if (toggle && menu && !this.#menuInitialized) {
            const toggleMenu = () => {
                toggle.classList.toggle("cs-active");
                nav.classList.toggle("cs-active");
                body.classList.toggle("cs-open");
                const isExpanded = nav.classList.contains("cs-active");
                menu.querySelector('.cs-ul').setAttribute("aria-expanded", isExpanded.toString());
            };

            const closeMenu = () => {
                toggle.classList.remove("cs-active");
                nav.classList.remove("cs-active");
                body.classList.remove("cs-open");
                menu.querySelector('.cs-ul').setAttribute("aria-expanded", "false");
            };

            const menuLinks = menu.querySelectorAll('a.cs-li-link');
            menuLinks.forEach(link => {
                link.addEventListener('click', (e) => {
                    closeMenu();
                });
                link._closeHandler = closeMenu;
            });

            toggle.addEventListener('click', toggleMenu);
            toggle._toggleHandler = toggleMenu;
            toggle._closeHandler = closeMenu;
        }

        const dropDowns = document.querySelectorAll('.cs-dropdown');
        dropDowns.forEach(item => {
            const toggleDropdown = () => item.classList.toggle('cs-active');
            item.addEventListener('click', toggleDropdown);
            item._dropdownHandler = toggleDropdown;
        });

        const handleScroll = () => {
            const scroll = document.documentElement.scrollTop;
            body.classList.toggle('scroll', scroll >= 100);
        };
        document.addEventListener('scroll', handleScroll);
        this._scrollHandler = handleScroll;

        this.initDarkMode();

        this.#menuInitialized = true;
    }

    static initDarkMode() {
        const toggle = document.getElementById('dark-mode-toggle');
        if (!toggle) return;

        const enableDarkMode = () => {
            document.body.classList.add('dark-mode');
            localStorage.setItem('theme', 'dark');
        };

        const disableDarkMode = () => {
            document.body.classList.remove('dark-mode');
            localStorage.setItem('theme', 'light');
        };

        const theme = localStorage.getItem('theme') || 
                     (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        theme === 'dark' ? enableDarkMode() : disableDarkMode();

        const toggleDarkMode = () => {
            localStorage.getItem('theme') === 'light' ? enableDarkMode() : disableDarkMode();
        };
        toggle.addEventListener('click', toggleDarkMode);
        toggle._darkModeHandler = toggleDarkMode;
    }

    static cleanupHeader() {
        const toggle = document.querySelector(".cs-toggle");
        if (toggle && toggle._toggleHandler) {
            toggle.removeEventListener('click', toggle._toggleHandler);
        }

        const dropDowns = document.querySelectorAll('.cs-dropdown');
        dropDowns.forEach(item => {
            if (item._dropdownHandler) {
                item.removeEventListener('click', item._dropdownHandler);
            }
        });

        if (this._scrollHandler) {
            document.removeEventListener('scroll', this._scrollHandler);
        }

        const darkModeToggle = document.getElementById('dark-mode-toggle');
        if (darkModeToggle && darkModeToggle._darkModeHandler) {
            darkModeToggle.removeEventListener('click', darkModeToggle._darkModeHandler);
        }

        const menuLinks = document.querySelectorAll('.cs-ul-wrapper a.cs-li-link');
        menuLinks.forEach(link => {
            if (link._closeHandler) {
                link.removeEventListener('click', link._closeHandler);
            }
        });

        this.#menuInitialized = false;

        this.#carouselInstances.forEach(instance => {
            if (instance && instance.destroy) {
                instance.destroy(true, true);
            }
        });
        this.#carouselInstances = [];

        if (this.#photoCarousel) {
            this.#photoCarousel.cleanup();
        }
        this.#menuInitialized = false;
    }

    static updateActiveNavLink() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.cs-nav .cs-li-link');
        
        navLinks.forEach(link => {
            link.classList.remove('cs-active');
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('cs-active');
            }
        });
    }

    static initPhotoCarousels() {
        if (document.querySelector('.photo-carousel')) {
            if (!this.#photoCarousel) {
                this.#photoCarousel = new PhotoCarousel();
            }
            this.#photoCarousel.init();
        }
    }

    static initAll() {
        this.initHeader();
        this.initFaqs();
        this.initSkipSection();
        this.updateActiveNavLink();
        this.initPhotoCarousels();
    }
}

window.ScriptManager = ScriptManager;

document.addEventListener('DOMContentLoaded', () => {
    ScriptManager.initAll();
});
