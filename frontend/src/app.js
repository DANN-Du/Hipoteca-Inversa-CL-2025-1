// =====================================================================
// LOGICA DE LA APLICACIÓN CLIENTE (FRONTEND) - HIPOTECA INVERSA CL
// =====================================================================

// Determinación dinámica de la URL base del Backend
// En Docker se utiliza el proxy inverso Nginx (/api), en desarrollo local se usa localhost:5000
const API_BASE = window.location.port === "5000" || window.location.hostname === "localhost" && window.location.port !== "80" && window.location.port !== ""
  ? (window.location.port === "5000" ? "" : "http://localhost:5000")
  : "";

const formatCOP = (num) => {
  return new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    maximumFractionDigits: 0
  }).format(num);
};

// =====================================================================
// NAVEGACIÓN POR PESTAÑAS
// =====================================================================
document.addEventListener("DOMContentLoaded", () => {
  const tabs = document.querySelectorAll(".nav-tab[data-tab]");
  const contents = document.querySelectorAll(".tab-content");

  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      contents.forEach(c => c.classList.remove("active"));

      tab.classList.add("active");
      const targetId = tab.getAttribute("data-tab");
      const targetContent = document.getElementById(targetId);
      if (targetContent) {
        targetContent.classList.add("active");
      }

      // Si cambia a solicitantes o viviendas, refrescar tablas
      if (targetId === "tab-solicitantes") cargarSolicitantes();
      if (targetId === "tab-viviendas") cargarViviendas();
    });
  });

  // Inicializar estado de salud
  verificarSaludServicios();

  // Escuchar botón de verificación manual
  const btnHealth = document.getElementById("btnCheckHealth");
  if (btnHealth) btnHealth.addEventListener("click", verificarSaludServicios);

  // Inicializar formularios y listeners
  initCalculo();
  initSolicitantes();
  initViviendas();
  initFlujoPrueba();
});

// =====================================================================
// CHEQUEO DE SALUD Y "HOLA MUNDO" DE SERVICIOS
// =====================================================================
async function verificarSaludServicios() {
  const badgeBack = document.getElementById("badgeBackend");
  const badgeDb = document.getElementById("badgeDatabase");

  if (badgeBack) {
    badgeBack.textContent = "Verificando...";
    badgeBack.className = "badge badge-checking";
  }
  if (badgeDb) {
    badgeDb.textContent = "Verificando...";
    badgeDb.className = "badge badge-checking";
  }

  try {
    const res = await fetch(`${API_BASE}/api/v1/health`);
    const data = await res.json();

    if (badgeBack) {
      badgeBack.textContent = "Online · Puerto 5000";
      badgeBack.className = "badge badge-success";
    }

    if (badgeDb) {
      if (data.base_de_datos === "conectado") {
        badgeDb.textContent = "Conectado · PostgreSQL 16";
        badgeDb.className = "badge badge-success";
      } else {
        badgeDb.textContent = "Desconectado";
        badgeDb.className = "badge badge-danger";
      }
    }
  } catch (err) {
    if (badgeBack) {
      badgeBack.textContent = "Offline / Sin conexión";
      badgeBack.className = "badge badge-danger";
    }
    if (badgeDb) {
      badgeDb.textContent = "Desconocido";
      badgeDb.className = "badge badge-danger";
    }
  }
}

// =====================================================================
// SIMULADOR DE HIPOTECA INVERSA
// =====================================================================
function initCalculo() {
  const form = document.getElementById("formCalculo");
  const errorBox = document.getElementById("calculoError");
  const resultsBox = document.getElementById("calculoResultados");
  const btnEjemplo = document.getElementById("btnEjemploCalc");

  if (btnEjemplo) {
    btnEjemplo.addEventListener("click", () => {
      document.getElementById("calcEdad").value = 72;
      document.getElementById("calcValor").value = 300000000;
    });
  }

  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      errorBox.classList.add("hidden");
      resultsBox.classList.add("hidden");

      const edad = parseInt(document.getElementById("calcEdad").value);
      const valor_vivienda = parseFloat(document.getElementById("calcValor").value);

      try {
        const res = await fetch(`${API_BASE}/api/v1/calculo`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ edad, valor_vivienda })
        });

        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.error || "Error al calcular hipoteca");
        }

        document.getElementById("resPagoMensual").textContent = formatCOP(data.pago_mensual);
        document.getElementById("resPorcentaje").textContent = `${data.porcentaje_financiado}%`;
        document.getElementById("resPlazo").textContent = `${data.plazo_anios} años (${data.plazo_meses} meses)`;
        document.getElementById("resValorFinanciado").textContent = formatCOP(data.valor_financiado);
        document.getElementById("resIntereses").textContent = formatCOP(data.intereses_totales);
        document.getElementById("resSaldoFinal").textContent = formatCOP(data.saldo_final_proyectado);

        resultsBox.classList.remove("hidden");
      } catch (err) {
        errorBox.textContent = `❌ ${err.message}`;
        errorBox.classList.remove("hidden");
      }
    });
  }
}

