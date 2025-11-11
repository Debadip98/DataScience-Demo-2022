/* ============================================================================
   CHART INITIALIZATION & MANAGEMENT
   ============================================================================ */

let featureImportanceChart = null;
let distributionChart = null;

/**
 * Initialize and display feature importance chart
 */
async function displayFeatureImportance() {
    try {
        showLoading('featureImportanceChart');
        
        const data = await getFeatureImportance();
        if (!data || !data.top_10) {
            console.error('No feature importance data');
            return;
        }

        const ctx = document.getElementById('featureImportanceChart');
        if (!ctx) return;

        // Prepare data
        const topFeatures = data.top_10;
        const labels = Object.keys(topFeatures);
        const values = Object.values(topFeatures);

        // Destroy existing chart
        if (featureImportanceChart) {
            featureImportanceChart.destroy();
        }

        // Create new chart
        featureImportanceChart = new Chart(ctx, {
            type: 'barh',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Importance Score',
                    data: values,
                    backgroundColor: [
                        '#6366f1',
                        '#818cf8',
                        '#a5b4fc',
                        '#c7d2fe',
                        '#e0e7ff',
                        '#f3f4f6',
                        '#ec4899',
                        '#f472b6',
                        '#fbcfe8',
                        '#fecdd3',
                    ],
                    borderColor: '#6366f1',
                    borderWidth: 1,
                    borderRadius: 4,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                indexAxis: 'y',
                plugins: {
                    legend: {
                        display: true,
                        position: 'bottom',
                    },
                    title: {
                        display: false,
                    },
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        max: Math.max(...values) * 1.1,
                    },
                },
            },
        });

    } catch (error) {
        console.error('Feature importance chart error:', error);
        showNotification('Failed to load feature importance', 'error');
    }
}

/**
 * Initialize distribution chart
 */
function initDistributionChart() {
    const ctx = document.getElementById('distributionChart');
    if (!ctx) return;

    distributionChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Class 0 (Negative)', 'Class 1 (Positive)'],
            datasets: [{
                data: [50, 50],
                backgroundColor: [
                    'rgba(99, 102, 241, 0.8)',
                    'rgba(236, 72, 153, 0.8)',
                ],
                borderColor: [
                    '#6366f1',
                    '#ec4899',
                ],
                borderWidth: 2,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        font: {
                            size: 14,
                        },
                    },
                },
            },
        },
    });
}

/**
 * Update prediction result visualization
 */
function updatePredictionResult(result) {
    const resultContainer = document.getElementById('resultContainer');
    const resultContent = document.getElementById('resultContent');

    if (!result) return;

    // Update prediction value
    document.getElementById('predictionValue').textContent = getClassLabel(result.prediction);

    // Update confidence
    const confidence = result.confidence;
    const confidencePercent = (confidence * 100).toFixed(2);
    document.getElementById('confidenceBar').style.width = `${confidence * 100}%`;
    document.getElementById('confidencePercent').textContent = `${confidencePercent}%`;

    // Update probability bars
    const prob0 = result.probabilities.class_0;
    const prob1 = result.probabilities.class_1;

    document.getElementById('prob0').style.width = `${prob0 * 100}%`;
    document.getElementById('prob0-text').textContent = `${(prob0 * 100).toFixed(2)}%`;

    document.getElementById('prob1').style.width = `${prob1 * 100}%`;
    document.getElementById('prob1-text').textContent = `${(prob1 * 100).toFixed(2)}%`;

    // Show result content
    resultContainer.style.display = 'none';
    resultContent.style.display = 'block';
}

/**
 * Reset prediction display
 */
function resetPredictionDisplay() {
    const resultContainer = document.getElementById('resultContainer');
    const resultContent = document.getElementById('resultContent');
    resultContainer.style.display = 'flex';
    resultContent.style.display = 'none';
}
