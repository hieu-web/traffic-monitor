// static/js/charts.js
const ctx = document.getElementById('typeChart').getContext('2d');
const typeChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['Car', 'Motorcycle', 'Bus', 'Truck'],
        datasets: [{
            data: [0, 0, 0, 0],
            backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6'],
            borderWidth: 0
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: { color: '#94a3b8' }
            }
        }
    }
});

function updateChart(stats) {
    typeChart.data.datasets[0].data = [
        stats.Car || 0, 
        stats.Motorcycle || 0, 
        stats.Bus || 0, 
        stats.Truck || 0
    ];
    typeChart.update();
}