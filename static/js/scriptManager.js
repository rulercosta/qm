class ScriptManager {
    static #instances = {
        menuInitialized: false,
        carouselInstances: [],
        photoCarousel: null,
        eventHandlers: new Map()
    };

    static registerHandler(element, event, handler) {
        if (!element) return;
        
        element.addEventListener(event, handler);
        if (!this.#instances.eventHandlers.has(element)) {
            this.#instances.eventHandlers.set(element, []);
        }
        this.#instances.eventHandlers.get(element).push({ event, handler });
    }

    static initFaqs() {
        const faqItems = document.querySelectorAll('.cs-faq-item');
        faqItems.forEach(item => {
            const handler = () => item.classList.toggle('active');
            this.registerHandler(item, 'click', handler);
        });
    }

    static initSkipSection() {
        const viewAllLink = document.getElementById('view-all-btn');
        const handler = (event) => {
            event.preventDefault();
            document.getElementById('cs-contact-549')?.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        };
        this.registerHandler(viewAllLink, 'click', handler);
    }

    static initHeader() {
        const elements = {
            body: document.querySelector("body"),
            nav: document.querySelector("#cs-navigation"),
            toggle: document.querySelector(".cs-toggle"),
            menu: document.querySelector(".cs-ul-wrapper")
        };

        if (elements.toggle && elements.menu && !this.#instances.menuInitialized) {
            const toggleMenu = () => {
                elements.toggle.classList.toggle("cs-active");
                elements.nav.classList.toggle("cs-active");
                elements.body.classList.toggle("cs-open");
                elements.menu.querySelector('.cs-ul')
                    .setAttribute("aria-expanded", elements.nav.classList.contains("cs-active"));
            };

            const closeMenu = () => {
                elements.toggle.classList.remove("cs-active");
                elements.nav.classList.remove("cs-active");
                elements.body.classList.remove("cs-open");
                elements.menu.querySelector('.cs-ul').setAttribute("aria-expanded", "false");
            };

            this.registerHandler(elements.toggle, 'click', toggleMenu);
            
            elements.menu.querySelectorAll('a.cs-li-link').forEach(link => {
                this.registerHandler(link, 'click', closeMenu);
            });
        }

        // Initialize dropdowns
        document.querySelectorAll('.cs-dropdown').forEach(item => {
            this.registerHandler(item, 'click', () => item.classList.toggle('cs-active'));
        });

        // Initialize scroll handler
        const scrollHandler = () => {
            elements.body.classList.toggle('scroll', document.documentElement.scrollTop >= 100);
        };
        this.registerHandler(document, 'scroll', scrollHandler);

        this.initDarkMode();
        this.#instances.menuInitialized = true;
    }

    static initDarkMode() {
        const toggle = document.getElementById('dark-mode-toggle');
        if (!toggle) return;

        const setTheme = (theme) => {
            document.body.classList.toggle('dark-mode', theme === 'dark');
            localStorage.setItem('theme', theme);
        };

        const theme = localStorage.getItem('theme') || 
                     (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        setTheme(theme);

        this.registerHandler(toggle, 'click', () => 
            setTheme(localStorage.getItem('theme') === 'light' ? 'dark' : 'light')
        );
    }

    static cleanup() {
        // Clean up all registered event handlers
        this.#instances.eventHandlers.forEach((handlers, element) => {
            handlers.forEach(({ event, handler }) => {
                element.removeEventListener(event, handler);
            });
        });
        this.#instances.eventHandlers.clear();

        // Clean up carousels
        this.#instances.carouselInstances.forEach(instance => {
            instance?.destroy?.(true, true);
        });
        this.#instances.carouselInstances = [];

        // Clean up photo carousel
        this.#instances.photoCarousel?.cleanup();
        this.#instances.photoCarousel = null;

        // Reset initialization flags
        this.#instances.menuInitialized = false;
    }

    static updateActiveNavLink() {
        const currentPath = window.location.pathname;
        document.querySelectorAll('.cs-nav .cs-li-link').forEach(link => {
            link.classList.toggle('cs-active', link.getAttribute('href') === currentPath);
        });
    }

    static initPhotoCarousels() {
        if (!document.querySelector('.photo-carousel')) return;
        
        if (!this.#instances.photoCarousel) {
            this.#instances.photoCarousel = new PhotoCarousel();
        }
        this.#instances.photoCarousel.init();
    }

    static initAll() {
        this.cleanup();
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
