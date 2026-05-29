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
body { font-family: 'Inter', 'Segoe UI', sans-serif; background: #f9fafb; color: #111827; }
header { background: #ffffff; border-bottom: 1px solid #e5e7eb; padding: 2rem; text-align: center; }
header h1 { font-size: 1.5rem; font-weight: 600; color: #111827; letter-spacing: -0.02em; }
header p { color: #6b7280; margin-top: 0.3rem; font-size: 0.9rem; }
.container { max-width: 860px; margin: 2rem auto; padding: 0 1.5rem; }
.card { background: #ffffff; border-radius: 8px; padding: 1.5rem; margin-bottom: 1rem; border: 1px solid #e5e7eb; }
.card h2 { color: #374151; margin-bottom: 1rem; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; }
.badge { display: inline-block; background: #f0fdf4; color: #166534; padding: 0.2rem 0.65rem; border-radius: 4px; font-size: 0.75rem; font-weight: 500; border: 1px solid #bbf7d0; }
.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }
.info-item { background: #f9fafb; border-radius: 6px; padding: 0.85rem 1rem; border: 1px solid #f3f4f6; }
.info-item .label { color: #9ca3af; font-size: 0.72rem; margin-bottom: 0.2rem; text-transform: uppercase; letter-spacing: 0.05em; }
.info-item .value { color: #111827; font-weight: 500; font-size: 0.9rem; }
.tech-list { display: flex; flex-wrap: wrap; gap: 0.4rem; }
.tech { background: #f3f4f6; color: #374151; padding: 0.25rem 0.7rem; border-radius: 4px; font-size: 0.8rem; border: 1px solid #e5e7eb; }
footer { text-align: center; padding: 2rem; color: #9ca3af; font-size: 0.8rem; border-top: 1px solid #f3f4f6; margin-top: 1rem; }
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
                    <div class="value">Metricas basicas</div>
                </div>
            </div>
        </div>
    </div>
    <footer>Universidad Mariano Galvez &bull; Sistemas Operativos II &bull; 2025</footer>
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
