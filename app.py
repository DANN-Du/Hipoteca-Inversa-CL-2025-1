# Punto de entrada principal en la raíz que enlaza con backend/app.py
import os
import sys

# Agregar backend y backend/src al path
backend_path = os.path.join(os.path.dirname(__file__), "backend")
src_path = os.path.join(backend_path, "src")
sys.path.insert(0, src_path)
sys.path.insert(0, backend_path)

from backend.app import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
