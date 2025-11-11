/* ============================================================================
   UI UTILITY FUNCTIONS
   ============================================================================ */

/**
 * Navigate to a specific section
 */
function navigateSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });

    // Remove active from all nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });

    // Show selected section
    const section = document.getElementById(sectionName);
    if (section) {
        section.classList.add('active');
    }

    // Set active nav link
    const navLink = document.querySelector(`[data-section="${sectionName}"]`);
    if (navLink) {
        navLink.classList.add('active');
    }

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Update status badge
 */
function updateStatus(status, message = '') {
    const badge = document.getElementById('status-indicator');
    if (!badge) return;

    badge.className = `status-badge ${status}`;
    badge.textContent = message || status.toUpperCase();
}

/**
 * Show notification/toast
 */
function showNotification(message, type = 'info', duration = 3000) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Style the notification
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 2000;
        animation: slideIn 0.3s ease-in-out;
        font-weight: 500;
    `;
    
    document.body.appendChild(notification);
    
    // Remove after duration
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in-out';
        setTimeout(() => notification.remove(), 300);
    }, duration);
}

/**
 * Disable/enable form
 */
function setFormDisabled(formElement, disabled) {
    const inputs = formElement.querySelectorAll('input, button, select');
    inputs.forEach(input => {
        input.disabled = disabled;
    });
}

/**
 * Get form values
 */
function getFormValues(formElement) {
    const inputs = formElement.querySelectorAll('input');
    const values = [];
    inputs.forEach(input => {
        values.push(parseFloat(input.value) || 0);
    });
    return values;
}

/**
 * Format number to percentage
 */
function formatPercent(value) {
    return `${(value * 100).toFixed(2)}%`;
}

/**
 * Format number with decimals
 */
function formatNumber(value, decimals = 4) {
    return parseFloat(value).toFixed(decimals);
}

/**
 * Clear form
 */
function clearForm(formElement) {
    formElement.reset();
}

/**
 * Show loading state
 */
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="loading-spinner"><span>Loading...</span></div>';
    }
}

/**
 * Format confidence level
 */
function getConfidenceLabel(confidence) {
    if (confidence >= 0.9) return 'Very High';
    if (confidence >= 0.8) return 'High';
    if (confidence >= 0.7) return 'Medium';
    if (confidence >= 0.6) return 'Fair';
    return 'Low';
}

/**
 * Get class label
 */
function getClassLabel(prediction) {
    return prediction === 1 ? 'Positive (Class 1)' : 'Negative (Class 0)';
}
