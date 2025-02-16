class LoaderAnimation {
    constructor(container) {
        this.container = container;
        this.dots = [];
        this.animationId = null;
        this.startTime = null;
    }

    initialize() {
        this.container.innerHTML = '';
        this.createDots();
        this.setupBackground();
    }

    createDots() {
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('span');
            dot.className = 'loader-dot';
            this.container.appendChild(dot);
            this.dots.push(dot);
        }
    }

    setupBackground() {
        const gradient = document.createElement('div');
        gradient.className = 'loader-background';
        this.container.appendChild(gradient);
    }

    startAnimation() {
        if (this.animationId) return;
        this.startTime = performance.now();
        this.animate();
    }

    stopAnimation() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }
    }

    animate(currentTime) {
        if (!this.startTime) this.startTime = currentTime;
        const elapsed = currentTime - this.startTime;

        this.dots.forEach((dot, index) => {
            const delay = index * 200;
            const time = (elapsed + delay) % 1800;
            const progress = time / 1800;

            const scale = this.calculateScale(progress);
            const opacity = this.calculateOpacity(progress);
            
            dot.style.transform = `scale(${scale})`;
            dot.style.opacity = opacity;
        });

        this.animateBackground(elapsed);
        this.animationId = requestAnimationFrame(this.animate.bind(this));
    }

    calculateScale(progress) {
        return 0.3 + Math.sin(progress * Math.PI) * 0.7;
    }

    calculateOpacity(progress) {
        return 0.2 + Math.sin(progress * Math.PI) * 0.8;
    }

    animateBackground(elapsed) {
        const backgroundScale = 1 + Math.sin(elapsed / 1000) * 0.2;
        const backgroundOpacity = 0.5 + Math.sin(elapsed / 1000) * 0.5;
        
        const background = this.container.querySelector('.loader-background');
        if (background) {
            background.style.transform = `scale(${backgroundScale})`;
            background.style.opacity = backgroundOpacity;
        }
    }

    show() {
        this.container.classList.add('active');
        this.startAnimation();
    }

    hide() {
        this.container.classList.remove('active');
        this.stopAnimation();
    }
}

window.LoaderAnimation = LoaderAnimation;
