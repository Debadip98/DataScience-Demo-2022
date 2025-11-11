/* ============================================================================
   API CLIENT FUNCTIONS
   ============================================================================ */

const API_BASE_URL = 'http://localhost:5000/api';

/**
 * Fetch health status
 */
async function getHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (!response.ok) throw new Error('Health check failed');
        return await response.json();
    } catch (error) {
        console.error('Health check error:', error);
        return null;
    }
}

/**
 * Get model information
 */
async function getModelInfo() {
    try {
        const response = await fetch(`${API_BASE_URL}/model/info`);
        if (!response.ok) throw new Error('Failed to get model info');
        return await response.json();
    } catch (error) {
        console.error('Model info error:', error);
        return null;
    }
}

/**
 * Make a single prediction
 */
async function predict(features) {
    try {
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ features }),
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Prediction failed');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Prediction error:', error);
        throw error;
    }
}

/**
 * Make batch predictions
 */
async function predictBatch(records) {
    try {
        const response = await fetch(`${API_BASE_URL}/predict/batch`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ records }),
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Batch prediction failed');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Batch prediction error:', error);
        throw error;
    }
}

/**
 * Generate sample data
 */
async function getSampleData() {
    try {
        const response = await fetch(`${API_BASE_URL}/generate-sample`);
        if (!response.ok) throw new Error('Failed to generate sample');
        return await response.json();
    } catch (error) {
        console.error('Sample generation error:', error);
        return null;
    }
}

/**
 * Get feature importance
 */
async function getFeatureImportance() {
    try {
        const response = await fetch(`${API_BASE_URL}/feature-importance`);
        if (!response.ok) throw new Error('Failed to get feature importance');
        return await response.json();
    } catch (error) {
        console.error('Feature importance error:', error);
        return null;
    }
}

/**
 * Get model metrics
 */
async function getMetrics() {
    try {
        const response = await fetch(`${API_BASE_URL}/metrics`);
        if (!response.ok) throw new Error('Failed to get metrics');
        return await response.json();
    } catch (error) {
        console.error('Metrics error:', error);
        return null;
    }
}

/**
 * Get LLM diagnosis insights
 */
async function getDiagnosis(features) {
    try {
        const response = await fetch(`${API_BASE_URL}/diagnosis`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ features }),
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Diagnosis failed');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Diagnosis error:', error);
        throw error;
    }
}
