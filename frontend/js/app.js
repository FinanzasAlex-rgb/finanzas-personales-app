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

// API Config
const API_URL = '/api';

// Loading state manager
function setLoading(show) {
    document.querySelector('.loading-state').style.display = show ? 'flex' : 'none';
}

// Modal Logic
function openModal(id) {
    document.getElementById(id).classList.add('active');
}

function closeModal(id) {
    document.getElementById(id).classList.remove('active');
}

function toggleFrecuencia() {
    const tipo = document.getElementById('ingresoTipo').value;
    const col = document.getElementById('colFrecuencia');
    col.style.display = tipo === 'fijo' ? 'block' : 'none';
}

// Data Fetching
async function fetchDashboardData() {
    try {
        setLoading(true);
        // Fetch balances (Ingresos - Gastos)
        const resIngresos = await fetch(`${API_URL}/ingresos`);
        const ingresos = await resIngresos.json();
        const totalIngresos = ingresos.reduce((acc, curr) => acc + curr.monto, 0);

        const resGastos = await fetch(`${API_URL}/gastos-fijos`);
        const gastos = await resGastos.json();
        const totalGastos = gastos.reduce((acc, curr) => acc + curr.monto, 0);

        // Actualizar KPIs
        document.getElementById('saldo-disponible').textContent = `$${(totalIngresos - totalGastos).toLocaleString('es-MX', { minimumFractionDigits: 2 })}`;
        document.getElementById('obligaciones-mensuales').textContent = `$${totalGastos.toLocaleString('es-MX', { minimumFractionDigits: 2 })}`;

        // Llenar Tablas
        renderIngresosTable(ingresos);
        renderGastosFijosTable(gastos);

        setLoading(false);
    } catch (e) {
        console.error('Error fetching data:', e);
        setLoading(false);
    }
}