// =====================================================================
// GESTIÓN DE SOLICITANTES
// =====================================================================
function initSolicitantes() {
  const form = document.getElementById("formCrearSolicitante");
  const fechaInput = document.getElementById("solFechaNac");
  const edadInput = document.getElementById("solEdad");
  const msgBox = document.getElementById("solMsg");
  const btnBuscar = document.getElementById("btnBuscarCedula");
  const inputCedula = document.getElementById("inputBuscarCedula");
  const foundBox = document.getElementById("solicitanteEncontrado");
  const btnRefrescar = document.getElementById("btnRefrescarSolicitantes");

  // Calcular edad automáticamente
  if (fechaInput && edadInput) {
    fechaInput.addEventListener("change", () => {
      const fn = new Date(fechaInput.value);
      const hoy = new Date();
      let edad = hoy.getFullYear() - fn.getFullYear();
      const m = hoy.getMonth() - fn.getMonth();
      if (m < 0 || (m === 0 && hoy.getDate() < fn.getDate())) {
        edad--;
      }
      if (edad > 0) edadInput.value = edad;
    });
  }

  // Guardar solicitante
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      msgBox.className = "alert hidden";

      const payload = {
        nombre: document.getElementById("solNombre").value,
        identificacion: document.getElementById("solIdentificacion").value,
        fecha_nacimiento: document.getElementById("solFechaNac").value,
        edad: parseInt(document.getElementById("solEdad").value)
      };

      try {
        const res = await fetch(`${API_BASE}/api/v1/solicitantes`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "Error al registrar");

        msgBox.textContent = `✅ ${data.mensaje}`;
        msgBox.className = "alert alert-success";
        form.reset();
        cargarSolicitantes();
      } catch (err) {
        msgBox.textContent = `❌ ${err.message}`;
        msgBox.className = "alert alert-error";
      }
    });
  }

  // Buscar por cédula
  if (btnBuscar && inputCedula) {
    btnBuscar.addEventListener("click", async () => {
      foundBox.classList.add("hidden");
      const cedula = inputCedula.value.trim();
      if (!cedula) return;

      try {
        const res = await fetch(`${API_BASE}/api/v1/solicitantes/${encodeURIComponent(cedula)}`);
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "No encontrado");

        document.getElementById("fNombre").textContent = data.nombre;
        document.getElementById("fCedula").textContent = data.identificacion;
        document.getElementById("fNacimiento").textContent = data.fecha_nacimiento;
        document.getElementById("fEdad").textContent = data.edad;
        foundBox.classList.remove("hidden");
      } catch (err) {
        alert(err.message);
      }
    });
  }

  if (btnRefrescar) btnRefrescar.addEventListener("click", cargarSolicitantes);
}

