class Router {
    constructor() {
        this.init();
        this.loader = document.getElementById('loader-overlay');
        this.minLoadTime = 800;
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
        const startTime = Date.now();
        try {
            this.showLoader();
            
            const fetchPromise = fetch(url).then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            });

            const [html] = await Promise.all([
                fetchPromise,
                new Promise(resolve => setTimeout(resolve, this.minLoadTime))
            ]);
            
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            
            const mainContent = doc.querySelector('main');
            if (!mainContent) {
                throw new Error('Main content not found in loaded page');
            }

            document.title = doc.title;
            document.querySelector('main').innerHTML = mainContent.innerHTML;

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
            const loadTime = Date.now() - startTime;
            if (loadTime < this.minLoadTime) {
                await new Promise(resolve => setTimeout(resolve, this.minLoadTime - loadTime));
            }
            this.hideLoader();
        }
    }

    updateActiveState(url) {
        window.ScriptManager.updateActiveNavLink();
    }

    async reinitializeScripts() {
        return new Promise(resolve => {
            window.ScriptManager.initAll();
            resolve();
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
