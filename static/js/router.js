class Router {
    constructor() {
        this.init();
        this.loader = document.getElementById('loader-overlay');
        this.minLoadTime = 500;
        window.ScriptManager.updateActiveNavLink();
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
            
            const minLoadTimePromise = new Promise(resolve => 
                setTimeout(resolve, this.minLoadTime)
            );

            const fetchPromise = fetch(url).then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            });

            const [html] = await Promise.all([
                fetchPromise,
                minLoadTimePromise
            ]);
            
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            
            await new Promise((resolve) => {
                const mainContent = doc.querySelector('main');
                if (!mainContent) {
                    throw new Error('Main content not found in loaded page');
                }

                document.title = doc.title;
                document.querySelector('main').innerHTML = mainContent.innerHTML;

                const images = Array.from(document.querySelector('main').getElementsByTagName('img'));
                const imagePromises = images.map(img => {
                    if (img.complete) return Promise.resolve();
                    return new Promise(resolve => {
                        img.onload = resolve;
                        img.onerror = resolve; 
                    });
                });

                Promise.all(imagePromises).then(resolve);
            });

            this.updateActiveState(url);
            
            if (pushState) {
                history.pushState({}, '', url);
            }

            window.scrollTo({
                top: 0,
                behavior: 'instant'
            });

            await this.reinitializeScripts();
        } catch (error) {
            console.error('Error loading page:', error);
        } finally {
            this.hideLoader();
        }
    }

    updateActiveState(url) {
        window.ScriptManager.updateActiveNavLink();
    }

    async reinitializeScripts() {
        return new Promise((resolve) => {
            window.ScriptManager.initAll();
            setTimeout(resolve, 100);
        });
    }

    onPopState(e) {
        this.loadPage(window.location.href, false);
    }

    onClick(e) {
        const link = e.target.closest('a');
        
        if (!link || link.hasAttribute('data-no-router')) return;

        if (link && link.href && link.href.startsWith(window.location.origin) && 
            !link.hasAttribute('download') && 
            !link.getAttribute('target')) {
            e.preventDefault();

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

document.addEventListener('DOMContentLoaded', () => {
    window.router = new Router();
});