// Renders
function renderIngresosTable(ingresos) {
    const tbody = document.getElementById('ingresos-list');
    if (!tbody) return;

    tbody.innerHTML = '';
    ingresos.forEach(i => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${i.concepto}</td>
            <td><span class="badge ${i.tipo === 'fijo' ? 'pagado' : 'pendiente'}">${i.tipo.toUpperCase()}</span></td>
            <td>$${i.monto.toLocaleString('es-MX', { minimumFractionDigits: 2 })}</td>
            <td>${i.frecuencia || i.fecha_ingreso || 'N/A'}</td>
            <td>
                <button class="btn-primary" style="padding: 6px 12px; font-size: 12px; background: var(--danger-color); color: white;" onclick="deleteIngreso('${i.id}')">
                    <i class="fa-solid fa-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function renderGastosFijosTable(gastos) {
    const tbody = document.getElementById('gastos-fijos-list');
    if (!tbody) return;

    tbody.innerHTML = '';
    gastos.forEach(g => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${g.concepto}</td>
            <td>$${g.monto.toLocaleString('es-MX', { minimumFractionDigits: 2 })}</td>
            <td>Día ${g.dia_pago}</td>
            <td><span class="badge ${g.estado_actual}">${g.estado_actual.toUpperCase()}</span></td>
            <td>
                <button class="btn-primary" style="padding: 6px 12px; font-size: 12px; background: var(--danger-color); color: white;" onclick="deleteGastoFijo('${g.id}')">
                    <i class="fa-solid fa-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// Form Submissions
async function guardarIngreso(e) {
    e.preventDefault();
    setLoading(true);

    const body = {
        concepto: document.getElementById('ingresoConcepto').value,
        monto: parseFloat(document.getElementById('ingresoMonto').value),
        tipo: document.getElementById('ingresoTipo').value,
        frecuencia: document.getElementById('ingresoTipo').value === 'fijo' ? document.getElementById('ingresoFrecuencia').value : null,
        fecha_ingreso: document.getElementById('ingresoFecha').value
    };

    try {
        const res = await fetch(`${API_URL}/ingresos/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (res.ok) {
            closeModal('ingresoModal');
            document.getElementById('formIngreso').reset();
            fetchDashboardData();
        } else {
            alert('Error guardando ingreso');
        }
    } catch (e) {
        console.error(e);
    }
    setLoading(false);
}

async function guardarGastoFijo(e) {
    e.preventDefault();
    setLoading(true);

    const body = {
        concepto: document.getElementById('gastoFijoConcepto').value,
        monto: parseFloat(document.getElementById('gastoFijoMonto').value),
        dia_pago: parseInt(document.getElementById('gastoFijoDia').value)
    };

    try {
        const res = await fetch(`${API_URL}/gastos-fijos/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (res.ok) {
            closeModal('gastoFijoModal');
            document.getElementById('formGastoFijo').reset();
            fetchDashboardData();
        } else {
            alert('Error guardando gasto fijo');
        }
    } catch (e) {
        console.error(e);
    }
    setLoading(false);
}

// Deletions
async function deleteIngreso(id) {
    if (!confirm('¿Eliminar este ingreso?')) return;
    setLoading(true);
    await fetch(`${API_URL}/ingresos/${id}`, { method: 'DELETE' });
    fetchDashboardData();
}

async function deleteGastoFijo(id) {
    if (!confirm('¿Eliminar este gasto fijo?')) return;
    setLoading(true);
    await fetch(`${API_URL}/gastos-fijos/${id}`, { method: 'DELETE' });
    fetchDashboardData();
}

// Gemini Coach
async function consultarCoach(e) {
    e.preventDefault();
    const input = document.getElementById('coach-input');
    const msg = input.value.trim();
    if (!msg) return;

    const chat = document.getElementById('coach-chat');

    // User message
    chat.innerHTML += `
        <div class="message user-message">
            <i class="fa-solid fa-user"></i>
            <p>${msg}</p>
        </div>
    `;
    input.value = '';

    // Loading AI
    const loadingId = 'loading-' + Date.now();
    chat.innerHTML += `
        <div class="message ai-message" id="${loadingId}">
            <i class="fa-solid fa-robot"></i>
            <p><i class="fa-solid fa-circle-notch fa-spin"></i> Analizando tu situación...</p>
        </div>
    `;
    chat.scrollTop = chat.scrollHeight;

    try {
        const res = await fetch(`${API_URL}/coach/ask`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pregunta: msg })
        });

        const data = await res.json();
        const loadingEl = document.getElementById(loadingId);
        if (loadingEl) loadingEl.remove();

        if (res.ok) {
            chat.innerHTML += `
                <div class="message ai-message">
                    <i class="fa-solid fa-robot"></i>
                    <p>${data.respuesta}</p>
                </div>
            `;
        } else {
            chat.innerHTML += `
                <div class="message ai-message" style="background: var(--danger-glow)">
                    <i class="fa-solid fa-triangle-exclamation"></i>
                    <p>Error: ${data.detail}</p>
                </div>
            `;
        }
    } catch (e) {
        const loadingEl = document.getElementById(loadingId);
        if (loadingEl) loadingEl.remove();
        console.error(e);
    }
    chat.scrollTop = chat.scrollHeight;
}

async function guardarApiKey(e) {
    e.preventDefault();
    const key = document.getElementById('geminiKey').value;
    if (!key) return;

    setLoading(true);
    try {
        const res = await fetch(`${API_URL}/coach/set-key?api_key=${encodeURIComponent(key)}`, {
            method: 'POST'
        });

        if (res.ok) {
            alert('¡Coach Financiero activado! Ya puedes hacerle preguntas.');
            document.getElementById('geminiKey').value = '';
        } else {
            const err = await res.json();
            alert('Error: ' + err.detail);
        }
    } catch (e) {
        console.error(e);
    }
    setLoading(false);
}

// Boot up
document.addEventListener('DOMContentLoaded', () => {
    fetchDashboardData();
});
