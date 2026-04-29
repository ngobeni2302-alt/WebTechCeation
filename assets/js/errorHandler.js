export function handleApiError(response, errorData, formElement) {
    if (!response) {
        // Network Error (0)
        showToast("Check your internet connection.", "error");
        return;
    }

    const status = response.status;

    if (status === 422) {
        // Validation Error: Highlight specific input fields in red
        if (formElement) {
            // Remove previous error highlights
            formElement.querySelectorAll('.input-error').forEach(el => el.classList.remove('input-error'));
            
            if (errorData && errorData.errors) {
                // Add error highlights to specific fields
                for (const field in errorData.errors) {
                    const input = formElement.querySelector(`[name="${field}"], #${field}`);
                    if (input) {
                        input.classList.add('input-error');
                    }
                }
            } else {
                // Fallback: highlight all inputs if specific errors aren't provided but it's a 422
                formElement.querySelectorAll('input, select, textarea').forEach(el => el.classList.add('input-error'));
            }
        }
    } else if (status === 401 || status === 403) {
        // Authentication (401/403): Redirect to login or show "Session Expired" modal
        const authOverlay = document.getElementById('authOverlay');
        if (authOverlay) {
            authOverlay.style.display = 'flex';
            setTimeout(() => { 
                authOverlay.classList.remove('hidden'); 
                authOverlay.setAttribute('aria-hidden', 'false');
            }, 10);
            
            const loginError = document.getElementById('loginError');
            if (loginError) {
                loginError.textContent = "Session Expired. Please log in again.";
            }
        } else {
            // Fallback if modal is not present
            window.location.href = '/login'; 
        }
    } else if (status === 500) {
        // Server Error (500)
        showToast("Something went wrong", "error");
    } else {
        // Generic handling for other errors if necessary
        const msg = errorData?.message || "An error occurred";
        showToast(msg, "error");
    }
}

export function showToast(message, type = 'info') {
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.style.position = 'fixed';
        toastContainer.style.bottom = '20px';
        toastContainer.style.right = '20px';
        toastContainer.style.zIndex = '9999';
        toastContainer.style.display = 'flex';
        toastContainer.style.flexDirection = 'column';
        toastContainer.style.gap = '10px';
        document.body.appendChild(toastContainer);
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    // Base styles for toast
    toast.style.padding = '12px 20px';
    toast.style.borderRadius = '8px';
    toast.style.color = '#fff';
    toast.style.background = type === 'error' ? '#ef4444' : '#3b82f6';
    toast.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(100%)';
    toast.style.transition = 'all 0.3s ease';

    toastContainer.appendChild(toast);

    // Animate in
    requestAnimationFrame(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateY(0)';
    });

    // Remove after 3 seconds
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(100%)';
        setTimeout(() => {
            if (toast.parentElement) {
                toastContainer.removeChild(toast);
            }
        }, 300);
    }, 3000);
}
