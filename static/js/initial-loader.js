class InitialLoader {
    constructor() {
        this.loader = document.getElementById('initial-loader');
        if (!this.loader) return;  

        this.brandText = document.getElementById('brand-text');
        this.heroText = document.getElementById('hero-text');
        
        this.brandTextContent = this.brandText ? this.brandText.querySelector('.brand-text-content') : null;
        
        if (this.brandTextContent) {
            const words = ['Quantum', 'Minds'];
            words.forEach(word => {
                const wordSpan = document.createElement('span');
                wordSpan.className = 'brand-text-word';
                wordSpan.textContent = word;
                this.brandTextContent.appendChild(wordSpan);
            });
        }

        this.starCount = 15; 
        this.stars = [];
        this.animationFrames = {};
        this.lightBar = this.heroText ? this.heroText.querySelector('::before') : null;
        this.breathingAnimation = null;

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

        this.updateResponsiveValues();
    }

    updateResponsiveValues() {
        const vw = window.innerWidth;
        this.starCount = Math.max(8, Math.min(15, Math.floor(vw / 100))); 
        this.animationScale = Math.min(1, vw / 1200);
    }

    createStars() {
        for (let i = 0; i < this.starCount; i++) {
            const star = document.createElement('div');
            star.className = 'star';
            const size = Math.random() * 8 + 4; 
            
            const particle = document.createElement('canvas');
            particle.width = size * 16;  
            particle.height = size * 16;
            particle.style.width = size * 4 + 'px';  
            particle.style.height = size * 4 + 'px';
            
            this.drawParticle(particle, size);
            star.appendChild(particle);
            
            const trail = document.createElement('canvas');
            trail.className = 'star-trail';
            trail.width = size * 24;  
            trail.height = size * 24;
            trail.style.width = size * 6 + 'px';
            trail.style.height = size * 6 + 'px';
            star.appendChild(trail);
            
            this.stars.push({
                element: star,
                size,
                trail,
                x: 0,
                y: 0
            });
            this.loader.appendChild(star);
        }
    }

    positionStars() {
        if (!this.brandText) return;
        
        const textRect = this.brandText.getBoundingClientRect();
        const centerX = textRect.left + textRect.width / 2;
        const centerY = textRect.top + textRect.height / 2;

        const zones = [
            { minDist: 50, maxDist: 120, count: Math.floor(this.starCount * 0.4) },  
            { minDist: 120, maxDist: 200, count: Math.floor(this.starCount * 0.3) }, 
            { minDist: 200, maxDist: 300, count: Math.floor(this.starCount * 0.3) }  
        ];

        let starIndex = 0;
        zones.forEach(zone => {
            for (let i = 0; i < zone.count && starIndex < this.stars.length; i++) {
                const star = this.stars[starIndex];
                const angle = (Math.PI * 2 * i / zone.count) + (Math.random() * 0.5 - 0.25); 
                const distance = zone.minDist + Math.random() * (zone.maxDist - zone.minDist);
                
                star.x = Math.cos(angle) * distance + centerX;
                star.y = Math.sin(angle) * distance + centerY;
                
                star.x += (Math.random() - 0.5) * 30;
                star.y += (Math.random() - 0.5) * 30;
                
                star.element.style.left = star.x + 'px';
                star.element.style.top = star.y + 'px';
                starIndex++;
            }
        });
    }

    drawParticle(canvas, size) {
        const ctx = canvas.getContext('2d');
        const center = canvas.width / 2;
        
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        const coreGradient = ctx.createRadialGradient(center, center, 0, center, center, size);
        coreGradient.addColorStop(0, 'rgba(255, 255, 255, 1)');
        coreGradient.addColorStop(0.1, 'rgba(255, 255, 255, 1)');  
        coreGradient.addColorStop(0.3, 'rgba(240, 248, 255, 0.9)');
        coreGradient.addColorStop(0.6, 'rgba(200, 220, 255, 0.2)');
        coreGradient.addColorStop(1, 'rgba(200, 220, 255, 0)');

        ctx.globalCompositeOperation = 'source-over';
        ctx.fillStyle = coreGradient;
        ctx.beginPath();
        ctx.arc(center, center, size, 0, Math.PI * 2);
        ctx.fill();

        ctx.globalCompositeOperation = 'screen';
        const highlightGradient = ctx.createRadialGradient(center, center, 0, center, center, size * 0.3);
        highlightGradient.addColorStop(0, 'rgba(255, 255, 255, 1)');
        highlightGradient.addColorStop(0.5, 'rgba(255, 255, 255, 0.8)');
        highlightGradient.addColorStop(1, 'rgba(255, 255, 255, 0)');

        ctx.fillStyle = highlightGradient;
        ctx.beginPath();
        ctx.arc(center, center, size * 0.3, 0, Math.PI * 2);
        ctx.fill();

        ctx.globalCompositeOperation = 'screen';
        ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
        
        const rayThickness = size * 0.08;  
        ctx.fillRect(center - size * 2, center - rayThickness, size * 4, rayThickness * 2);
        ctx.fillRect(center - rayThickness, center - size * 2, rayThickness * 2, size * 4);
        
        ctx.save();
        ctx.translate(center, center);
        ctx.rotate(Math.PI / 4);
        ctx.fillRect(-size * 2, -rayThickness, size * 4, rayThickness * 2);
        ctx.rotate(Math.PI / 2);
        ctx.fillRect(-size * 2, -rayThickness, size * 4, rayThickness * 2);
        ctx.restore();

        ctx.globalCompositeOperation = 'screen';
        const outerGlow = ctx.createRadialGradient(center, center, size, center, center, size * 2);
        outerGlow.addColorStop(0, 'rgba(180, 220, 255, 0.2)');
        outerGlow.addColorStop(0.5, 'rgba(180, 220, 255, 0.05)');
        outerGlow.addColorStop(1, 'rgba(180, 220, 255, 0)');

        ctx.fillStyle = outerGlow;
        ctx.beginPath();
        ctx.arc(center, center, size * 2, 0, Math.PI * 2);
        ctx.fill();
    }

    animateStars() {
        this.stars.forEach((star, index) => {
            const startDelay = index * 150; 
            const startTime = performance.now() + startDelay;
            let lastTrailUpdate = startTime;
            const trailCtx = star.trail.getContext('2d');
            
            const animate = (currentTime) => {
                const elapsed = currentTime - startTime;
                if (elapsed < 0) {
                    this.animationFrames[`star${index}`] = requestAnimationFrame(animate);
                    return;
                }

                const duration = 4000; 
                const progress = (elapsed % duration) / duration;
                
                const curve = this.cubicBezier(0.4, 0, 0.2, 1, progress);
                const angle = progress * Math.PI * 4;
                const radius = 60 + Math.sin(progress * Math.PI * 2) * 40;
                
                const x = Math.cos(angle) * radius;
                const y = Math.sin(angle) * radius;
                
                const opacity = Math.min(1, elapsed / 500) * (1 - Math.pow(progress, 2));
                
                if (currentTime - lastTrailUpdate > 50) {
                    this.updateTrail(trailCtx, star.size, opacity);
                    lastTrailUpdate = currentTime;
                }

                const scale = 0.8 + Math.sin(progress * Math.PI * 2) * 0.2;
                star.element.style.transform = `translate(${x}px, ${y}px) scale(${scale})`;
                star.element.style.opacity = opacity;

                this.animationFrames[`star${index}`] = requestAnimationFrame(animate);
            };
            
            this.animationFrames[`star${index}`] = requestAnimationFrame(animate);
        });
    }

    updateTrail(ctx, size, opacity) {
        ctx.globalCompositeOperation = 'destination-out';
        ctx.fillStyle = `rgba(0, 0, 0, ${0.15})`; 
        ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        
        ctx.globalCompositeOperation = 'source-over';
        const gradient = ctx.createRadialGradient(
            ctx.canvas.width / 2, ctx.canvas.height / 2, 0,
            ctx.canvas.width / 2, ctx.canvas.height / 2, size * 3
        );
        
        gradient.addColorStop(0, `rgba(255, 255, 255, ${opacity * 0.4})`);
        gradient.addColorStop(0.3, `rgba(220, 240, 255, ${opacity * 0.2})`);
        gradient.addColorStop(0.6, `rgba(200, 220, 255, ${opacity * 0.1})`);
        gradient.addColorStop(1, 'rgba(200, 220, 255, 0)');
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(ctx.canvas.width / 2, ctx.canvas.height / 2, size * 3, 0, Math.PI * 2);
        ctx.fill();
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
            ...this.stars.map(star => star.element)  
        ].filter(Boolean); 

        const duration = 1000;
        const startTime = performance.now();

        return new Promise(resolve => {
            const animate = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const eased = this.cubicBezier(0.4, 0, 0.2, 1, progress);
                const opacity = 1 - eased;

                elements.forEach(element => {
                    if (element && element.style) {
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

        this.updateResponsiveValues();
        this.createStars();
        this.positionStars(); 
        
        await new Promise(resolve => setTimeout(resolve, 500));
        const letters = this.createLetterMasks();
        this.brandText.style.opacity = '1';
        
        const letterAnimation = this.revealLetters(letters);
        await new Promise(resolve => setTimeout(resolve, 800)); 
        this.animateStars();
        
        await letterAnimation;
        
        await new Promise(resolve => setTimeout(resolve, 600));
        this.animateText(this.brandText, 0, -64 * this.animationScale, 0.8, 2000);
        
        setTimeout(() => {
            this.smoothRevealHeroText(15, 0, 1800);
            this.startGlowCycles(2); 
        }, 400); 

        await new Promise(resolve => setTimeout(resolve, 6000));
        await this.fadeOutAll();
        this.loader.remove();
    }

    async startGlowCycles(cycles) {
        let currentCycle = 0;
        
        const runCycle = () => {
            if (currentCycle < cycles) {
                this.animateBreathingLight();
                currentCycle++;
                
                setTimeout(() => {
                    if (this.breathingAnimation) {
                        cancelAnimationFrame(this.breathingAnimation);
                    }
                    runCycle();
                }, 3000); 
            }
        };
        
        runCycle();
    }

    smoothRevealHeroText(startY, endY, duration) {
        if (!this.heroText) return;
        
        const startTime = performance.now();
        const initialScale = 0.98; 
        const targetScale = 1;
        const initialBlur = 2; 
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const eased = this.cubicBezier(0.2, 0.8, 0.2, 1, progress);
            const opacityEase = this.cubicBezier(0.2, 0.9, 0.3, 1, progress);
            
            const currentY = startY + (endY - startY) * eased;
            const currentScale = initialScale + (targetScale - initialScale) * eased;
            const currentBlur = initialBlur * (1 - opacityEase);
            const opacity = Math.pow(opacityEase, 1.5); 
            
            this.heroText.style.transform = `translateY(${currentY}px) scale(${currentScale})`;
            this.heroText.style.opacity = opacity;
            this.heroText.style.filter = `blur(${currentBlur}px)`;

            if (progress < 1) {
                this.animationFrames['heroText'] = requestAnimationFrame(animate);
            }
        };

        this.animationFrames['heroText'] = requestAnimationFrame(animate);
    }

    springEase(t) {
        return 1 + (--t) * t * (2.5 * t + 1.5);
    }

    animateBreathingLight() {
        const startTime = performance.now();
        const duration = 3000; 
        
        const animate = (currentTime) => {
            const elapsed = (currentTime - startTime) % duration;
            const progress = elapsed / duration;
            
            const ease = (Math.sin(progress * Math.PI * 2 - Math.PI/2) + 1) / 2;
            
            const width = 140 + (ease * 260); 
            const opacity = 0.85 + (ease * 0.15); 
            
            const shadowIntensity = 0.6 + (ease * 0.4);
            const shadows = [
                `0 0 ${25 * shadowIntensity}px rgba(255,255,255,${0.95 * shadowIntensity})`,
                `0 0 ${50 * shadowIntensity}px rgba(255,255,255,${0.85 * shadowIntensity})`,
                `0 0 ${75 * shadowIntensity}px rgba(255,255,255,${0.75 * shadowIntensity})`,
                `0 0 ${100 * shadowIntensity}px rgba(255,255,255,${0.65 * shadowIntensity})`,
                `0 0 ${125 * shadowIntensity}px rgba(255,255,255,${0.45 * shadowIntensity})`
            ].join(', ');

            const textShadows = [
                `0 0 ${2 * shadowIntensity}px rgba(255,255,255,${0.7 * shadowIntensity})`,
                `0 0 ${4 * shadowIntensity}px rgba(255,255,255,${0.5 * shadowIntensity})`,
                `0 0 ${6 * shadowIntensity}px rgba(255,255,255,${0.3 * shadowIntensity})`,
                `0 0 ${8 * shadowIntensity}px rgba(255,255,255,${0.2 * shadowIntensity})`
            ].join(', ');

            const words = this.brandTextContent.querySelectorAll('.brand-text-word');
            words.forEach(word => {
                word.style.textShadow = textShadows;
                word.style.filter = `brightness(${1 + 0.08 * ease})`;
            });

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
        if (this.stars) {
            this.stars.forEach(star => {
                if (star.element && star.element.parentNode) {
                    star.element.parentNode.removeChild(star.element);
                }
            });
        }
        
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
