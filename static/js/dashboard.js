/**
 * Premium Modern Dashboard JS
 * Handles dynamic API fetching, shimmer visibility, theme colors, and gradient line charts.
 */

let charts = {};

document.addEventListener('DOMContentLoaded', function() {
    if (typeof Chart === 'undefined') {
        const chartScript = document.createElement('script');
        chartScript.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js';
        document.head.appendChild(chartScript);
        chartScript.onload = function() {
            initDashboard();
        };
    } else {
        initDashboard();
    }
});

function initDashboard() {
    loadDashboard();

    window.addEventListener('themeChanged', function() {
        loadDashboard();
    });
}

function resolveLoader(chartId) {
    const canvas = document.getElementById(chartId);
    const shimmer = document.getElementById(chartId + 'Shimmer');
    if (canvas) canvas.classList.remove('d-none');
    if (shimmer) shimmer.classList.add('d-none');
}

function setKpiText(elementId, value) {
    const el = document.getElementById(elementId);
    if (el) el.textContent = value;
}

function getUploadId() {
    const select = document.getElementById('uploadSelect');
    return select ? select.value : '';
}

function loadDashboard() {
    // 1. Fetch Dashboard KPIs
    fetch('/api/dashboard')
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                setKpiText('kpi-sales', 'Error');
                setKpiText('kpi-profit', 'Error');
                setKpiText('kpi-aov', 'Error');
                setKpiText('kpi-orders', 'Error');
            } else {
                const salesStr = '$' + data.total_sales.toLocaleString('en-US', { maximumFractionDigits: 0 });
                const profitStr = '$' + data.total_profit.toLocaleString('en-US', { maximumFractionDigits: 0 });
                const aovStr = '$' + data.avg_order_value.toLocaleString('en-US', { maximumFractionDigits: 2 });
                const ordersStr = data.total_orders.toLocaleString();

                setKpiText('kpi-sales', salesStr);
                setKpiText('kpi-profit', profitStr);
                setKpiText('kpi-aov', aovStr);
                setKpiText('kpi-orders', ordersStr);

                setKpiText('t-sales', salesStr);
                setKpiText('t-profit', profitStr);
                setKpiText('t-aov', aovStr);
                setKpiText('t-orders', ordersStr);
            }
        })
        .catch(err => {
            console.error('KPI error:', err);
        });

    // Theme values configuration
    const isDark = document.body.classList.contains('theme-dark');
    const textColor = isDark ? '#94a3b8' : '#475569';
    const gridColor = isDark ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.05)';

    // 2. Fetch Monthly Sales
    fetch('/api/sales/monthly')
        .then(res => res.json())
        .then(data => {
            const monthlyData = data.monthly_sales || {};
            const canvas = document.getElementById('salesChart');
            const ctx = canvas.getContext('2d');
            
            if (charts.salesChart) charts.salesChart.destroy();

            const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
            const labels = Object.keys(monthlyData).map(m => monthNames[parseInt(m) - 1] || `M${m}`);
            const values = Object.values(monthlyData);

            // Create gradient line fill
            const gradient = ctx.createLinearGradient(0, 0, 0, 280);
            gradient.addColorStop(0, 'rgba(99, 102, 241, 0.35)');
            gradient.addColorStop(1, 'rgba(99, 102, 241, 0.00)');

            charts.salesChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Sales ($)',
                        data: values,
                        borderColor: '#6366f1',
                        backgroundColor: gradient,
                        tension: 0.3,
                        fill: true,
                        borderWidth: 2,
                        pointBackgroundColor: '#6366f1',
                        pointBorderColor: '#ffffff',
                        pointHoverRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        x: { grid: { color: gridColor }, ticks: { color: textColor, font: { family: 'Inter', size: 11 } } },
                        y: { grid: { color: gridColor }, ticks: { color: textColor, font: { family: 'Inter', size: 11 } } }
                    }
                }
            });
            resolveLoader('salesChart');
        })
        .catch(err => {
            console.error('Monthly error:', err);
            resolveLoader('salesChart');
        });

    // 3. Fetch Sales by Region
    fetch('/api/sales/by-region')
        .then(res => res.json())
        .then(data => {
            const regionData = data.sales_by_region || {};
            const canvas = document.getElementById('regionChart');
            const ctx = canvas.getContext('2d');

            if (charts.regionChart) charts.regionChart.destroy();

            charts.regionChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: Object.keys(regionData),
                    datasets: [{
                        label: 'Sales ($)',
                        data: Object.values(regionData),
                        backgroundColor: [
                            'rgba(99, 102, 241, 0.8)',
                            'rgba(139, 92, 246, 0.8)',
                            'rgba(16, 185, 129, 0.8)',
                            'rgba(245, 158, 11, 0.8)'
                        ],
                        borderRadius: 6,
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        x: { grid: { display: false }, ticks: { color: textColor, font: { family: 'Inter', size: 11 } } },
                        y: { grid: { color: gridColor }, ticks: { color: textColor, font: { family: 'Inter', size: 11 } } }
                    }
                }
            });
            resolveLoader('regionChart');
        })
        .catch(err => {
            console.error('Region error:', err);
            resolveLoader('regionChart');
        });

    // 4. Fetch Sales by Category
    fetch('/api/sales/by-category')
        .then(res => res.json())
        .then(data => {
            const categoryData = data.sales_by_category || {};
            const canvas = document.getElementById('categoryChart');
            const ctx = canvas.getContext('2d');

            if (charts.categoryChart) charts.categoryChart.destroy();

            charts.categoryChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: Object.keys(categoryData),
                    datasets: [{
                        data: Object.values(categoryData),
                        backgroundColor: [
                            '#6366f1',
                            '#8b5cf6',
                            '#10b981',
                            '#f59e0b'
                        ],
                        borderWidth: isDark ? 3 : 2,
                        borderColor: isDark ? '#131b2e' : '#ffffff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { color: textColor, font: { family: 'Inter', size: 11 } }
                        }
                    }
                }
            });
            resolveLoader('categoryChart');
        })
        .catch(err => {
            console.error('Category error:', err);
            resolveLoader('categoryChart');
        });

    // 5. Fetch Top Products
    fetch('/api/top-products?n=5')
        .then(res => res.json())
        .then(data => {
            const products = data.top_products || {};
            const tbody = document.getElementById('topProductsBody');
            tbody.innerHTML = '';

            const items = Object.entries(products);
            if (items.length === 0) {
                tbody.innerHTML = '<tr><td colspan="2" class="text-center">No products found</td></tr>';
            } else {
                items.forEach(([name, sales]) => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td><span style="font-weight: 600; color: var(--text-primary);">${name}</span></td>
                        <td style="text-align:right; font-weight: 700; color: var(--accent-indigo)">$${sales.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                    `;
                    tbody.appendChild(row);
                });
            }
        })
        .catch(err => {
            console.error('Products error:', err);
        });

    // 6. Fetch RFM Segments
    fetch('/api/customers/rfm')
        .then(res => res.json())
        .then(data => {
            const segments = data.rfm_segments || {};
            const listContainer = document.getElementById('segmentList');
            listContainer.innerHTML = '';

            const items = Object.entries(segments);
            if (items.length === 0) {
                listContainer.innerHTML = '<p class="text-center text-muted">No segment data calculated.</p>';
            } else {
                const segColors = {
                    'Champions': '#6366f1',
                    'Loyal Customers': '#10b981',
                    'New Customers': '#f59e0b',
                    'At Risk': '#f43f5e',
                    'Hibernating / Lost': '#64748b',
                    'General Customers': '#8b5cf6'
                };

                items.sort((a,b) => b[1] - a[1]).forEach(([segmentName, count]) => {
                    const color = segColors[segmentName] || '#8b5cf6';
                    const el = document.createElement('div');
                    el.className = 'segment-item';
                    el.innerHTML = `
                        <div class="segment-meta">
                          <span class="segment-dot" style="background-color: ${color}"></span>
                          <span class="segment-name">${segmentName}</span>
                        </div>
                        <span class="segment-count">${count}</span>
                    `;
                    listContainer.appendChild(el);
                });
            }
        })
        .catch(err => {
            console.error('RFM error:', err);
        });
}