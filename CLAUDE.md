# Vicepedia: cómo está montado este repositorio

La web (https://vicepedia.github.io/) ya no es una sola página. Desde el 19 de noviembre de 2026 tiene una página por tema y se genera con un script:

- `python3 _build/build.py` (desde la raíz) regenera todas las páginas, `assets/`, `sitemap.xml` y el buscador global.
- El contenido está en `_build/build.py` (listas de datos de cada página) y los trucos en `_build/cheats.py`.
- No edites a mano ningún `index.html` ni nada de `assets/`: se sobrescribe en la siguiente generación.

## Dónde va cada cosa
- Trucos (antes `#trucos` de index.html) → `_build/cheats.py`. Código con letras U/D/L/R separadas por espacios; `""` = por descubrir. El formato con flechas y la secuencia de PS5 y Xbox los pone el generador.
- Secretos, easter eggs, misterios, lugares ocultos → lista `SECRETS` (página `/secretos/`).
- Misiones secundarias → `STRANGERS` (`/secundarias/`).
- Dinero → `MONEY` (`/dinero/`). Coleccionables → bloque de `/coleccionables/` (`CARD_SPOTS` y tarjetas). Mapa → `REGIONS` y `SPOTS`. Personajes → `CHARS`. Consejos → `TIPS`.
- Novedades de la portada → `LATEST` (los 6 descubrimientos más recientes).
- Preguntas frecuentes → el parámetro `faq=` de cada página (genera también el JSON-LD).
- Fecha visible → `UPDATED`; fecha del sitemap → `LASTMOD`.

## Enfoque y reglas
- La web trata de lo que se hace dentro del juego. Nada de precios, ventas, bolsa, notas de prensa, marketing ni plataformas.
- Español de España, con palabras propias, sin copiar frases de las fuentes, sin imágenes externas, sin destripes de la historia principal.
- Nada inventado: lo no confirmado se marca como "Rumor" o "Sin confirmar". Un código de truco solo se confirma si lo publican al menos dos fuentes fiables y coinciden.
- Desconfía de guías de "secretos" publicadas antes del 19 de noviembre de 2026: son especulación.
- Si no hay nada nuevo y verificado, no se cambia ni se sube nada.

## Publicar
Commit en `main` con autor `Vicepedia <vicepedia@users.noreply.github.com>` y `git -c push.negotiate=true push origin main`. GitHub Pages publica solo. No borres `google1f2797058b1f53ed.html` (verificación de Google Search Console).
