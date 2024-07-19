
/**
 * charts.js
 * Purpose: Provide functions for generating various types of charts and graphs.
 * Description: This file contains functions to create, update, and animate charts
 * using the Chart.js library. It includes data processing utilities and supports
 * line, bar, pie, and other chart types.
 */

// Ensure Chart.js is loaded
if (typeof Chart === 'undefined') {
    console.error('Chart.js is not loaded. Please include the Chart.js library before this file.');
}

// Utility function to generate random colors
function generateRandomColors(count) {
    const colors = [];
    for (let i = 0; i < count; i++) {
        colors.push(`rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 0.7)`);
    }
    return colors;
}

// Function to create a line chart
function createLineChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    return new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            ...options
        }
    });
}

// Function to create a bar chart
function createBarChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    return new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            ...options
        }
    });
}

// Function to create a pie chart
function createPieChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    return new Chart(ctx, {
        type: 'pie',
        data: data,
        options: {
            responsive: true,
            ...options
        }
    });
}

// Function to process data for charts
function processChartData(rawData, chartType) {
    // This is a placeholder function. In a real-world scenario,
    // you would process the raw data based on the chart type.
    return rawData;
}

// Function to update chart data
function updateChartData(chart, newData) {
    chart.data = newData;
    chart.update();
}

// Function to animate chart
function animateChart(chart, duration = 1000) {
    chart.options.animation = {
        duration: duration,
        easing: 'easeOutQuart'
    };
    chart.update();
}

// Example usage: Create a project progress chart
function createProjectProgressChart(canvasId, projectData) {
    const data = {
        labels: projectData.map(item => item.date),
        datasets: [{
            label: 'Tasks Completed',
            data: projectData.map(item => item.tasksCompleted),
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    };

    return createLineChart(canvasId, data, {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Number of Tasks'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Date'
                }
            }
        }
    });
}

// Example usage: Create a code quality heatmap
function createCodeQualityHeatmap(canvasId, qualityData) {
    const data = {
        labels: qualityData.map(item => item.file),
        datasets: [{
            label: 'Code Quality Score',
            data: qualityData.map(item => item.score),
            backgroundColor: qualityData.map(item => `rgba(${255 - item.score * 2.55}, ${item.score * 2.55}, 0, 0.7)`),
        }]
    };

    return createBarChart(canvasId, data, {
        indexAxis: 'y',
        scales: {
            x: {
                beginAtZero: true,
                max: 100,
                title: {
                    display: true,
                    text: 'Quality Score'
                }
            }
        }
    });
}

// Example usage: Create a task distribution pie chart
function createTaskDistributionChart(canvasId, taskData) {
    const data = {
        labels: taskData.map(item => item.status),
        datasets: [{
            data: taskData.map(item => item.count),
            backgroundColor: generateRandomColors(taskData.length),
        }]
    };

    return createPieChart(canvasId, data);
}

// Debug logging
if (DEBUG) {
    console.log('Charts module loaded successfully');
}

// Export functions for use in other modules
export {
    createLineChart,
    createBarChart,
    createPieChart,
    processChartData,
    updateChartData,
    animateChart,
    createProjectProgressChart,
    createCodeQualityHeatmap,
    createTaskDistributionChart
};
