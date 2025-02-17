class Router {
    #config = {
        minLoadTime: 800,
        styleCache: new Map(),
        loader: null,
        loaderAnimation: null,
        isNavigating: false
    };

    constructor() {
        this.#config.loader = document.getElementById('loader-overlay');
        if (this.#config.loader) {
            this.#config.loaderAnimation = new LoaderAnimation(this.#config.loader);
            this.#config.loaderAnimation.initialize();
        }
        this.#initEventListeners();
        window.ScriptManager?.updateActiveNavLink();
    }

    #initEventListeners() {
        window.addEventListener('popstate', () => this.#handleNavigation(window.location.href, false));
        document.addEventListener('click', (e) => this.#handleClick(e));
    }

    async #handleNavigation(url, pushState = true) {
        const photoModal = document.getElementById('photo-modal');
        if (photoModal?.dataset.isOpen === 'true') {
            window.ScriptManager?.closePhotoModal();
        }

        if (this.#config.isNavigating) return;
        
        const startTime = Date.now();
        const mainContent = document.querySelector('main');
        
        try {
            mainContent.style.opacity = '0';
            await this.#showLoader();
            
            const content = await this.#loadContent(url);
            await this.#updatePage(content, url, pushState);
        } catch (error) {
            console.error('Navigation error:', error);
            mainContent.style.opacity = '1';
        } finally {
            await this.#ensureMinLoadTime(startTime);
            mainContent.style.opacity = '1';
            await this.#hideLoader();
            this.#config.isNavigating = false;
        }
    }

    async #showLoader() {
        if (!this.#config.loaderAnimation) return;
        
        this.#config.loaderAnimation.show();
        await new Promise(resolve => setTimeout(resolve, 300));
    }

    async #hideLoader() {
        if (this.#config.loaderAnimation) {
            this.#config.loaderAnimation.hide();
            await new Promise(resolve => setTimeout(resolve, 300));
        }
    }

    async #loadContent(url) {
        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            const html = await response.text();
            const doc = new DOMParser().parseFromString(html, 'text/html');
            
            if (!doc.querySelector('main')) {
                throw new Error('Invalid page content: missing main element');
            }
            
            return doc;
        } catch (error) {
            console.error('Content loading failed:', error);
            throw error;
        }
    }

    async #updatePage(doc, url, pushState) {
        await this.#loadStylesheets(doc);
        
        const newMain = doc.querySelector('main');
        const currentMain = document.querySelector('main');
        
        if (!newMain || !currentMain) throw new Error('Main content not found');
        
        if (pushState) history.pushState({}, '', url);
        document.title = doc.title;
        
        await PageTransition.crossFade(currentMain, newMain);
        
        window.scrollTo({ top: 0, behavior: 'instant' });
        await window.ScriptManager?.initAll();
    }

    async #loadStylesheets(doc) {
        const newStyles = Array.from(doc.getElementsByTagName('link'))
            .filter(link => 
                link.rel === 'stylesheet' && 
                !document.querySelector(`link[href="${link.href}"]`)
            );

        const stylePromises = newStyles.map(async (style) => {
            if (this.#config.styleCache.has(style.href)) {
                return this.#config.styleCache.get(style.href);
            }

            const newStyle = document.createElement('link');
            newStyle.rel = 'stylesheet';
            newStyle.href = style.href;

            const stylePromise = new Promise((resolve, reject) => {
                newStyle.onload = () => resolve(newStyle);
                newStyle.onerror = reject;
            });

            document.head.appendChild(newStyle);
            this.#config.styleCache.set(style.href, newStyle);
            
            return stylePromise;
        });

        await Promise.all(stylePromises);
    }

    async #ensureMinLoadTime(startTime) {
        const elapsed = Date.now() - startTime;
        if (elapsed < this.#config.minLoadTime) {
            await new Promise(resolve => 
                setTimeout(resolve, this.#config.minLoadTime - elapsed)
            );
        }
    }

    #handleClick(e) {
        const link = e.target.closest('a');
        if (!this.#isValidNavigationLink(link) || this.#config.isNavigating) return;
        
        e.preventDefault();
        if (window.location.href === link.href) return;
        
        this.#closeMenu();
        this.#handleNavigation(link.href);
    }

    #isValidNavigationLink(link) {
        return link && 
               link.href && 
               link.href.startsWith(window.location.origin) && 
               !link.hasAttribute('data-no-router') &&
               !link.hasAttribute('download') && 
               !link.getAttribute('target');
    }

    #closeMenu() {
        const elements = {
            toggle: document.querySelector("#cs-navigation .cs-toggle"),
            nav: document.querySelector("#cs-navigation"),
            body: document.querySelector("body"),
            menu: document.querySelector('#cs-expanded')
        };

        if (elements.nav?.classList.contains("cs-active")) {
            elements.toggle?.classList.remove("cs-active");
            elements.nav?.classList.remove("cs-active");
            elements.body?.classList.remove("cs-open");
            elements.menu?.setAttribute('aria-expanded', 'false');
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.router = new Router();
});
