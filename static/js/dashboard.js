
document.addEventListener('DOMContentLoaded', function() {
    const chartScript = document.createElement('script');
    chartScript.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js';
    document.head.appendChild(chartScript);
    chartScript.onload = function() {
        loadDashboard();
    };
});

function getUploadId() {
    const select = document.getElementById('uploadSelect');
    return select ? select.value : '';
}

function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) overlay.classList.remove('d-none');
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) overlay.classList.add('d-none');
}

function setError(elementId, message) {
    const el = document.getElementById(elementId);
    if (el) el.textContent = message;
}

function loadDashboard() {
    const uploadId = getUploadId();
    const params = uploadId ? '?upload_id=' + uploadId : '';

    showLoading();

    let completed = 0;
    const total = 4;

    function checkDone() {
        completed++;
        if (completed >= total) {
            hideLoading();
        }
    }

    // KPI cards
    fetch('/api/dashboard' + params)
        .then(function (response) { return response.json(); })
        .then(function (data) {
            if (data.error) {
                setError('total-sales', 'Error');
                setError('total-profit', 'Error');
                setError('avg-order', 'Error');
                setError('total-orders', 'Error');
            } else {
                document.getElementById('total-sales').textContent =
                    '$' + data.total_sales.toLocaleString('en-US', { maximumFractionDigits: 0 });

                document.getElementById('total-profit').textContent =
                    '$' + data.total_profit.toLocaleString('en-US', { maximumFractionDigits: 0 });

                document.getElementById('avg-order').textContent =
                    '$' + data.avg_order_value.toLocaleString('en-US', { maximumFractionDigits: 2 });

                document.getElementById('total-orders').textContent =
                    data.total_orders.toLocaleString();
            }
            checkDone();
        })
        .catch(function (error) {
            console.error('Dashboard API Error:', error);
            setError('total-sales', 'Error');
            setError('total-profit', 'Error');
            setError('avg-order', 'Error');
            setError('total-orders', 'Error');
            checkDone();
        });

    // Monthly Sales Chart
    fetch('/api/sales/monthly' + params)
        .then(function (response) { return response.json(); })
        .then(function (data) {
            var salesData = data.monthly_sales || {};
            var ctx = document.getElementById('salesChart').getContext('2d');

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: Object.keys(salesData),
                    datasets: [{
                        label: 'Monthly Sales',
                        data: Object.values(salesData),
                        borderColor: 'rgb(75, 192, 192)',
                        backgroundColor: 'rgba(75, 192, 192, 0.1)',
                        tension: 0.1,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Monthly Sales Trend'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

            checkDone();
        })
        .catch(function (error) {
            console.error('Monthly Sales Error:', error);
            checkDone();
        });

    // Sales by Region Chart
    fetch('/api/sales/by-region' + params)
        .then(function (response) { return response.json(); })
        .then(function (data) {
            var regionData = data.sales_by_region || {};
            var ctx = document.getElementById('regionChart').getContext('2d');

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: Object.keys(regionData),
                    datasets: [{
                        label: 'Sales by Region',
                        data: Object.values(regionData),
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.6)',
                            'rgba(54, 162, 235, 0.6)',
                            'rgba(255, 206, 86, 0.6)',
                            'rgba(75, 192, 192, 0.6)'
                        ],
                        borderColor: [
                            'rgb(255, 99, 132)',
                            'rgb(54, 162, 235)',
                            'rgb(255, 206, 86)',
                            'rgb(75, 192, 192)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Sales by Region'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

            checkDone();
        })
        .catch(function (error) {
            console.error('Region Sales Error:', error);
            checkDone();
        });

    // Sales by Category Chart
    fetch('/api/sales/by-category' + params)
        .then(function (response) { return response.json(); })
        .then(function (data) {
            var categoryData = data.sales_by_category || {};
            var ctx = document.getElementById('categoryChart').getContext('2d');

            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: Object.keys(categoryData),
                    datasets: [{
                        label: 'Sales by Category',
                        data: Object.values(categoryData),
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.6)',
                            'rgba(54, 162, 235, 0.6)',
                            'rgba(255, 206, 86, 0.6)',
                            'rgba(75, 192, 192, 0.6)',
                            'rgba(153, 102, 255, 0.6)'
                        ],
                        borderColor: [
                            'rgb(255, 99, 132)',
                            'rgb(54, 162, 235)',
                            'rgb(255, 206, 86)',
                            'rgb(75, 192, 192)',
                            'rgb(153, 102, 255)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Sales by Category'
                        },
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });

            checkDone();
        })
        .catch(function (error) {
            console.error('Category Sales Error:', error);
            checkDone();
        });
}
