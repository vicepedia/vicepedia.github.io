# Generador de Vicepedia

Toda la web se genera con `python3 _build/build.py` desde la raíz del repositorio.

- `build.py`: contenido de cada página (listas de datos al principio de cada bloque) y plantilla común.
- `cheats.py`: los 61 trucos. Para confirmar un código, rellena el tercer campo con letras U/D/L/R separadas por espacios.
- `base.css`: estilos base; los añadidos están al final de `build.py`.

No edites a mano los `index.html` generados: se sobrescriben. Cambia los datos aquí y vuelve a generar.
Para una página nueva, copia uno de los bloques `PAGES.append(page(...))`, añádela a `NAV` si va en el menú y regenera (el sitemap y el buscador se actualizan solos).