async function cargarSolicitantes() {
  const tbody = document.getElementById("tbodySolicitantes");
  if (!tbody) return;

  try {
    const res = await fetch(`${API_BASE}/api/v1/solicitantes`);
    const data = await res.json();

    if (!Array.isArray(data) || data.length === 0) {
      tbody.innerHTML = `<tr><td colspan="4" class="text-center">No hay solicitantes registrados</td></tr>`;
      return;
    }

    tbody.innerHTML = data.map(s => `
      <tr>
        <td><strong>${s.identificacion}</strong></td>
        <td>${s.nombre}</td>
        <td>${s.edad} años</td>
        <td>${s.fecha_nacimiento}</td>
      </tr>
    `).join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="4" class="text-center text-danger">Error al cargar solicitantes</td></tr>`;
  }
}

// =====================================================================
// GESTIÓN DE VIVIENDAS
// =====================================================================
function initViviendas() {
  const form = document.getElementById("formCrearVivienda");
  const msgBox = document.getElementById("vivMsg");
  const btnBuscar = document.getElementById("btnBuscarDireccion");
  const inputDir = document.getElementById("inputBuscarDireccion");
  const foundBox = document.getElementById("viviendaEncontrada");
  const btnRefrescar = document.getElementById("btnRefrescarViviendas");

  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      msgBox.className = "alert hidden";

      const payload = {
        ciudad: document.getElementById("vivCiudad").value,
        barrio: document.getElementById("vivBarrio").value,
        direccion: document.getElementById("vivDireccion").value,
        identificacion_propietario: document.getElementById("vivPropietario").value,
        valor: parseFloat(document.getElementById("vivValor").value)
      };

      try {
        const res = await fetch(`${API_BASE}/api/v1/viviendas`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "Error al registrar vivienda");

        msgBox.textContent = `✅ ${data.mensaje}`;
        msgBox.className = "alert alert-success";
        form.reset();
        cargarViviendas();
      } catch (err) {
        msgBox.textContent = `❌ ${err.message}`;
        msgBox.className = "alert alert-error";
      }
    });
  }

  if (btnBuscar && inputDir) {
    btnBuscar.addEventListener("click", async () => {
      foundBox.classList.add("hidden");
      const dir = inputDir.value.trim();
      if (!dir) return;

      try {
        const res = await fetch(`${API_BASE}/api/v1/viviendas/${encodeURIComponent(dir)}`);
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "No encontrada");

        document.getElementById("fvDireccion").textContent = data.direccion;
        document.getElementById("fvUbicacion").textContent = `${data.ciudad} (${data.barrio})`;
        document.getElementById("fvPropietario").textContent = data.identificacion_propietario;
        document.getElementById("fvValor").textContent = formatCOP(data.valor);
        foundBox.classList.remove("hidden");
      } catch (err) {
        alert(err.message);
      }
    });
  }

  if (btnRefrescar) btnRefrescar.addEventListener("click", cargarViviendas);
}

async function cargarViviendas() {
  const tbody = document.getElementById("tbodyViviendas");
  if (!tbody) return;

  try {
    const res = await fetch(`${API_BASE}/api/v1/viviendas`);
    const data = await res.json();

    if (!Array.isArray(data) || data.length === 0) {
      tbody.innerHTML = `<tr><td colspan="5" class="text-center">No hay viviendas registradas</td></tr>`;
      return;
    }

    tbody.innerHTML = data.map(v => `
      <tr>
        <td><strong>${v.direccion}</strong></td>
        <td>${v.ciudad}</td>
        <td>${v.barrio}</td>
        <td>${v.identificacion_propietario}</td>
        <td>${formatCOP(v.valor)}</td>
      </tr>
    `).join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="5" class="text-center text-danger">Error al cargar viviendas</td></tr>`;
  }
}

// =====================================================================
// FLUJO COMPLETO DE PRUEBA (E2E)
// =====================================================================
function initFlujoPrueba() {
  const btn = document.getElementById("btnEjecutarFlujo");
  const box = document.getElementById("flujoResultadoBox");
  const output = document.getElementById("terminalOutput");
  const badge = document.getElementById("terminalBadge");

  const s1 = document.getElementById("flowStep1");
  const s2 = document.getElementById("flowStep2");
  const s3 = document.getElementById("flowStep3");
  const s4 = document.getElementById("flowStep4");

  if (!btn) return;

  btn.addEventListener("click", async () => {
    btn.disabled = true;
    box.classList.remove("hidden");
    output.textContent = "[INFO] Iniciando prueba de comunicación de componentes...\n";

    [s1, s2, s3, s4].forEach(s => {
      s.className = "step-card active";
      s.querySelector(".step-status").textContent = "⏳ Ejecutando...";
    });

    try {
      output.textContent += "[HTTP] Enviando POST /api/v1/flujo-prueba ...\n";
      const res = await fetch(`${API_BASE}/api/v1/flujo-prueba`, { method: "POST" });
      const data = await res.json();

      if (!res.ok) throw new Error(data.mensaje || "Error en el flujo");

      // Actualizar estados
      [s1, s2, s3, s4].forEach(s => {
        s.className = "step-card done";
        s.querySelector(".step-status").textContent = "✅ Verificado";
      });

      badge.textContent = "100% Exitoso";
      badge.className = "badge badge-success";

      output.textContent += `[STATUS] Código de Respuesta HTTP: ${res.status} OK\n`;
      output.textContent += `[RESULT] ${data.mensaje}\n`;
      output.textContent += `\nDetalles del Flujo:\n` + JSON.stringify(data.pasos, null, 2);
    } catch (err) {
      badge.textContent = "Error";
      badge.className = "badge badge-danger";
      output.textContent += `[ERROR] ${err.message}\n`;
    } finally {
      btn.disabled = false;
    }
  });
}
