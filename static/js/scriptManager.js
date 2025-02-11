class ScriptManager {
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
        var CSbody = document.querySelector("body");
        const CSnavbarMenu = document.querySelector("#cs-navigation");
        const CShamburgerMenu = document.querySelector("#cs-navigation .cs-toggle");
        
        if (CShamburgerMenu) {
            CShamburgerMenu.addEventListener('click', function() {
                CShamburgerMenu.classList.toggle("cs-active");
                CSnavbarMenu.classList.toggle("cs-active");
                CSbody.classList.toggle("cs-open");
                ScriptManager.ariaExpanded();
            });
        }

        const dropDowns = Array.from(document.querySelectorAll('#cs-navigation .cs-dropdown'));
        for (const item of dropDowns) {
            item.addEventListener('click', () => {
                item.classList.toggle('cs-active')
            });
        }
    }

    static ariaExpanded() {
        const csUL = document.querySelector('#cs-expanded');
        if (csUL) {
            const csExpanded = csUL.getAttribute('aria-expanded');
            csUL.setAttribute('aria-expanded', csExpanded === 'false' ? 'true' : 'false');
        }
    }

    static initAll() {
        this.initFaqs();
        this.initSkipSection();
        this.initHeader();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    ScriptManager.initAll();
});

window.ScriptManager = ScriptManager;
