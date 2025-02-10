class Router {
    constructor() {
        this.init();
        this.loader = document.getElementById('loader-overlay');
        this.minLoadTime = 300; // reduced to 300ms for a snappier feel
    }

    init() {
        window.addEventListener('popstate', (e) => this.onPopState(e));
        document.addEventListener('click', (e) => this.onClick(e));
    }

    showLoader() {
        this.loader.classList.add('active');
    }

    hideLoader() {
        this.loader.classList.remove('active');
    }

    async loadPage(url, pushState = true) {
        try {
            this.showLoader();
            
            // Create a promise that resolves after minLoadTime
            const minLoadTimePromise = new Promise(resolve => 
                setTimeout(resolve, this.minLoadTime)
            );

            // Fetch the page
            const fetchPromise = fetch(url).then(response => response.text());

            // Wait for both minimum time and fetch to complete
            const [html] = await Promise.all([
                fetchPromise,
                minLoadTimePromise
            ]);
            
            // Parse the HTML string
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            
            // Update title
            document.title = doc.title;
            
            // Update content
            const content = doc.querySelector('main').innerHTML;
            document.querySelector('main').innerHTML = content;
            
            // Update active nav link
            document.querySelectorAll('.cs-nav a').forEach(link => {
                link.classList.remove('cs-active');
                if (link.href === window.location.href) {
                    link.classList.add('cs-active');
                }
            });

            // Push state to history if needed
            if (pushState) {
                history.pushState({}, '', url);
            }

            // Re-initialize any necessary scripts
            this.reinitializeScripts();
        } catch (error) {
            console.error('Error loading page:', error);
        } finally {
            this.hideLoader();
        }
    }

    reinitializeScripts() {
        // Re-initialize any page-specific JavaScript
        if (window.initFaqs) {
            window.initFaqs();
        }
        if (window.initSkipSection) {
            window.initSkipSection();
        }
    }

    onPopState(e) {
        this.loadPage(window.location.href, false);
    }

    onClick(e) {
        // Handle internal navigation links
        const link = e.target.closest('a');
        
        // Skip if no anchor found or if it has data-no-router attribute
        if (!link || link.hasAttribute('data-no-router')) return;

        if (link && link.href && link.href.startsWith(window.location.origin) && 
            !link.hasAttribute('download') && 
            !link.getAttribute('target')) {
            e.preventDefault();

            // Close hamburger menu if open
            const CShamburgerMenu = document.querySelector("#cs-navigation .cs-toggle");
            const CSnavbarMenu = document.querySelector("#cs-navigation");
            const CSbody = document.querySelector("body");
            if (CSnavbarMenu.classList.contains("cs-active")) {
                CShamburgerMenu.classList.remove("cs-active");
                CSnavbarMenu.classList.remove("cs-active");
                CSbody.classList.remove("cs-open");
                const csUL = document.querySelector('#cs-expanded');
                csUL.setAttribute('aria-expanded', 'false');
            }

            if (window.location.href !== link.href) {
                this.loadPage(link.href);
            }
        }
    }
}

// Initialize router after DOM loads
document.addEventListener('DOMContentLoaded', () => {
    window.router = new Router();
});
