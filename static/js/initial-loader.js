class InitialLoader {
    constructor() {
        this.loader = document.getElementById('initial-loader');
        if (!this.loader) return;  

        this.brandText = document.getElementById('brand-text');
        this.heroText = document.getElementById('hero-text');
        
        this.brandTextContent = this.brandText ? this.brandText.querySelector('.brand-text-content') : null;
        
        if (this.brandTextContent) {
            // Initialize the text content
            const words = ['Quantum', 'Minds'];
            words.forEach(word => {
                const wordSpan = document.createElement('span');
                wordSpan.className = 'brand-text-word';
                wordSpan.textContent = word;
                this.brandTextContent.appendChild(wordSpan);
            });
        }

        this.starCount = 10;
        this.stars = [];
        this.animationFrames = {};
        this.lightBar = this.heroText ? this.heroText.querySelector('::before') : null;
        this.breathingAnimation = null;

        // Add will-change to optimize text rendering
        if (this.brandText) {
            this.brandText.style.willChange = 'transform';
            this.brandText.style.backfaceVisibility = 'hidden';
        }

        this.handleResize = this.handleResize.bind(this);
        window.addEventListener('resize', this.handleResize);
        this.handleResize();
    }

    handleResize() {
        if (!this.brandTextContent) return;
        
        const isMobile = window.innerWidth <= 480;
        const words = this.brandTextContent.querySelectorAll('.brand-text-word');
        
        words.forEach(word => {
            word.style.display = isMobile ? 'block' : 'inline-block';
        });

        // Adjust star positions and animations based on screen size
        this.updateResponsiveValues();
    }

    updateResponsiveValues() {
        // Scale values based on viewport
        const vw = window.innerWidth;
        this.starCount = Math.max(6, Math.min(10, Math.floor(vw / 120)));
        this.animationScale = Math.min(1, vw / 1200);
    }

    createStars() {
        for (let i = 0; i < this.starCount; i++) {
            const star = document.createElement('div');
            star.className = 'star';
            star.style.width = Math.random() * 10 + 5 + 'px';
            star.style.height = star.style.width;
            this.stars.push(star);
            this.loader.appendChild(star);
        }
    }

    positionStars() {
        const textRect = this.brandText.getBoundingClientRect();
        this.stars.forEach(star => {
            const angle = Math.random() * Math.PI * 2;
            const distance = Math.random() * 100 + 50;
            const x = Math.cos(angle) * distance + textRect.left + textRect.width / 2;
            const y = Math.sin(angle) * distance + textRect.top + textRect.height / 2;
            star.style.left = x + 'px';
            star.style.top = y + 'px';
        });
    }

    animateStars() {
        this.stars.forEach((star, index) => {
            const startTime = performance.now() + (index * 100);
            const animate = (currentTime) => {
                const elapsed = currentTime - startTime;
                if (elapsed < 0) {
                    this.animationFrames[`star${index}`] = requestAnimationFrame(animate);
                    return;
                }
                
                const duration = 1000; // 1s animation
                const progress = Math.min(elapsed / duration, 1);
                
                // Scale and opacity animation
                const scale = progress < 0.5 
                    ? 2 * progress // 0 to 1 in first half
                    : 2 * (1 - progress); // 1 to 0 in second half
                
                star.style.transform = `scale(${scale})`;
                star.style.opacity = scale;

                if (progress < 1) {
                    this.animationFrames[`star${index}`] = requestAnimationFrame(animate);
                }
            };
            this.animationFrames[`star${index}`] = requestAnimationFrame(animate);
        });
    }

    createLetterMasks() {
        if (!this.brandTextContent) return [];
        const words = this.brandTextContent.querySelectorAll('.brand-text-word');
        const allLetters = [];
        
        words.forEach(word => {
            const text = word.textContent || '';
            word.textContent = '';
            
            [...text].forEach(char => {
                const span = document.createElement('span');
                span.textContent = char;
                span.style.opacity = '0';
                span.style.transform = 'translateY(-10px)';  
                span.style.display = 'inline-block';
                span.style.transition = 'all 1.2s cubic-bezier(0.23, 1, 0.32, 1)';  
                word.appendChild(span);
                allLetters.push(span);
            });
        });
        
        return allLetters;
    }

    async revealLetters(letters) {
        const stagger = 60;
        
        return Promise.all(letters.map((letter, index) => {
            return new Promise(resolve => {
                setTimeout(() => {
                    const startTime = performance.now();
                    const animate = (currentTime) => {
                        const elapsed = currentTime - startTime;
                        const duration = 1200;
                        const progress = Math.min(elapsed / duration, 1);
                        const eased = this.cubicBezier(0.23, 1, 0.32, 1, progress);
                        
                        const translateY = -10 + (10 * eased);
                        const opacity = eased;
                        
                        letter.style.transform = `translateY(${translateY}px)`;
                        letter.style.opacity = opacity;

                        if (progress < 1) {
                            requestAnimationFrame(animate);
                        } else {
                            resolve();
                        }
                    };
                    requestAnimationFrame(animate);
                }, index * stagger);
            });
        }));
    }

    animateText(element, startY, endY, scale = 1, duration = 2000) {
        const startTime = performance.now();
        const initialOpacity = parseFloat(getComputedStyle(element).opacity);
        const targetOpacity = 1;

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function (cubic-bezier approximation)
            const eased = this.cubicBezier(0.23, 1, 0.32, 1, progress);
            
            const currentY = startY + (endY - startY) * eased;
            const currentScale = 0.98 + (scale - 0.98) * eased;
            const currentOpacity = initialOpacity + (targetOpacity - initialOpacity) * eased;

            element.style.transform = `translateY(${currentY}px) scale(${currentScale})`;
            element.style.opacity = currentOpacity;

            if (progress < 1) {
                this.animationFrames[element.id] = requestAnimationFrame(animate);
            }
        };

        this.animationFrames[element.id] = requestAnimationFrame(animate);
    }

    cubicBezier(x1, y1, x2, y2, t) {
        const cx = 3 * x1;
        const bx = 3 * (x2 - x1) - cx;
        const ax = 1 - cx - bx;
        
        const cy = 3 * y1;
        const by = 3 * (y2 - y1) - cy;
        const ay = 1 - cy - by;
        
        const t3 = t * t * t;
        const t2 = t * t;
        
        return ay * t3 + by * t2 + cy * t;
    }

    async fadeOutAll() {
        const elements = [
            this.loader,
            this.brandText,
            this.heroText,
            ...this.stars
        ];

        const duration = 1000;
        const startTime = performance.now();

        return new Promise(resolve => {
            const animate = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const eased = this.cubicBezier(0.4, 0, 0.2, 1, progress);
                const opacity = 1 - eased;

                elements.forEach(element => {
                    if (element) {
                        if (element === this.loader) {
                            element.style.backgroundColor = `rgba(7, 7, 36, ${opacity})`;
                        }
                        element.style.opacity = opacity;
                    }
                });

                const lightBar = this.heroText?.querySelector('.hero-light-bar');
                if (lightBar) {
                    lightBar.style.opacity = opacity;
                }

                if (progress < 1) {
                    requestAnimationFrame(animate);
                } else {
                    this.cleanup();
                    resolve();
                }
            };

            requestAnimationFrame(animate);
        });
    }

    async startAnimation() {
        if (!this.loader || !this.brandText || !this.brandTextContent || !this.heroText) {
            console.warn('Required elements for initial loader animation not found');
            if (this.loader) {
                this.loader.remove();
            }
            return;
        }

        // Initial setup
        this.updateResponsiveValues();
        this.createStars();
        
        // Rest of the animation sequence
        await new Promise(resolve => setTimeout(resolve, 500));
        const letters = this.createLetterMasks();
        this.brandText.style.opacity = '1';
        await this.revealLetters(letters);
        
        await new Promise(resolve => setTimeout(resolve, 800));
        this.positionStars();
        this.animateStars();

        await new Promise(resolve => setTimeout(resolve, 600));
        this.animateText(this.brandText, 0, -64 * this.animationScale, 0.8, 2000);
        
        setTimeout(() => {
            this.heroText.style.opacity = '1';
            this.animateText(this.heroText, 20, 0, 1, 800);
            this.animateBreathingLight();
        }, 100);

        await new Promise(resolve => setTimeout(resolve, 3000));
        await this.fadeOutAll();
        this.loader.remove();
    }

    animateBreathingLight() {
        const startTime = performance.now();
        const duration = 3000; // 3s per cycle
        
        const animate = (currentTime) => {
            const elapsed = (currentTime - startTime) % duration;
            const progress = elapsed / duration;
            
            // Enhanced sinusoidal easing
            const ease = (Math.sin(progress * Math.PI * 2 - Math.PI/2) + 1) / 2;
            
            // Increased width range and intensity
            const width = 140 + (ease * 260); // 140px to 400px
            const opacity = 0.85 + (ease * 0.15); // 0.85 to 1
            
            // Enhanced shadow intensity
            const shadowIntensity = 0.6 + (ease * 0.4);
            const shadows = [
                `0 0 ${25 * shadowIntensity}px rgba(255,255,255,${0.95 * shadowIntensity})`,
                `0 0 ${50 * shadowIntensity}px rgba(255,255,255,${0.85 * shadowIntensity})`,
                `0 0 ${75 * shadowIntensity}px rgba(255,255,255,${0.75 * shadowIntensity})`,
                `0 0 ${100 * shadowIntensity}px rgba(255,255,255,${0.65 * shadowIntensity})`,
                `0 0 ${125 * shadowIntensity}px rgba(255,255,255,${0.45 * shadowIntensity})`
            ].join(', ');

            // Create a light bar element if it doesn't exist
            let lightBar = this.heroText.querySelector('.hero-light-bar');
            if (!lightBar) {
                lightBar = document.createElement('div');
                lightBar.className = 'hero-light-bar';
                this.heroText.insertBefore(lightBar, this.heroText.firstChild);
            }

            lightBar.style.width = `${width}px`;
            lightBar.style.opacity = opacity;
            lightBar.style.boxShadow = shadows;
            lightBar.style.filter = `blur(${0.8 * shadowIntensity}px)`;

            this.breathingAnimation = requestAnimationFrame(animate);
        };

        this.breathingAnimation = requestAnimationFrame(animate);
    }

    cleanup() {
        Object.values(this.animationFrames).forEach(frame => {
            cancelAnimationFrame(frame);
        });
        if (this.breathingAnimation) {
            cancelAnimationFrame(this.breathingAnimation);
        }
        window.removeEventListener('resize', this.handleResize);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const loader = new InitialLoader();
    if (loader.loader) {
        loader.startAnimation();
    }
});
