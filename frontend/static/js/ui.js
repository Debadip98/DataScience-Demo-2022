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

/**
 * Update prediction result with LLM diagnosis
 */
function updatePredictionResult(result) {
    const container = document.getElementById('resultContainer');
    if (!container) return;

    const prediction = result.prediction;
    const confidence = result.confidence;
    const proba = result.probabilities || {};
    const diagnosis = result.diagnosis_insights || {};

    // Determine prediction class
    const predictionClass = prediction === 1 ? 'cancer-positive' : 'cancer-negative';
    const predictionLabel = prediction === 1 ? 'Cancer Risk: HIGH' : 'Cancer Risk: LOW';

    // Build diagnosis HTML
    let diagnosisHTML = `
        <div class="result-container ${predictionClass}">
            <!-- Prediction Summary -->
            <div class="result-section prediction-summary">
                <h3>Prediction Result</h3>
                <div class="prediction-badge ${predictionClass}">
                    ${predictionLabel}
                </div>
                <div class="prediction-details">
                    <div class="detail-row">
                        <span class="label">Confidence Level:</span>
                        <span class="value">${formatPercent(confidence)}</span>
                        <span class="confidence-label">(${getConfidenceLabel(confidence)})</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Class 0 Probability:</span>
                        <span class="value">${formatPercent(proba.class_0 || 0)}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Class 1 Probability:</span>
                        <span class="value">${formatPercent(proba.class_1 || 0)}</span>
                    </div>
                </div>
            </div>
    `;

    // Add diagnosis insights if available
    if (diagnosis && diagnosis.diagnosis_summary) {
        diagnosisHTML += `
            <div class="result-section diagnosis-section">
                <h3>Clinical Assessment</h3>
                <div class="diagnosis-text">
                    ${diagnosis.diagnosis_summary.replace(/\n/g, '<br>')}
                </div>
            </div>
        `;
    }

    // Add feature summary
    if (diagnosis && diagnosis.feature_summary && Array.isArray(diagnosis.feature_summary)) {
        diagnosisHTML += `
            <div class="result-section feature-summary-section">
                <h3>Input Parameters Summary</h3>
                <div class="features-grid">
        `;
        
        diagnosis.feature_summary.forEach(feature => {
            diagnosisHTML += `
                <div class="feature-card">
                    <div class="feature-title">${feature.feature}</div>
                    <div class="feature-value">${feature.value.toFixed(2)}</div>
                    <div class="feature-interpretation">${feature.interpretation}</div>
                </div>
            `;
        });
        
        diagnosisHTML += `
                </div>
            </div>
        `;
    }

    // Add risk analysis
    if (diagnosis && diagnosis.risk_analysis) {
        const risk = diagnosis.risk_analysis;
        diagnosisHTML += `
            <div class="result-section risk-analysis-section">
                <h3>Risk Factor Analysis</h3>
        `;
        
        if (risk.high_risk && risk.high_risk.length > 0) {
            diagnosisHTML += `
                <div class="risk-category high-risk">
                    <h4>🔴 High Risk Factors</h4>
                    <ul>
            `;
            risk.high_risk.forEach(factor => {
                diagnosisHTML += `
                    <li>
                        <strong>${factor.factor}</strong> (Value: ${factor.value.toFixed(2)})
                        <div class="urgency-badge">${factor.urgency}</div>
                    </li>
                `;
            });
            diagnosisHTML += `
                    </ul>
                </div>
            `;
        }
        
        if (risk.moderate_risk && risk.moderate_risk.length > 0) {
            diagnosisHTML += `
                <div class="risk-category moderate-risk">
                    <h4>⚠️ Moderate Risk Factors</h4>
                    <ul>
            `;
            risk.moderate_risk.forEach(factor => {
                diagnosisHTML += `
                    <li>
                        <strong>${factor.factor}</strong> (Value: ${factor.value.toFixed(2)})
                        <div class="urgency-badge">${factor.urgency}</div>
                    </li>
                `;
            });
            diagnosisHTML += `
                    </ul>
                </div>
            `;
        }
        
        diagnosisHTML += `
            </div>
        `;
    }

    // Add recommendations
    if (diagnosis && diagnosis.recommendations && Array.isArray(diagnosis.recommendations)) {
        diagnosisHTML += `
            <div class="result-section recommendations-section">
                <h3>Clinical Recommendations</h3>
                <div class="recommendations-list">
        `;
        
        diagnosis.recommendations.forEach(rec => {
            diagnosisHTML += `<div class="recommendation-item">${rec}</div>`;
        });
        
        diagnosisHTML += `
                </div>
            </div>
        `;
    }

    // Add next steps
    if (diagnosis && diagnosis.next_steps && Array.isArray(diagnosis.next_steps)) {
        diagnosisHTML += `
            <div class="result-section next-steps-section">
                <h3>Recommended Next Steps</h3>
                <ol class="next-steps-list">
        `;
        
        diagnosis.next_steps.forEach(step => {
            diagnosisHTML += `<li>${step}</li>`;
        });
        
        diagnosisHTML += `
                </ol>
            </div>
        `;
    }

    diagnosisHTML += `</div>`;

    container.innerHTML = diagnosisHTML;
    document.getElementById('resultContent').style.display = 'block';
}

/**
 * Reset prediction display
 */
function resetPredictionDisplay() {
    const container = document.getElementById('resultContainer');
    if (container) {
        container.innerHTML = '';
        document.getElementById('resultContent').style.display = 'none';
    }
}
