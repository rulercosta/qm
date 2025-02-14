class PhotoCarousel {
    #instances = [];
    #modal;
    #modalImg;
    
    init() {
        this.cleanup();
        this.#createModal();
        this.#initModal();
        
        const carousels = document.querySelectorAll('.photo-carousel');
        carousels.forEach(carousel => {
            const instance = new Swiper(carousel, {
                slidesPerView: 1,
                spaceBetween: 20,
                loop: true,
                speed: 800,
                autoplay: {
                    delay: 2500,
                    disableOnInteraction: false, 
                    pauseOnMouseEnter: true,
                    waitForTransition: true  
                },
                effect: 'fade',
                fadeEffect: {
                    crossFade: true
                },
                on: {
                    slideChangeTransitionEnd: function() {
                        this.autoplay.start();
                    }
                }
            });

            instance.autoplay.start();
            
            carousel.addEventListener('mouseleave', () => {
                instance.autoplay.start();
            });

            instance.on('slideChangeTransitionEnd', () => {
                instance.autoplay.start();
            });
            
            carousel.querySelectorAll('.cs-picture img').forEach(img => {
                img.addEventListener('click', (e) => {
                    e.stopPropagation();
                    this.#showModal(img.src);
                    instance.autoplay.stop();
                });
            });
            
            this.#instances.push(instance);
        });
    }

    #createModal() {
        const existingModal = document.getElementById('photo-modal');
        if (existingModal) {
            existingModal.remove();
        }

        this.#modal = document.createElement('div');
        this.#modal.id = 'photo-modal';
        this.#modal.className = 'photo-modal';

        const closeBtn = document.createElement('span');
        closeBtn.className = 'modal-close';
        closeBtn.innerHTML = '&times;';

        this.#modalImg = document.createElement('img');
        this.#modalImg.id = 'modal-img';
        this.#modalImg.className = 'modal-content';
        this.#modalImg.alt = '';

        this.#modal.appendChild(closeBtn);
        this.#modal.appendChild(this.#modalImg);

        document.body.appendChild(this.#modal);
    }

    #initModal() {
        if (!this.#modal || !this.#modalImg) return;
        
        this.#modal.addEventListener('click', () => {
            this.#hideModal();
            this.#instances.forEach(instance => instance.autoplay.start());
        });
        
        this.#modalImg.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }

    #showModal(imgSrc) {
        this.#modalImg.src = imgSrc;
        this.#modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
        
        void this.#modal.offsetWidth;
        
        this.#modal.classList.add('active');
        this.#modalImg.classList.add('active');
        this.#modal.querySelector('.modal-close').classList.add('active');
    }

    #hideModal() {
        this.#modal.classList.remove('active');
        this.#modalImg.classList.remove('active');
        this.#modal.querySelector('.modal-close').classList.remove('active');
        
        setTimeout(() => {
            this.#modal.style.display = 'none';
            document.body.style.overflow = '';
            this.#instances.forEach(instance => {
                instance.autoplay.start();
            });
        }, 300); 
    }

    cleanup() {
        this.#instances.forEach(instance => {
            if (instance && instance.destroy) {
                instance.destroy(true, true);
            }
        });
        this.#instances = [];
        
        if (this.#modal && this.#modal.parentNode) {
            this.#modal.parentNode.removeChild(this.#modal);
        }
        this.#modal = null;
        this.#modalImg = null;
    }
}

window.PhotoCarousel = PhotoCarousel;
