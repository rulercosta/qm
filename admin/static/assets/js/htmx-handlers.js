document.addEventListener('DOMContentLoaded', function() {
    // Handle successful form submissions
    document.body.addEventListener('htmx:afterRequest', function(evt) {
        try {
            if (evt.detail.successful) {
                const response = JSON.parse(evt.detail.xhr.response);
                
                if (response.success) {
                    toastr.success(response.message);
                    
                    // Close modal if operation was successful
                    if (evt.target.closest('.modal')) {
                        $(evt.target.closest('.modal')).modal('hide');
                    }
                    
                    // Refresh user info if username was changed
                    if (response.username) {
                        document.querySelectorAll('.profile-username').forEach(el => {
                            el.textContent = response.username;
                        });
                    }
                } else {
                    toastr.error(response.message || 'An error occurred');
                }
            }
        } catch (e) {
            console.error('Error processing response:', e);
        }
    });

    // Handle form submission errors
    document.body.addEventListener('htmx:responseError', function(evt) {
        try {
            const response = JSON.parse(evt.detail.xhr.response);
            toastr.error(response.message || 'An error occurred');
        } catch (e) {
            toastr.error('An error occurred. Please try again.');
        }
    });
});
