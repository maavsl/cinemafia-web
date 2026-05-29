import subprocess
from datetime import datetime

print("🎬 CINEMAFIA GIDDY UP INICIADO...")

# 1. Generar HTML
subprocess.run(["python3", "generador.py"], check=True)

# 2. Git add
subprocess.run(["git", "add", "."], check=True)

# 3. Commit
mensaje = f"GIDDY UP Cinemafia {datetime.now().strftime('%Y-%m-%d %H:%M')}"
subprocess.run(["git", "commit", "-m", mensaje], check=False)

# 4. Push
subprocess.run(["git", "push"], check=True)

print("✅ GIDDY UP COMPLETADO: web generada y subida a GitHub")