
document.addEventListener('DOMContentLoaded', function () {

    // Only run on the dashboard page
    if (!document.getElementById('total-sales')) {
        return;
    }

    const chartScript = document.createElement('script');
    chartScript.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js';

    chartScript.onload = function () {
        loadDashboard();
    };

    document.head.appendChild(chartScript);

    console.log('Dashboard initialized');
});

function loadDashboard() {

    // Load KPI cards
    fetch('/api/dashboard')
        .then(response => response.json())
        .then(data => {
            document.getElementById('total-sales').textContent =
                '$' + data.total_sales.toLocaleString('en-US', { maximumFractionDigits: 0 });

            document.getElementById('total-profit').textContent =
                '$' + data.total_profit.toLocaleString('en-US', { maximumFractionDigits: 0 });

            document.getElementById('avg-order').textContent =
                '$' + data.avg_order_value.toLocaleString('en-US', { maximumFractionDigits: 2 });

            document.getElementById('total-orders').textContent =
                data.total_orders.toLocaleString();
        })
        .catch(error => console.error('Dashboard API Error:', error));

    // Monthly Sales Chart
    fetch('/api/sales/monthly')
        .then(response => response.json())
        .then(data => {

            const salesData = data.monthly_sales;
            const ctx = document.getElementById('salesChart').getContext('2d');

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: Object.keys(salesData),
                    datasets: [{
                        label: 'Monthly Sales',
                        data: Object.values(salesData),
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Monthly Sales Trend'
                        }
                    }
                }
            });

        })
        .catch(error => console.error('Monthly Sales Error:', error));

    // Sales by Region Chart
    fetch('/api/sales/by-region')
        .then(response => response.json())
        .then(data => {

            const regionData = data.sales_by_region;
            const ctx = document.getElementById('regionChart').getContext('2d');

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: Object.keys(regionData),
                    datasets: [{
                        label: 'Sales by Region',
                        data: Object.values(regionData),
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.5)',
                            'rgba(54, 162, 235, 0.5)',
                            'rgba(255, 206, 86, 0.5)',
                            'rgba(75, 192, 192, 0.5)'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Sales by Region'
                        }
                    }
                }
            });

        })
        .catch(error => console.error('Region Sales Error:', error));
}