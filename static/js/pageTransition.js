class PageTransition {
    static async fadeOut(element, duration = 300) {
        if (!element) return;
        
        element.style.transition = `opacity ${duration}ms ease-out`;
        element.style.opacity = '0';
        
        await new Promise(resolve => setTimeout(resolve, duration));
    }

    static async fadeIn(element, duration = 300) {
        if (!element) return;
        
        element.style.transition = `opacity ${duration}ms ease-in`;
        element.style.opacity = '1';
        
        await new Promise(resolve => setTimeout(resolve, duration));
    }

    static async crossFade(oldContent, newContent, duration = 300) {
        if (!oldContent || !newContent) return;
        
        await this.fadeOut(oldContent, duration);
        
        oldContent.innerHTML = newContent.innerHTML;
        
        await this.fadeIn(oldContent, duration);
    }
}

window.PageTransition = PageTransition;
