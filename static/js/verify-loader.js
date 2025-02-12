class VerifyLoader {
    constructor() {
        this.loader = document.getElementById('verify-loader');
        this.progressRing = document.querySelector('.progress-ring-fill');
        this.checkmark = document.querySelector('.checkmark');
        this.statusText = document.querySelector('.status-text');
        this.crossmark = document.querySelector('.crossmark');
        this.resultContainer = document.querySelector('.result-container');
        this.resultText = document.querySelector('.result-text');
        this.resultSubtext = document.querySelector('.result-subtext');
        this.isError = this.loader.dataset.error === 'true';
        
        if (this.isError) {
            this.verificationSteps = [
                { text: 'Analyzing Certificate', duration: 900 },
                { text: 'Detecting Issues', duration: 900 },
                { text: 'Verification Failed', duration: 900 }
            ];
        } else {
            this.verificationSteps = [
                { text: 'Analyzing Certificate', duration: 900 },
                { text: 'Validating Signatures', duration: 900 },
                { text: 'Verifying Authenticity', duration: 900 }
            ];
        }
        this.circumference = 2 * Math.PI * 45; // 45 is the radius of our circle
        this.progressRing.style.strokeDasharray = this.circumference;
        this.progressRing.style.strokeDashoffset = this.circumference;
        this.congratsContainer = document.querySelector('.congrats-container');
        this.verificationContainer = document.querySelector('.verification-container');
    }

    async createParticles() {
        const particleCount = 20;
        const center = { 
            x: this.checkmark.getBoundingClientRect().left + 26,
            y: this.checkmark.getBoundingClientRect().top + 26
        };

        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            const size = Math.random() * 6 + 4;
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            
            const angle = (Math.random() * 360) * (Math.PI / 180);
            const velocity = Math.random() * 100 + 50;
            const tx = Math.cos(angle) * velocity;
            const ty = Math.sin(angle) * velocity;
            
            particle.style.left = `${center.x}px`;
            particle.style.top = `${center.y}px`;
            particle.style.setProperty('--tx', `${tx}px`);
            particle.style.setProperty('--ty', `${ty}px`);
            
            this.loader.appendChild(particle);
            particle.style.animation = `particle-fade 1s ease-out forwards`;
            
            particle.addEventListener('animationend', () => particle.remove());
        }
    }

    updateProgress(progress) {
        const offset = this.circumference - (progress * this.circumference);
        this.progressRing.style.strokeDashoffset = offset;
        
        const opacity = Math.min(1, progress * 3);
        this.statusText.style.opacity = opacity;
        this.statusText.style.transform = `translateY(${10 - (opacity * 10)}px)`;
    }

    async verifySequence() {
        let progress = 0;
        for (const step of this.verificationSteps) {
            this.statusText.textContent = step.text;
            
            const increment = 1 / this.verificationSteps.length;
            const start = progress;
            const end = progress + increment;
            
            await this.animateProgress(start, end, step.duration);
            progress = end;
        }
    }

    async animateProgress(start, end, duration) {
        const startTime = performance.now();
        
        return new Promise(resolve => {
            const animate = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                
                const easeProgress = progress < 0.5
                    ? 4 * progress * progress * progress
                    : 1 - Math.pow(-2 * progress + 2, 3) / 2;
                
                const currentProgress = start + (end - start) * easeProgress;
                this.updateProgress(currentProgress);
                
                if (progress < 1) {
                    requestAnimationFrame(animate);
                } else {
                    resolve();
                }
            };
            
            requestAnimationFrame(animate);
        });
    }

    async showSuccess() {
        if (this.isError) {
            this.statusText.textContent = 'Verification Failed';
            this.crossmark.style.display = 'block';
            this.progressRing.style.stroke = '#dc2626';
        } else {
            this.statusText.textContent = 'Certificate Verified';
            this.checkmark.style.display = 'block';
        }
    }

    async showResult() {
        if (this.isError) {
            this.verificationContainer.classList.add('fade');
            
            await new Promise(resolve => setTimeout(resolve, 800));
            
            this.resultContainer.innerHTML = '';
            const errorImage = document.createElement('img');
            errorImage.src = '/static/images/404.png';
            errorImage.alt = 'Error';
            errorImage.className = 'error-image';
            this.resultContainer.appendChild(errorImage);
            this.resultContainer.classList.add('show', 'error');
            
            await new Promise(resolve => setTimeout(resolve, 3000));
            
            this.loader.classList.add('fade-out');
            this.resultContainer.classList.add('fade-out');
            
            await new Promise(resolve => setTimeout(resolve, 800));
            
            this.loader.remove();
        } else {
            this.verificationContainer.classList.add('fade');
            await new Promise(resolve => setTimeout(resolve, 800));
            await this.showCongratulations();
        }
    }

    async showCongratulations() {
        this.checkmark.style.display = 'none';
        this.statusText.style.opacity = '0';
        
        this.resultText.innerHTML = '<span class="party-popper">🎉</span>Congratulations!<span class="party-popper">🎉</span>';
        this.resultSubtext.textContent = 'Your certificate has been successfully verified';
        this.resultContainer.classList.add('show');
        
        await new Promise(resolve => setTimeout(resolve, 200));
        await this.createEnhancedParticles();
        
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        this.resultContainer.style.transition = 'opacity 0.6s ease-out';
        this.resultContainer.style.opacity = '0';
        
        await new Promise(resolve => setTimeout(resolve, 600));
    }

    async createEnhancedParticles() {
        const particleCount = 100;
        const colors = ['#4f46e5', '#9333ea', '#FFD700', '#FF6B6B', '#4CAF50'];
        
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            
            const size = Math.random() * 10 + 5;
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            
            const angle = (Math.random() * 360) * (Math.PI / 180);
            const distance = Math.random() * 100 + 50;
            const startX = Math.cos(angle) * distance;
            const startY = Math.sin(angle) * distance;
            
            particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            particle.style.left = `calc(50% + ${startX}px)`;
            particle.style.top = `calc(50% + ${startY}px)`;
            
            const endDistance = distance * 2;
            const endX = Math.cos(angle) * endDistance;
            const endY = Math.sin(angle) * endDistance;
            
            particle.style.setProperty('--tx', `${endX}px`);
            particle.style.setProperty('--ty', `${endY}px`);
            
            this.loader.appendChild(particle);
            particle.style.animation = `particle-fade ${1 + Math.random()}s ease-out forwards`;
            
            particle.addEventListener('animationend', () => particle.remove());
        }
    }

    async startAnimation() {
        await this.verifySequence();
        await this.showSuccess();
        await new Promise(resolve => setTimeout(resolve, 800));
        await this.showResult();
        
        this.loader.classList.add('hidden');
        
        setTimeout(() => {
            this.loader.style.display = 'none';
            this.loader.remove();
        }, 900);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('verify-loader')) {
        const loader = new VerifyLoader();
        loader.startAnimation();
    }
});
