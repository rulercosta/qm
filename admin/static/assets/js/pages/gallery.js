class Gallery {
    constructor() {
        this.items = [];
        this.mainSpinner = document.getElementById('mainLoadingSpinner');
        this.init();
    }

    async init() {
        // Show main spinner
        this.mainSpinner.style.display = 'flex';
        
        await this.loadImages();
        this.renderGallery();
        this.setupEventListeners();
        
        // Hide main spinner with a fade effect
        this.mainSpinner.style.opacity = '0';
        setTimeout(() => {
            this.mainSpinner.style.display = 'none';
        }, 300);
    }

    async loadImages() {
        try {
            const response = await fetch('/admin/gallery/images'); // Updated URL with /admin prefix
            const data = await response.json();
            if (data.success) {
                this.items = data.images;
            }
        } catch (error) {
            console.error('Error loading images:', error);
        }
    }

    createGalleryItemHTML(item) {
        return `
        <div class="col-sm-6 col-md-4 col-lg-3">
          <div class="gallery-item loading" data-id="${item.id}">
            <img 
              src="${item.img}" 
              alt="Gallery image" 
              onload="gallery.handleImageLoad(this)"
              onerror="gallery.handleImageError(this)">
            <div class="item-overlay">
              <button class="overlay-btn preview-btn" data-img="${item.img}" title="Preview">
                <i class="fas fa-eye"></i>
              </button>
              <button class="overlay-btn copy-btn" data-img="${item.img}" title="Copy URL">
                <i class="fas fa-link"></i>
              </button>
              <button class="overlay-btn delete-btn" title="Delete Image">
                <i class="fas fa-trash"></i>
              </button>
            </div>
          </div>
        </div>
      `;
    }

    handleImageLoad(img) {
        const item = img.closest('.gallery-item');
        img.classList.add('loaded');
        item.classList.remove('loading');
    }

    handleImageError(img) {
        const item = img.closest('.gallery-item');
        item.classList.remove('loading');
        item.classList.add('error');
        item.innerHTML = '<div class="error-message">Failed to load image</div>';
    }

    renderGallery() {
        const gallery = document.getElementById('galleryGrid');
        if (this.items.length === 0) {
            gallery.innerHTML = '<div class="col-12 text-center p-5">No images found</div>';
            return;
        }
        
        gallery.innerHTML = this.items
            .map(item => this.createGalleryItemHTML(item))
            .join('');
    }

    showPreview(imgUrl) {
        const preview = document.getElementById('fullscreenPreview');

        // Setup preview with loader
        preview.innerHTML = `
        <div class="loading-spinner">
          <div class="spinner"></div>
        </div>
        <img src="" alt="Preview">
      `;

        preview.style.display = 'flex';
        preview.classList.add('active');

        const newImg = preview.querySelector('img');

        // Simulate network delay and add loading animation
        setTimeout(() => {
            // Create a new image to preload
            const tempImg = new Image();

            tempImg.onload = () => {
                setTimeout(() => {
                    newImg.src = imgUrl;
                    // Add small delay before showing image
                    setTimeout(() => {
                        preview.querySelector('.loading-spinner').style.opacity = '0';
                        newImg.classList.add('preview-loaded');
                    }, 150);
                }, 300); // Add extra delay for smoother transition
            };

            tempImg.src = imgUrl;
        }, 500); // Initial delay before loading starts

        // Trigger reflow to enable transitions
        preview.offsetHeight;

        preview.classList.add('active');

        const closePreview = () => {
            preview.classList.remove('active');
            setTimeout(() => {
                preview.style.display = 'none';
            }, 300); // Match transition duration
        };

        // Close preview on click
        preview.addEventListener('click', closePreview, { once: true });

        // Close on escape key
        const escHandler = (e) => {
            if (e.key === 'Escape') {
                closePreview();
                document.removeEventListener('keydown', escHandler);
            }
        };
        document.addEventListener('keydown', escHandler);
    }

    setupUploadArea() {
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const imagePreview = document.getElementById('imagePreview');

        const handleFileSelect = (file) => {
            if (!file || !file.type.startsWith('image/')) {
                alert('Please select an image file');
                return;
            }

            const reader = new FileReader();
            reader.onload = (e) => {
                const previewImg = imagePreview.querySelector('img');
                previewImg.src = e.target.result;
                
                // Hide upload area and show preview
                uploadArea.classList.add('hidden');
                imagePreview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        };

        // Handle file input change
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length) {
                handleFileSelect(e.target.files[0]);
            }
        });

        // Handle file drop
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            e.stopPropagation();
            uploadArea.classList.remove('highlight');
            
            const files = e.dataTransfer.files;
            if (files.length) {
                fileInput.files = files;
                handleFileSelect(files[0]);
            }
        });

        // Handle preview removal
        document.querySelector('.remove-preview').addEventListener('click', () => {
            imagePreview.style.display = 'none';
            uploadArea.classList.remove('hidden');
            fileInput.value = '';
        });

        // Reset preview when modal is hidden
        $('#uploadModal').on('hidden.bs.modal', () => {
            imagePreview.style.display = 'none';
            uploadArea.classList.remove('hidden');
            fileInput.value = '';
        });

        // Drag and drop handlers
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.add('highlight');
            });
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.remove('highlight');
            });
        });

        uploadArea.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files.length) fileInput.files = files;
        });

        // Handle upload submission
        document.getElementById('uploadSubmit').addEventListener('click', async () => {
            const fileInput = document.getElementById('fileInput');
            if (!fileInput.files.length) {
                toastr.error('Please select an image file before uploading');
                return;
            }
            const success = await this.handleUpload(fileInput.files[0]);
            if (success) {
                $('#uploadModal').modal('hide');
            }
        });
    }

    async handleUpload(file) {
        const uploadProgress = document.getElementById('uploadProgress');
        const uploadStatus = document.getElementById('uploadStatus');
        
        if (!file.type.startsWith('image/')) {
            showToast('Invalid file type. Please select an image file.', 'error');
            return false;
        }

        uploadProgress.style.display = 'block';
        uploadStatus.textContent = 'Uploading image...';

        const formData = new FormData();
        formData.append('file', file);

        try {
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            
            const response = await fetch('/admin/gallery/upload', {  // Updated URL path
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData,
                credentials: 'same-origin'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success) {
                showToast('Image was uploaded successfully!', 'success');
                uploadProgress.classList.add('bg-success');
                uploadStatus.textContent = 'Upload complete!';
                
                // Add new image to gallery
                this.items.push({
                    id: data.data.id,
                    img: data.data.url
                });
                
                this.renderGallery();
                
                // Reset upload form
                document.getElementById('fileInput').value = '';
                
                setTimeout(() => {
                    $('#uploadModal').modal('hide');
                    uploadProgress.style.display = 'none';
                    uploadProgress.classList.remove('bg-success');
                    uploadStatus.textContent = '';
                }, 1500);
                
                return true;
            } else {
                showToast(data.message || 'Upload failed', 'error');
                uploadProgress.classList.add('bg-danger');
                uploadStatus.textContent = 'Upload failed';
                return false;
            }
        } catch (error) {
            console.error('Upload error:', error);
            showToast('Upload failed: ' + error.message, 'error');
            uploadProgress.classList.add('bg-danger');
            uploadStatus.textContent = 'Upload failed';
            return false;
        }
    }

    async handleDelete(itemId) {
        try {
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            
            const response = await fetch('/admin/gallery/delete', {  // Updated URL path
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                credentials: 'same-origin',
                body: JSON.stringify({ id: itemId })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.success) {
                this.items = this.items.filter(item => item.id !== itemId);
                this.renderGallery();
                return true;
            }
            return false;
        } catch (error) {
            console.error('Delete error:', error);
            return false;
        }
    }

    setupEventListeners() {
        // Preview
        $('#galleryGrid').on('click', '.preview-btn', e => {
            const imgUrl = $(e.currentTarget).data('img');
            this.showPreview(imgUrl);
        });

        // Copy URL
        $('#galleryGrid').on('click', '.copy-btn', async e => {
            const button = e.currentTarget;
            const imgUrl = button.dataset.img;
            
            try {
                await navigator.clipboard.writeText(imgUrl);
                
                // Visual feedback
                button.classList.add('copied');
                const originalTitle = button.title;
                button.title = 'Copied!';
                
                showToast('Image URL copied to clipboard!', 'success');
                
                // Reset after animation
                setTimeout(() => {
                    button.classList.remove('copied');
                    button.title = originalTitle;
                }, 2000);
            } catch (err) {
                console.error('Failed to copy:', err);
                showToast('Failed to copy URL to clipboard', 'error');
            }
        });

        // Upload
        $('#uploadBtn').click(() => $('#uploadModal').modal('show'));
        this.setupUploadArea();

        // Delete functionality
        let deleteTimeout;
        let itemToDelete = null;

        $('#galleryGrid').on('click', '.delete-btn', e => {
            e.preventDefault();
            itemToDelete = $(e.currentTarget).closest('.gallery-item');
            $('#deleteModal').modal('show');
        });

        $('#confirmDelete').on('click', async function () {
            const progressBar = $('#deleteModal .progress');
            const footer = $('#deleteModal .modal-footer');

            progressBar.removeClass('d-none');
            footer.hide();

            const itemId = itemToDelete.data('id');

            deleteTimeout = setTimeout(async () => {
                const success = await gallery.handleDelete(itemId);
                if (success) {
                    itemToDelete.parent().fadeOut(300, function () {
                        $(this).remove();
                        showToast(`Image #${itemId} was successfully deleted.`, 'success');
                    });
                } else {
                    showToast(`Failed to delete image #${itemId}. Please try again.`, 'error');
                }

                $('#deleteModal').modal('hide');
                setTimeout(() => {
                    progressBar.addClass('d-none');
                    footer.show();
                }, 300);
            }, 1000); // Reduced timeout for better UX
        });

        $('#deleteModal').on('hidden.bs.modal', function () {
            // Clear timeout if modal is closed before deletion
            if (deleteTimeout) {
                clearTimeout(deleteTimeout);
            }
            // Reset modal state
            $(this).find('.progress').addClass('d-none');
            $(this).find('.modal-footer').show();
            itemToDelete = null;
        });

        // File validation in upload area
        const fileInput = document.getElementById('fileInput');
        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file && !file.type.startsWith('image/')) {
                showToast('Please select a valid image file', 'warning');
                fileInput.value = '';
            }
        });
    }
}

// Initialize gallery when DOM is loaded
let gallery; // Declare gallery globally
$(document).ready(() => {
    $.widget.bridge('uibutton', $.ui.button);
    $('[data-widget="pushmenu"]').PushMenu();
    $('.content-wrapper').overlayScrollbars({
        scrollbars: {
            autoHide: 'scroll'
        }
    });
    gallery = new Gallery(); // Assign to global variable
});

// Optimize modal animations
$('.modal').on('show.bs.modal', function () {
    $(this).addClass('fade');
}).on('shown.bs.modal', function () {
    $(this).removeClass('fade');
});