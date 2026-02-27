document.addEventListener('DOMContentLoaded', () => {
    // 1. Set current date
    const dateDisplay = document.getElementById('current-date');
    if (dateDisplay) {
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        dateDisplay.textContent = new Date().toLocaleDateString('es-ES', options);
    }

    // 2. Navigation Logic
    const navLinks = document.querySelectorAll('.nav-links li');
    const views = document.querySelectorAll('.view');
    const pageTitle = document.getElementById('page-title');

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            // Remove active classes
            navLinks.forEach(n => n.classList.remove('active'));
            views.forEach(v => v.classList.remove('active'));

            // Add active class to clicked nav
            link.classList.add('active');

            // Show target view
            const targetId = link.getAttribute('data-target');
            const targetView = document.getElementById(targetId);
            if (targetView) targetView.classList.add('active');

            // Update title
            pageTitle.textContent = link.querySelector('span').textContent;
        });
    });

    // 3. Initialize Demo Charts
    initCharts();
});

function initCharts() {
    Chart.defaults.color = '#A0A4B8';
    Chart.defaults.font.family = "'Outfit', sans-serif";

    // Trend Chart (Line)
    const trendCtx = document.getElementById('trendChart');
    if (trendCtx) {
        new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
                datasets: [{
                    label: 'Ingresos',
                    data: [35000, 38000, 36000, 42000, 39000, 45000],
                    borderColor: '#00E676',
                    backgroundColor: 'rgba(0, 230, 118, 0.1)',
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true
                }, {
                    label: 'Gastos',
                    data: [28000, 31000, 27000, 29000, 32000, 30000],
                    borderColor: '#FF5252',
                    backgroundColor: 'transparent',
                    borderWidth: 3,
                    tension: 0.4,
                    borderDash: [5, 5]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'top' },
                    tooltip: {
                        backgroundColor: 'rgba(30,32,47,0.9)',
                        titleColor: '#fff',
                        bodyColor: '#A0A4B8',
                        borderColor: 'rgba(255,255,255,0.1)',
                        borderWidth: 1,
                        padding: 12
                    }
                },
                scales: {
                    y: {
                        grid: { color: 'rgba(255,255,255,0.05)' },
                        border: { display: false }
                    },
                    x: {
                        grid: { display: false },
                        border: { display: false }
                    }
                }
            }
        });
    }

    // Distribution Chart (Doughnut)
    const distCtx = document.getElementById('distributionChart');
    if (distCtx) {
        new Chart(distCtx, {
            type: 'doughnut',
            data: {
                labels: ['Comida', 'Servicios', 'Transporte', 'Deudas'],
                datasets: [{
                    data: [40, 20, 15, 25],
                    backgroundColor: [
                        '#00E676',
                        '#2196F3',
                        '#FFD740',
                        '#FF5252'
                    ],
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '75%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { padding: 20, usePointStyle: true }
                    }
                }
            }
        });
    }
}
