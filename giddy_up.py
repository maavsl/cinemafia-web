import subprocess
from datetime import datetime

def run(cmd, obligatorio=True):
    print("▶️", " ".join(cmd))
    r = subprocess.run(cmd)
    if obligatorio and r.returncode != 0:
        raise SystemExit(f"❌ Falló: {' '.join(cmd)}")

print("🎬 GIDDY UP CINEMAFIA...")

run(["python3", "generador.py"])
run(["git", "add", "-A"])
run(["git", "status"])

mensaje = f"GIDDY UP Cinemafia {datetime.now().strftime('%Y-%m-%d %H:%M')}"
run(["git", "commit", "-m", mensaje], obligatorio=False)
run(["git", "push"])

print("✅ Publicado en GitHub Pages")