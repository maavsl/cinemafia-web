#!/bin/bash

cd /Users/usuario/Desktop/Placer/CINEMAFIA-WEB

echo "📥 Copiando CSV..."

cp "/Users/usuario/Library/CloudStorage/GoogleDrive-eliseo.gom@gmail.com/Mi unidad/CINEMAFIA_EXPORT/cinemafia.csv" "./csv/cinemafia.csv"

echo "🎬 GIDDY UP CINEMAFIA..."

python3 giddy_up.py

echo ""
echo "✅ TERMINADO"
echo "Web actualizada y publicada."
read -p "Pulsa ENTER para cerrar..."