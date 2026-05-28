from flask import Flask, jsonify, render_template_string
import os
import datetime
import platform

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevOps Project - SO2</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #e2e8f0; }
        header { background: linear-gradient(135deg, #1e40af, #7c3aed); padding: 2rem; text-align: center; }
        header h1 { font-size: 2rem; font-weight: 700; }
        header p { color: #bfdbfe; margin-top: 0.5rem; }
        .container { max-width: 900px; margin: 2rem auto; padding: 0 1rem; }
        .card { background: #1e293b; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; border: 1px solid #334155; }
        .card h2 { color: #60a5fa; margin-bottom: 1rem; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 0.05em; }
        .badge { display: inline-block; background: #166534; color: #86efac; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 600; }
        .badge.blue { background: #1e3a5f; color: #93c5fd; }
        .info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
        .info-item { background: #0f172a; border-radius: 8px; padding: 1rem; }
        .info-item .label { color: #94a3b8; font-size: 0.8rem; margin-bottom: 0.25rem; }
        .info-item .value { color: #f1f5f9; font-weight: 600; }
        .tech-list { display: flex; flex-wrap: wrap; gap: 0.5rem; }
        .tech { background: #1e3a5f; color: #93c5fd; padding: 0.3rem 0.8rem; border-radius: 6px; font-size: 0.85rem; }
        footer { text-align: center; padding: 2rem; color: #64748b; font-size: 0.85rem; }
    </style>
</head>
<body>
    <header>
        <h1> Infraestructura DevOps en la Nube</h1>
        <p>Proyecto Final  Sistemas Operativos II</p>
        <br>
        <span class="badge"> Sistema Operativo</span>
    </header>
    <div class="container">
        <div class="card">
            <h2> Estado del Sistema</h2>
            <div class="info-grid">
                <div class="info-item">
                    <div class="label">Fecha y Hora</div>
                    <div class="value">{{ timestamp }}</div>
                </div>
                <div class="info-item">
                    <div class="label">Versin de App</div>
                    <div class="value">v1.0.0</div>
                </div>
                <div class="info-item">
                    <div class="label">Entorno</div>
                    <div class="value">{{ env }}</div>
                </div>
                <div class="info-item">
                    <div class="label">Hostname (Contenedor)</div>
                    <div class="value">{{ hostname }}</div>
                </div>
            </div>
        </div>
        <div class="card">
            <h2> Tecnologas Implementadas</h2>
            <div class="tech-list">
                <span class="tech"> Docker</span>
                <span class="tech"> Python Flask</span>
                <span class="tech"> GitHub Actions</span>
                <span class="tech"> Nginx</span>
                <span class="tech"> PostgreSQL</span>
                <span class="tech"> Render.com</span>
                <span class="tech"> Docker Hub</span>
                <span class="tech"> CI/CD Pipeline</span>
            </div>
        </div>
        <div class="card">
            <h2> Endpoints Disponibles</h2>
            <div class="info-grid">
                <div class="info-item">
                    <div class="label">GET /</div>
                    <div class="value">Panel principal</div>
                </div>
                <div class="info-item">
                    <div class="label">GET /health</div>
                    <div class="value">Health check</div>
                </div>
                <div class="info-item">
                    <div class="label">GET /api/info</div>
                    <div class="value">Info del sistema (JSON)</div>
                </div>
                <div class="info-item">
                    <div class="label">GET /api/metrics</div>
                    <div class="value">Mtricas bsicas</div>
                </div>
            </div>
        </div>
    </div>
    <footer>Universidad Mariano Glvez &bull; Sistemas Operativos II &bull; 2025</footer>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE,
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        env=os.getenv("APP_ENV", "production"),
        hostname=platform.node()
    )

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "timestamp": str(datetime.datetime.now())}), 200

@app.route("/api/info")
def info():
    return jsonify({
        "app": "DevOps SO2 Project",
        "version": "1.0.0",
        "environment": os.getenv("APP_ENV", "production"),
        "hostname": platform.node(),
        "python": platform.python_version(),
        "timestamp": str(datetime.datetime.now())
    })

@app.route("/api/metrics")
def metrics():
    import psutil
    return jsonify({
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": {
            "total_mb": round(psutil.virtual_memory().total / 1024 / 1024, 2),
            "used_mb": round(psutil.virtual_memory().used / 1024 / 1024, 2),
            "percent": psutil.virtual_memory().percent
        },
        "uptime": str(datetime.datetime.now())
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
