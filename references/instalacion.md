# Instalación única por equipo — cuando falta una herramienta

Los scripts de esta skill avisan con el comando exacto cuando falta algo. Aquí está la instalación **una sola vez por máquina**, ordenada por preferencia, para que **cualquier agente o sesión posterior** tenga el ejecutable en el PATH sin repetir nada.

Índice: [1 Principios](#1-principios) · [2 Matriz](#2-matriz-de-herramientas) · [3 Carpeta compartida](#3-carpeta-compartida-portable) · [4 Verificación](#4-verificación-final)

## 1 Principios

1. **Una vez, en el PATH**: instala con el gestor del sistema (winget/apt/brew/npm -g); todas las sesiones futuras lo encuentran.
2. **Orden de preferencia**: gestor del sistema → npm global (CLIs JS) → binario portable en carpeta del PATH (si el gestor no existe o la versión oficial no sirve).
3. **Nada por proyecto**: no instales FFmpeg/Graphviz dentro de un repo; son del equipo.
4. **Pip va al entorno Python del equipo** (`pip install --user ...`) una sola vez; los scripts de la skill lo detectan.

## 2 Matriz de herramientas

| Herramienta | Para qué (esta skill) | Windows | Linux / macOS | Verificar |
|---|---|---|---|---|
| **FFmpeg** (+ffprobe) | video y audio: convertir, filtros, denoise, normalizar | `winget install Gyan.FFmpeg` | `sudo apt install ffmpeg` / `brew install ffmpeg` | `ffmpeg -version` |
| **Graphviz** | `diagrams` (arquitectura cloud), DOT, layout de PlantUML | `winget install Graphviz.Graphviz` | `sudo apt install graphviz` / `brew install graphviz` | `dot -V` |
| **Node.js 22+** | mermaid-cli, svgo, motor de video HTML | `winget install OpenJS.NodeJS.LTS` | `sudo apt install nodejs` / `brew install node` | `node -v` |
| **mermaid-cli** | render Mermaid (`mmdc`) | `npm install -g @mermaid-js/mermaid-cli` | igual | `mmdc -v` |
| **svgo** | optimizar SVG | `npm install -g svgo` (o `npx svgo`) | igual | `svgo --version` |
| **Inkscape** | SVG→PNG de alta calidad, DXF→PNG | `winget install Inkscape.Inkscape` | `sudo apt install inkscape` / `brew install --cask inkscape` | `inkscape --version` |
| **PlantUML** (+Java) | UML clásico `.puml` | `winget install Microsoft.OpenJDK.21` + `winget install PlantUML.PlantUML` | `sudo apt install default-jre plantuml` | `plantuml -version` |
| **Python: Pillow, matplotlib** | edición de imagen y gráficos (núcleo) | `pip install --user pillow matplotlib` | `pip install --user pillow matplotlib` | `python -c "import PIL, matplotlib"` |
| **Python: schemdraw, ezdxf, diagrams, svglib, cairosvg, opencv-python** | circuitos, DXF, arquitectura, SVG→PDF/PNG, denoise avanzado | `pip install --user schemdraw ezdxf diagrams svglib reportlab cairosvg opencv-python` | igual | `python -c "import schemdraw"` |

Notas:

- **FFmpeg** es la pieza central de video/audio; si solo instalas una, instala esa. El build completo de Gyan incluye ffprobe y los filtros (`hqdn3d`, `loudnorm`).
- **WinGet viene en Windows 10/11**; si no está: `irm https://aka.ms/getwinget | iex`. Alternativas: `scoop install ffmpeg graphviz` o `choco install ffmpeg graphviz` (si ya usas esos gestores).
- Los CLIs de npm con `-g` quedan en el PATH de Node (cualquier sesión los ve). No uses `npx` para trabajo diario si puedes instalar global: npx re-descarga.
- **cv2 es opcional**: solo para `desruido` avanzado de imagen; sin él, el script usa la mediana de Pillow.
- **`cairosvg` en Windows** puede fallar al importar si falta la DLL nativa de Cairo (mensaje `no library called "cairo-2"`): en ese caso la cadena de `svg_a_raster.py` sigue sola con `svglib` o Inkscape — instala uno de esos dos (`pip install svglib reportlab`) en vez de pelear con Cairo.

## 3 Carpeta compartida (portable)

Cuando NO haya gestor (USB, equipo bloqueado) o quieras un binario concreto: una carpeta fija dentro del PATH del **usuario**, accesible para cualquier proceso/sesión de esa cuenta (todos los agentes corren en ella):

**Windows** (PowerShell):

```powershell
mkdir "$env:LOCALAPPDATA\tools\bin" -Force
# 1) descarga el ZIP oficial (p. ej. ffmpeg-release-essentials) y descomprime ahí sus .exe
# 2) añade la carpeta al PATH del usuario (persistente, sin límite de setx):
$p = [Environment]::GetEnvironmentVariable("Path","User")
[Environment]::SetEnvironmentVariable("Path", "$p;$env:LOCALAPPDATA\tools\bin", "User")
```

**Linux / macOS:**

```bash
mkdir -p ~/.local/bin
# descomprime el binario descargado en ~/.local/bin y dale permisos:
chmod +x ~/.local/bin/<ejecutable>
# ~/.local/bin ya viene en PATH en la mayoria de distros; si no:
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.profile && . ~/.profile
```

Reglas: nombres de ejecutable tal cual el sistema los busca (`ffmpeg.exe`, `dot.exe`); **una** carpeta, no repartir; anotar la versión descargada junto al binario para actualizar después.

## 4 Verificación final

```bash
ffmpeg -version        # video/audio
dot -V                 # graphviz
node -v && mmdc -v     # mermaid
python -c "import PIL, matplotlib, cv2"
```

Si algo sigue sin verse tras instalar: **cierra y reabre la terminal/sesión** (el PATH se hereda al inicio de la sesión, no se actualiza en procesos ya abiertos). Comprueba después con el comando de verificación.
