class InitialLoader {
    constructor() {
        this.loader = document.getElementById('initial-loader');
        this.brandText = document.getElementById('brand-text');
        this.starCount = 10;
        this.stars = [];
        this.heroText = document.getElementById('hero-text');
        this.brandTextContent = this.brandText.querySelector('.brand-text-content');
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
            star.style.animation = `starShine 1s ${index * 0.1}s`;
        });
    }

    createLetterMasks() {
        const words = this.brandTextContent.querySelectorAll('.brand-text-word');
        const allLetters = [];
        
        words.forEach(word => {
            const text = word.textContent;
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
                    letter.style.opacity = '1';
                    letter.style.transform = 'translateY(0)';
                    resolve();
                }, index * stagger);
            });
        }));
    }

    async startAnimation() {
        this.createStars();
        await new Promise(resolve => setTimeout(resolve, 500));

        const letters = this.createLetterMasks();
        this.brandText.classList.add('visible');
        await this.revealLetters(letters);
        
        await new Promise(resolve => setTimeout(resolve, 1000));  
        
        this.positionStars();
        this.animateStars();

        await new Promise(resolve => setTimeout(resolve, 800));

        requestAnimationFrame(() => {
            this.brandText.classList.add('moved-up');
            this.heroText.classList.add('visible');
        });

        await new Promise(resolve => setTimeout(resolve, 3500)); 

        this.loader.classList.add('hidden');

        setTimeout(() => {
            this.loader.remove();
        }, 1500); 
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const loader = new InitialLoader();
    loader.startAnimation();
});
