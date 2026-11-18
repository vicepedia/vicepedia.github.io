# -*- coding: utf-8 -*-
"""Genera la web multipágina de Vicepedia en el repositorio."""
import json, html, os, re, unicodedata, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
BASE = "https://vicepedia.github.io"
UPDATED = "19 de noviembre de 2026"
LASTMOD = "2026-11-19"

def esc(s): return html.escape(s, quote=True)
def slug(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

# ---------- trucos (reutiliza los datos ya verificados) ----------
sys.path.insert(0, HERE)
from cheats import CHEATS, A

def code_html(s):
    if not s:
        return '<span class="pend">Por descubrir</span>'
    arrows = " ".join(A[c] for c in s.split())
    return ('<span class="code">' + arrows + '</span>'
            '<small class="seq">PS5: ↑ (teléfono) · mantén L1 · R1 · ' + arrows + '</small>'
            '<small class="seq">Xbox: ↑ (teléfono) · mantén LB · RB · ' + arrows + '</small>')

INDEX = []  # buscador global: (título, texto, url)
def idx(title, text, url): INDEX.append({"t": title, "x": text, "u": url})

# ---------- plantilla ----------
NAV = [("/trucos/", "Trucos"), ("/dinero/", "Dinero"), ("/secretos/", "Secretos"),
       ("/secundarias/", "Secundarias"), ("/coleccionables/", "Coleccionables"),
       ("/mapa/", "Mapa"), ("/personajes/", "Personajes"), ("/consejos/", "Consejos")]

def page(path, title, desc, h1, eyebrow, intro, body, faq=None, crumbs=True):
    url = BASE + path
    nav = "\n".join(f'<a href="{h}"{" aria-current=\"page\"" if h == path else ""}>{n}</a>' for h, n in NAV)
    ld = [{"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": url,
           "dateModified": LASTMOD, "inLanguage": "es",
           "isPartOf": {"@type": "WebSite", "name": "Vicepedia", "url": BASE + "/"}}]
    if crumbs and path != "/":
        ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Vicepedia", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": h1, "item": url}]})
    faq_html = ""
    if faq:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
        faq_html = ('<section id="preguntas"><h2>Preguntas <em>frecuentes</em></h2>' +
                    "".join(f'<details class="s"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faq) +
                    "</section>")
        for q, a in faq: idx(q, a, path + "#preguntas")
    ld_html = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    doc = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Vicepedia">
<meta property="og:locale" content="es_ES">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Work+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
{ld_html}
</head>
<body>
<div class="top">
  <div class="wrap">
    <a class="brand" href="/">VICE<span>PEDIA</span></a>
    <div class="search">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
      <input id="q" type="search" placeholder="Busca en toda la guía: Bigfoot, dinero, chaleco, Yago…" aria-label="Buscar en toda la guía" autocomplete="off">
      <div class="results" id="results" role="listbox" hidden></div>
    </div>
  </div>
  <nav class="chips" aria-label="Secciones">{nav}</nav>
</div>
<header class="hero">
  <div class="wrap">
    <div class="eyebrow">{esc(eyebrow)} · actualizada el {UPDATED}</div>
    <h1>{esc(h1)}</h1>
    <p class="lede">{intro}</p>
  </div>
</header>
<main class="wrap">
{body}
{faq_html}
</main>
<footer>
  <div class="wrap">
    <nav class="foot-nav" aria-label="Todas las secciones"><a href="/">Inicio</a>{"".join(f'<a href="{h}">{n}</a>' for h, n in NAV)}</nav>
    <p><strong>Vicepedia es una web fan no oficial.</strong> No tiene relación con Rockstar Games ni con Take-Two Interactive. Grand Theft Auto, GTA VI y todos los nombres relacionados son marcas de sus respectivos propietarios. La información procede de guías y prensa especializada y la actualizamos a medida que la comunidad descubre más del juego. Sin destripes de la historia principal.</p>
  </div>
</footer>
<script src="/assets/app.js" defer></script>
</body>
</html>
"""
    d = os.path.join(OUT, path.strip("/"))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(doc)
    return path

def cards(items, cls=""):
    """items: (titulo, etiqueta, texto, url_base)"""
    out = []
    for t, tag, txt, base in items:
        i = slug(t)
        out.append(f'<article class="card s {cls}" id="{i}"><span class="tag">{esc(tag)}</span><h3>{esc(t)}</h3><p>{txt}</p></article>')
        idx(t, re.sub("<[^>]+>", "", txt), base + "#" + i)
    return '<div class="grid">' + "\n".join(out) + "</div>"

def stats(items):
    return '<div class="stats">' + "".join(f'<div class="stat"><b>{esc(n)}</b><span>{esc(l)}</span></div>' for n, l in items) + "</div>"

PAGES = []

# =====================================================================
# TRUCOS
# =====================================================================
total = sum(len(v) for v in CHEATS.values())
known = sum(1 for v in CHEATS.values() for r in v if r[2])
groups = []
for cat, rows in CHEATS.items():
    cs = slug(cat)
    trs = []
    for n, e, c, u in rows:
        i = "truco-" + slug(n)
        trs.append(f'<tr class="s" id="{i}" data-known="{1 if c else 0}"><td><strong>{esc(n)}</strong><small>{esc(e)}</small></td><td>{code_html(c)}</td><td>{esc(u)}</td></tr>')
        idx("Truco: " + n, e + " Cómo se desbloquea: " + u, "/trucos/#" + i)
    groups.append(f'<div class="cheat-group" data-cat="{cs}"><h3>{cat} <span class="count">{len(rows)}</span></h3>'
                  '<div class="table-wrap"><table><thead><tr><th>Truco</th><th>Código</th><th>Cómo se desbloquea</th></tr></thead><tbody>'
                  + "".join(trs) + "</tbody></table></div></div>")
btns = '<button type="button" data-f="all" aria-pressed="true">Todos</button>' + "".join(
    f'<button type="button" data-f="{slug(c)}" aria-pressed="false">{c}</button>' for c in CHEATS)
body = f"""
<section id="como-se-meten">
  <p class="note"><strong>Cómo se meten:</strong> abre el teléfono con la cruceta (↑), mantén L1/LB, pulsa R1/RB e introduce la combinación con la cruceta. La lista aparece en Menú de progreso &gt; Trucos cuando terminas la historia. <strong>Ojo:</strong> usar cualquier truco desactiva los trofeos y el guardado, así que guarda antes.</p>
  <div class="filters" role="group" aria-label="Filtrar trucos">{btns}
    <label for="onlyKnown"><input type="checkbox" id="onlyKnown"> Solo con código conocido</label>
  </div>
  {"".join(groups)}
</section>"""
PAGES.append(page("/trucos/", "Trucos de GTA 6: los 61 códigos y cómo desbloquearlos",
    f"Lista completa de los {total} trucos de GTA 6 para PS5 y Xbox: código con la cruceta, qué hace cada uno y el reto que lo desbloquea. {known} códigos confirmados.",
    f"Los {total} trucos de GTA 6", "Trucos",
    f"GTA 6 recupera los trucos de toda la vida, pero hay que ganárselos: cada uno se desbloquea al terminar la historia y cumplir un reto concreto. Ya conocemos {known} combinaciones y añadimos el resto en cuanto se confirman.",
    body,
    faq=[("¿Cuándo se pueden usar los trucos en GTA 6?", "Solo después de terminar la historia, y cada truco exige además cumplir su propio reto, por ejemplo completar 100 entrenamientos para el chaleco antibalas."),
         ("¿Los trucos desactivan los trofeos?", "Sí. Usar cualquier truco desactiva los trofeos y logros y también el guardado de la partida."),
         ("¿Hay truco de dinero en GTA 6?", "Sí, uno: da 250.000 $ y se puede repetir. Se desbloquea al terminar la historia y su código es ↑ → ↓ ← ↑ ← ↓ →."),
         ("¿Por qué no funciona un truco?", "Porque todavía no lo has desbloqueado. Si metes un código antes de cumplir su reto, no pasa nada. Mira su requisito en la tabla.")]))

# =====================================================================
# DINERO
# =====================================================================
MONEY = [
 ("Atracar tiendas", "Capítulo 1", "Unos miles de $", "Gasolineras y tiendas de barrio. Poco riesgo y dinero rápido para empezar."),
 ("Vender coches a Moses", "Capítulo 2", "Desde 1.000 $ por coche", "Te compra coches robados, pero sin localizador. Es una de sus misiones de Desconocidos y Locos."),
 ("Buceo de tesoros para Kenton", "Al principio, en Key Lento", "Decenas de miles en total", "Uno de los métodos más rentables y sin persecuciones. Kenton tiene 7 lotes de tesoros."),
 ("Operaciones de bandas", "Icono amarillo en el mapa", "Alto", "Hay 39 escondites de bandas para robar dinero, droga y objetos de valor. Mejor con tu pareja."),
 ("Joyerías", "Capítulo 3", "10.000–25.000 $", "Se pueden encadenar. Yasmani también te ofrece trabajos de joyerías, cajeros y préstamos rápidos."),
 ("Coches de lujo para Randy", "Capítulo 3", "30.000 $ o más", "Coches de gama alta y limpios de su lista de deseos."),
 ("Vehículos con localizador en Pay 'n' Spray", "Capítulo 3", "Desde 4.000 $", "La salida para los coches que no acepta Moses. Hay 19 Pay 'n' Spray en el mapa."),
 ("Grandes cámaras acorazadas", "Final del capítulo 4", "Hasta 205.000 $", "Se desbloquean con la misión opcional That's Where The Money Is… Hay 8 bancos grandes y 14 pequeños."),
 ("Vender cartas coleccionables", "Siempre", "20 $–1.000 $ o más por carta", "En cualquier casa de empeños. Venderlas no las quita de tu colección."),
 ("Misiones de Kirk", "Desde el capítulo 1", "1.000 $ la primera", "La búsqueda del Skunk Ape paga 1.000 $ y abre una de las historias más curiosas del juego."),
]
rows = []
for a, b, c, d in MONEY:
    i = slug(a)
    rows.append(f'<tr class="s" id="{i}"><td><strong>{esc(a)}</strong><small>{esc(d)}</small></td><td>{esc(b)}</td><td class="num">{esc(c)}</td></tr>')
    idx("Dinero: " + a, d + " " + c, "/dinero/#" + i)
body = f"""
<section id="metodos">
  <h2>Los métodos, de principio a <em>fin</em></h2>
  <div class="table-wrap"><table><thead><tr><th>Método</th><th>Cuándo</th><th>Cuánto</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
</section>
<section id="golpes">
  <h2>Cuántos golpes hay en <em>Leonida</em></h2>
  {stats([("11","tipos de robo"),("39","operaciones de bandas"),("22","atracos a bancos"),("35","robos relámpago"),("7","préstamos rápidos"),("7","peristas para vender lo robado")])}
</section>
<section id="reglas">
  <h2>Tres reglas para no <em>perderlo</em></h2>
  {cards([
    ("Ingresa el dinero en el cajero", "Clave", "Si te detienen o te matan, pierdes lo que llevas encima. Ingrésalo en un cajero (BuckMe) después de cada golpe.", "/dinero/"),
    ("Jason y Lucía comparten cartera", "Bueno saberlo", "Lo que gana uno lo puede gastar el otro, así que no hace falta repartir.", "/dinero/"),
    ("La historia te pedirá dinero", "Ojo", "Algunas misiones exigen tener una cantidad mínima antes de empezar. Ganar dinero en el mundo abierto forma parte del avance.", "/dinero/"),
    ("Lo robado hay que venderlo", "Peristas", "El botín va a una bolsa y no se convierte en dinero hasta que lo vendes al perista adecuado. Hay 7 en el mapa.", "/dinero/"),
  ])}
</section>"""
PAGES.append(page("/dinero/", "Cómo ganar dinero rápido en GTA 6: los mejores métodos",
    "Los mejores métodos para ganar dinero en GTA 6 ordenados por capítulo: tiendas, Moses, Kenton, joyerías, Randy y las cámaras de hasta 205.000 $.",
    "Cómo ganar dinero rápido en GTA 6", "Dinero",
    "Del atraco a la gasolinera del capítulo 1 a las cámaras acorazadas de hasta 205.000 $. Estos son los métodos que mejor pagan en cada momento de la historia.",
    body,
    faq=[("¿Cuál es la forma más rápida de ganar dinero en GTA 6?", "Las grandes cámaras acorazadas, con hasta 205.000 $, pero llegan al final del capítulo 4. Antes, lo mejor es el buceo de tesoros para Kenton, las joyerías y los coches para Randy."),
         ("¿Se pierde el dinero al morir en GTA 6?", "Sí, el que llevas encima. Ingrésalo en un cajero después de cada golpe para no perderlo.")]))

# =====================================================================
# SECRETOS
# =====================================================================
SECRETS = [
 ("El Skunk Ape (Bigfoot) existe", "Easter egg", "Por fin es real. Es un encuentro aleatorio en los pantanos del sur de Grassrivers, cerca del lago Cottonmouth y del puente hacia allí. Lo oirás rugir antes de verlo. Acércate y usa el Modo Foto para verlo bien. Se puede encontrar en cuanto se abre el mundo libre."),
 ("El piso de Dexter Morgan", "Easter egg", "El apartamento del forense asesino de la serie está en Washington Island, en Vice City, cerca de la tienda de drones Top Fun de Vice Beach."),
 ("Un huevo de Pascua literal", "Easter egg", "En lo alto del rascacielos más alto de Vice City hay un nido con un huevo que puedes coger y lanzar. Subir lleva unos siete minutos."),
 ("Guiños a Red Dead Redemption", "Easter egg", "Hay recuerdos de Red Dead repartidos por Leonida. Uno de los más claros está en Jacob's Tavern, en Millport."),
 ("Dinero bajo el suelo de Jason", "Lugar oculto", "Debajo de las tablas del suelo del dormitorio de Jason hay un alijo de dinero, muy útil antes de tener acceso al banco."),
 ("La historia de las fresas", "Secundaria oculta", "Un cartel en una granja pide un piloto. Si te acercas, empieza una trama secundaria sobre fresas con metanfetamina que acaba con un guiño a un superhéroe muy conocido."),
 ("Una pista de aterrizaje escondida", "Lugar oculto", "Una pista oculta llena de aviones clásicos y antiguos. No aparece marcada en el mapa: hay que encontrarla explorando."),
 ("La categoría “?” del menú de progreso", "Sin resolver", "Dentro de Exploración, el menú de progreso tiene una categoría sin nombre que la comunidad aún no ha identificado. Es el gran misterio del momento."),
 ("Equipos de Liberty City y Los Santos", "Easter egg", "Entre los 18 juegos de cartas coleccionables hay equipos de Liberty City y Los Santos, las ciudades de GTA IV y GTA V."),
 ("El Ridgeway y el Vamos de Martha", "Por investigar", "Dos vehículos especiales que desbloquean filtros secretos solo con descubrirlos. Aún se sabe muy poco de dónde aparecen."),
 ("Los 16 vehículos Girlypop", "Coleccionable secreto", "Una serie de coches especiales repartidos por Leonida. Si los encuentras todos, desbloqueas el filtro Neon Jungle."),
 ("Chatarra espacial y meteoritos", "Coleccionable secreto", "Con la app WAiNK puedes escanear restos espaciales repartidos por el mapa. Si los escaneas todos, desbloqueas el filtro Powdered Sugar."),
]
body = f"""
<section id="secretos-lista">
  <h2>Lo que ya se ha <em>descubierto</em></h2>
  {cards([(t, g, x, "/secretos/") for t, g, x in SECRETS], "secret")}
</section>
<section id="edificios">
  <h2>Cómo encontrar sitios a los que se puede <em>entrar</em></h2>
  {cards([
    ("Mira el color de los edificios en el mapa", "Truco del mapa", "Los edificios en azul oscuro tienen una entrada o un interior accesible; los de azul claro, no. En el minimapa, una línea blanca marca una puerta por la que se puede pasar.", "/secretos/"),
    ("Usa la Concentración (Focus)", "Truco", "Con la Concentración activada se ven entradas, habitaciones escondidas y puertas con alarma.", "/secretos/"),
    ("Algunos interiores solo se abren en misiones", "Ojo", "Hay edificios de la historia a los que solo se puede entrar durante su misión. Si una puerta no se abre, puede que sea eso.", "/secretos/"),
  ])}
</section>"""
PAGES.append(page("/secretos/", "Secretos y easter eggs de GTA 6: Bigfoot, Dexter y más",
    "Todos los secretos y easter eggs confirmados de GTA 6: dónde encontrar al Skunk Ape (Bigfoot), el piso de Dexter, el huevo del rascacielos, el dinero oculto de Jason y los misterios sin resolver.",
    "Secretos y easter eggs de GTA 6", "Secretos",
    "Bigfoot existe, Dexter tiene piso en Vice City y hay un huevo en lo alto del rascacielos más alto. Estos son los secretos confirmados de Leonida y los misterios que la comunidad aún no ha resuelto.",
    body,
    faq=[("¿Dónde está Bigfoot en GTA 6?", "Es el Skunk Ape, un encuentro aleatorio en los pantanos del sur de Grassrivers, cerca del lago Cottonmouth. Lo oirás rugir antes de verlo."),
         ("¿Dónde está el piso de Dexter en GTA 6?", "En Washington Island, Vice City, cerca de la tienda de drones Top Fun de Vice Beach."),
         ("¿Cómo sé si puedo entrar en un edificio?", "En el mapa, los edificios en azul oscuro tienen interior accesible. Con la Concentración verás además entradas, habitaciones ocultas y puertas con alarma.")]))

# =====================================================================
# SECUNDARIAS
# =====================================================================
STRANGERS = [
 ("Capítulo 1", "Shirley", "Get Shirley's Rum · Steal the Scooter", "Vecina de Jason. Solo en el capítulo 1: si avanzas, se pierden.", "No"),
 ("Capítulo 1", "Kirk", "Search for the Skunk Ape · Search for Tree Effigies · Help Kirk Find Mr. Mangrove", "Empieza leyendo uno de sus carteles (hay uno en el bar Skeeter's, en Hamlet) y llamándole. La primera y la última son de noche; la última, solo con Lucía. No se puede terminar hasta el capítulo 2.", "Sí"),
 ("Capítulo 2", "Kyle", "Check Out McKittrick Farm · Collect Chemicals for Kyle · Buddy? (Check on Kyle)", "En la granja McKittrick, en Kelly County. Al final eliges entre dejarle escapar o ponerte del lado de la policía.", "Sí"),
 ("Capítulo 2", "Moses", "Steal Vehicles for Moses", "Te compra coches robados sin localizador. Muy buena fuente de dinero.", "—"),
 ("Capítulo 2", "Bret Vogel", "Veteran Hunted (Meet Bret) · Bret's Hunting Decks", "Solo con Jason. Caza; sus 15 mazos de caza dan el trofeo Fair Game.", "—"),
 ("Capítulo 2", "Billy", "Thrillbillies · Twist Wrist, Smash, Grab · Mall Rats · The Impaler · Hometown Heroes", "Empieza en el Thrillbilly Mud Club. Termina con el trofeo The Lone Rider.", "No"),
 ("Capítulo 3", "Yago", "Join a Street Race · Bumper to Bumper · Race Against Yago · Brother to Brother", "Carreras callejeras. Race Against Yago es temporal: hazla en cuanto aparezca o la pierdes. Dos misiones son solo con Jason.", "Sí"),
 ("Capítulo 3", "Andy", "Climbing the Cellerichain (1–3) · Pay the Cellerica Fee · Peach! · Read the Label · Puff Puff Pass", "Todas solo con Lucía. Termina con el trofeo Road to Rehabilitation.", "No"),
 ("Capítulo 3", "Yasmani", "Trabajos de joyerías, de cajeros y de préstamos rápidos · Tail the Security Van", "Su tienda está en Little Cuba. Robos que dan mucho dinero.", "No"),
 ("Capítulo 3", "Randy", "Randy's Wish List", "Coches de lujo que pagan 30.000 $ o más. Trofeo Supply & Demand.", "—"),
 ("Capítulo 3", "Tyrone", "Take Out Kitty Litter · Spin On This", "Cierra los laboratorios Kitty Litter. Trofeo Spin On This!", "No"),
 ("Capítulo 3", "Dunk", "Dunk's Robbery Tips", "Consejos y encargos de atracos.", "—"),
 ("Capítulo 4", "Eddie Acosta", "Attend Eddie Acosta's Party", "Una fiesta que no conviene perderse.", "No"),
 ("Capítulo 4", "Pilot Pete", "The Last Mile: Passing the Torch · Backseat Pilot · Pete's Deliveries", "Solo con Jason. Recuperas su avioneta y haces repartos aéreos desde Southpoint Airfield.", "Sí"),
]
rows = []
for ch, who, ms, note, tro in STRANGERS:
    i = "desconocido-" + slug(who)
    rows.append(f'<tr class="s" id="{i}"><td><strong>{esc(who)}</strong><small>{esc(ch)}</small></td><td>{esc(ms)}<small>{esc(note)}</small></td><td>{esc(tro)}</td></tr>')
    idx("Secundaria: " + who, ms + ". " + note, "/secundarias/#" + i)
body = f"""
<section id="perdibles">
  <p class="note"><strong>Antes de avanzar en la historia:</strong> las dos misiones de Shirley solo existen en el capítulo 1, y Race Against Yago desaparece si no la haces cuando sale. El resto de secundarias sigue disponible después de la historia, y nada de lo que cuenta para el 100 % se puede perder.</p>
</section>
<section id="desconocidos">
  <h2>Desconocidos y Locos, por <em>capítulo</em></h2>
  <p class="intro">Para el trofeo Strangers &amp; Freaks hay que completar ocho historias de desconocidos; las de Kirk, Kyle, Yago y Pilot Pete cuentan seguro. En los iconos del mapa, las misiones opcionales aparecen en negro con letras rosas y las tareas secundarias, en morado.</p>
  <div class="table-wrap"><table><thead><tr><th>Personaje</th><th>Misiones</th><th>¿Cuenta para el trofeo?</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
</section>
<section id="actividades">
  <h2>Actividades para cuando no hay <em>misión</em></h2>
  {stats([("40","carreras únicas"),("42","galerías de tiro"),("42","contrarrelojes con dron"),("13","desafíos de carreras"),("5","campos de golf"),("7","rivales de billar"),("4","máquinas recreativas"),("80","desafíos")])}
  {stats([("130","saltos acrobáticos"),("202","pasos bajo puentes"),("40","vuelos a cuchillo"),("25","saltos BASE"),("100","canastas"),("255","animales")])}
</section>"""
PAGES.append(page("/secundarias/", "Misiones secundarias de GTA 6: Desconocidos y Locos",
    "Todas las misiones secundarias de Desconocidos y Locos de GTA 6 por capítulo: Kirk y el Skunk Ape, Yago, Kyle, Pilot Pete y las que se pueden perder.",
    "Misiones secundarias de GTA 6", "Secundarias",
    "Quién te da misiones, en qué capítulo aparece, cuáles son solo para Jason o para Lucía y, sobre todo, cuáles se pierden si avanzas en la historia. Sin destripes.",
    body,
    faq=[("¿Qué misiones secundarias se pueden perder en GTA 6?", "Las dos de Shirley, que solo existen en el capítulo 1, y Race Against Yago, que es temporal. Ninguna cuenta para el 100 %."),
         ("¿Cuántas historias hacen falta para el trofeo Strangers & Freaks?", "Ocho historias de desconocidos. Las de Kirk, Kyle, Yago y Pilot Pete cuentan seguro.")]))

# =====================================================================
# COLECCIONABLES
# =====================================================================
CARD_SETS = ["Vice City Flamingos (24)", "Vice City Narcos (24)", "Vice City Manatees (24)", "Vice City Club De Fútbol (30)",
             "Liberty City Swingers (24)", "Liberty City Penetrators (24)", "Liberty City Wrath (24)", "Los Santos Corkers (24)",
             "Los Santos Panic", "Los Santos Pounders", "Backyard Wrestling"]
CARD_SPOTS = [
 ("Julian Cruz (oro, Vice City Flamingos)", "Vice City, Little Cuba: en el edificio justo al sur de la tienda de Yasmani, en un despacho pequeño del lado norte del pasillo largo, sobre un tablón."),
 ("Mateo Caballero (plata, Vice City Flamingos)", "Vice City, La Perle: en un dormitorio de una casa al norte del local de Zenon."),
 ("Sammy Wordsworth (Vice City Flamingos)", "Port Gellhorn: en el garaje detrás de Sarena's Bargain Store."),
 ("Charlie Spears (Vice City Flamingos)", "Port Gellhorn: en un edificio restringido junto al helipuerto al lado de Gellhorn Speedway, en una caja cerrada de un almacén del piso de arriba."),
 ("Lupin de Juarez (Vice City Club de Fútbol)", "Key Lento: en una caravana al este de The Rusty Anchor."),
 ("D'Angelou Miles (Liberty City Penetrators)", "Key Lento: en el edificio rectangular al que se puede entrar, justo al sur de The Rusty Anchor."),
]
rows = "".join(f'<tr class="s" id="carta-{slug(n)}"><td><strong>{esc(n)}</strong></td><td>{esc(w)}</td></tr>' for n, w in CARD_SPOTS)
for n, w in CARD_SPOTS: idx("Carta: " + n, w, "/coleccionables/#carta-" + slug(n))
body = f"""
<section id="resumen">
  <h2>Todo lo que hay que <em>coleccionar</em></h2>
  <p class="intro">El menú de progreso tiene unas 3.000 entradas entre vehículos, animales, armas, objetos y actividades. La mayoría no se marca en el mapa hasta que la encuentras, pero nada de lo que cuenta para el 100 % se puede perder. El 100 % de la lista lleva unas 200 horas; el 100 % real, más de 300.</p>
  {stats([("480","cartas en 18 colecciones"),("125","flamencos de cocaína"),("34","relojes de lujo"),("33","hallazgos submarinos"),("27","revistas, libros y cómics"),("18","lugares de meditación"),("7","intercambios de libros"),("79","estilos")])}
  {stats([("557","vehículos"),("196","armas y variantes"),("255","animales"),("31","monumentos WAiNK"),("35","curiosidades WAiNK"),("23","esculturas WAiNK"),("23","grafitis No Flusher"),("12","piezas de equipo")])}
</section>
<section id="cartas">
  <h2>Cartas <em>coleccionables</em></h2>
  <p class="intro">Hay 18 colecciones con 480 cartas en total. Con 3 colecciones completas consigues el trofeo Don't Touch My Deck; con 15, el que cuenta para el 100 % (A Long Road). Cada carta se puede vender en cualquier casa de empeños por entre 20 $ y más de 1.000 $ según su rareza, y venderla no la quita de tu colección. Completar los Vice City Flamingos desbloquea el filtro Bubblegum.</p>
  <div class="tags">{"".join(f'<span class="chip-s s">{esc(c)}</span>' for c in CARD_SETS)}</div>
  <h3 class="sub">Algunas ubicaciones</h3>
  <div class="table-wrap"><table><thead><tr><th>Carta</th><th>Dónde está</th></tr></thead><tbody>{rows}</tbody></table></div>
</section>
<section id="otros">
  <h2>Coleccionables que desbloquean <em>trucos</em></h2>
  {cards([
    ("Relojes coleccionables", "Truco", "Con 10 relojes desbloqueas el truco para adelantar la hora; con 20, el de pausarla.", "/coleccionables/"),
    ("Flamencos de cocaína", "Truco", "Hay 125. Destruir 50 desbloquea el flamenco hinchable.", "/coleccionables/"),
    ("Chatarra espacial (WAiNK)", "Filtro", "Escanéala toda con la app WAiNK para el filtro Powdered Sugar.", "/coleccionables/"),
    ("Vehículos Girlypop", "Filtro", "Encuentra los 16 para el filtro Neon Jungle.", "/coleccionables/"),
    ("Lotes de Kenton", "Dinero", "7 lotes de tesoros submarinos que dan decenas de miles de dólares.", "/coleccionables/"),
    ("Mazos de caza de Bret", "Trofeo", "15 mazos de caza que dan el trofeo Fair Game.", "/coleccionables/"),
  ])}
</section>"""
PAGES.append(page("/coleccionables/", "Coleccionables de GTA 6: cartas, relojes, flamencos y más",
    "Todos los coleccionables de GTA 6: las 480 cartas en 18 colecciones, 125 flamencos, 34 relojes, 33 hallazgos submarinos y qué desbloquea cada uno.",
    "Coleccionables de GTA 6", "Coleccionables",
    "Cartas, relojes, flamencos, chatarra espacial, tesoros submarinos… Cuántos hay de cada uno, qué desbloquean y dónde están los que ya se han localizado.",
    body,
    faq=[("¿Cuántas cartas coleccionables hay en GTA 6?", "480 cartas repartidas en 18 colecciones. Para el 100 % hacen falta 15 colecciones completas."),
         ("¿Se pueden perder coleccionables en GTA 6?", "No. Nada de lo que cuenta para el 100 % se puede perder: puedes buscarlo después de la historia.")]))

# =====================================================================
# MAPA
# =====================================================================
REGIONS = [
 ("Vice City", "La gran ciudad, inspirada en Miami. Barrios como Little Cuba, La Perle, Washington Island y Vice Beach. Neón, playas, clubs y casi todos los negocios."),
 ("Leonida Keys", "La cadena de islas del sur. En Key Lento, junto a The Rusty Anchor, empieza el buceo de tesoros con Kenton y hay varias cartas coleccionables."),
 ("Grassrivers", "Los pantanos al estilo de los Everglades. Caimanes, hidrodeslizadores, el lago Cottonmouth y, si tienes suerte, el Skunk Ape."),
 ("Port Gellhorn", "Ciudad costera venida a menos, con el circuito Gellhorn Raceway, tiendas de saldo y garajes donde se esconden coleccionables."),
 ("Ambrosia", "Zona industrial y rural del interior."),
 ("Mount Kalaga National Park", "El parque natural del norte: bosques, ríos y la zona más salvaje del mapa, ideal para caza, pesca y exploración."),
]
SPOTS = [("Hamlet", "Bar Skeeter's, con un cartel de Kirk"), ("Millport", "Jacob's Tavern y su guiño a Red Dead"),
         ("Kelly County", "Granja McKittrick (misiones de Kyle)"), ("Mariana County", "Pelican Valley (misiones de Kirk)"),
         ("Southpoint Airfield", "Repartos de Pilot Pete"), ("Thrillbilly Mud Club", "Carreras y las misiones de Billy"),
         ("Boone Speedway", "Carreras"), ("Washington Island", "El piso de Dexter")]
SERV = [("57","gasolineras"),("19","Pay 'n' Spray"),("14","talleres de tuneo"),("24","Ammu-Nation"),("12","garajes"),("25","estaciones de tren"),("67","tiendas de ropa"),("11","estudios de tatuaje")]
body = f"""
<section id="regiones">
  <h2>Las seis regiones de <em>Leonida</em></h2>
  <p class="intro">El estado ficticio inspirado en Florida es unas dos veces más grande que el mapa de GTA V y casi todo está abierto desde el principio. Lo mejor es explorar a fondo la zona en la que estás antes de lanzarte a recorrerlo todo.</p>
  {cards([(n, f"Región {i+1:02d}", d, "/mapa/") for i, (n, d) in enumerate(REGIONS)], "region")}
</section>
<section id="lugares">
  <h2>Lugares que conviene <em>conocer</em></h2>
  {cards([(n, "Lugar", d, "/mapa/") for n, d in SPOTS])}
</section>
<section id="servicios">
  <h2>Servicios por todo el <em>mapa</em></h2>
  {stats(SERV)}
</section>"""
PAGES.append(page("/mapa/", "Mapa de GTA 6: las 6 regiones de Leonida y sus lugares clave",
    "Guía del mapa de GTA 6: las seis regiones de Leonida (Vice City, Leonida Keys, Grassrivers, Port Gellhorn, Ambrosia, Mount Kalaga), lugares clave y servicios.",
    "El mapa de Leonida", "Mapa",
    "Seis regiones, de los neones de Vice City a los pantanos de Grassrivers. Qué hay en cada una y qué lugares tienes que conocer.",
    body))

# =====================================================================
# PERSONAJES
# =====================================================================
CHARS = [
 ("Lucía Caminos", "Protagonista", "La gran protagonista y el personaje más buscado de todo el juego. La conocemos saliendo de prisión, decidida a darle la vuelta a su vida en Vice City junto a Jason."),
 ("Jason Duval", "Protagonista", "Creció rodeado de estafadores y delincuentes. Trabaja para Brian y vive en una de sus propiedades. Bajo el suelo de su dormitorio hay un alijo de dinero."),
 ("Cal Hampton", "Amigo de Jason", "Socio de Brian y colega de Jason. Prefiere quedarse en casa escuchando las comunicaciones de la Guardia Costera. Te reta a un concurso de pesca."),
 ("Brian Heder", "Casero y contrabandista", "Contrabandista veterano y casero de Jason, al que aloja a cambio de trabajos sucios."),
 ("Raul Bautista", "Atracador de bancos", "Un atracador veterano y carismático al que le gusta subir la apuesta en cada golpe."),
 ("Boobie Ike", "Empresario de Vice City", "Leyenda local con inmobiliarias, un club de striptease y un estudio de grabación."),
 ("Dre'Quan Priest", "Magnate musical", "Socio de Boobie en el negocio de la música."),
 ("Real Dimez", "Dúo de rap", "Bae-Luxe y Roxy, dúo de rap convertido en sensación de las redes de Leonida."),
]
body = f"""
<section id="principales"><h2>Los <em>protagonistas</em> y su círculo</h2>{cards([(n, r, d, "/personajes/") for n, r, d in CHARS], "char")}</section>
<section id="cambio"><p class="note"><strong>Cambiar de personaje:</strong> puedes pasar de Jason a Lucía en cualquier momento pulsando abajo en la cruceta. Algunas misiones secundarias son solo para uno de los dos: consulta la página de <a href="/secundarias/">secundarias</a>.</p></section>
<section id="desconocidos-p"><h2>Los desconocidos que te dan <em>misiones</em></h2>
{cards([("Kirk", "Cazador de criaturas", "Busca al Skunk Ape. Sus carteles están por todo Grassrivers.", "/personajes/"),
        ("Yago", "Piloto callejero", "Carreras callejeras en Vice City. Una de sus misiones es temporal.", "/personajes/"),
        ("Kenton", "Buscador de tesoros", "Buceo en los Cayos. Uno de los mejores métodos para ganar dinero.", "/personajes/"),
        ("Moses y Randy", "Compradores de coches", "Moses compra coches robados; Randy, coches de lujo por 30.000 $ o más.", "/personajes/"),
        ("Pilot Pete", "Piloto", "Repartos aéreos, solo con Jason.", "/personajes/"),
        ("Bret Vogel", "Cazador veterano", "Caza y sus mazos de caza, solo con Jason.", "/personajes/")])}</section>"""
PAGES.append(page("/personajes/", "Personajes de GTA 6: Lucía, Jason y quién es quién",
    "Todos los personajes de GTA 6: Lucía Caminos, Jason Duval, Cal, Brian, Raul, Boobie, Dre'Quan, Real Dimez y los desconocidos que te dan misiones.",
    "Personajes de GTA 6", "Personajes",
    "Quién es quién en Leonida, sin destripes de la historia: los protagonistas, su círculo y los desconocidos que te darán trabajo.",
    body,
    faq=[("¿Se puede cambiar entre Jason y Lucía?", "Sí, en cualquier momento pulsando abajo en la cruceta. Comparten la misma cartera.")]))

# =====================================================================
# CONSEJOS
# =====================================================================
TIPS = [
 ("Cámbiate de ropa para despistar a la policía", "Policía", "La policía te identifica por la ropa, el coche y el arma. Lleva ropa de repuesto en el maletero y cámbiate, o córtate el pelo, para bajar el Heat. Separaos si os buscan como pareja."),
 ("Entiende el sistema de Heat", "Policía", "Solo te buscan si alguien te ve, una víctima te denuncia o te graba una cámara. Las estrellas huecas significan que saben del delito, pero no quién fue. Hay hasta seis estrellas."),
 ("Guarda a mano antes de cada misión importante", "Básico", "Te ahorrará repetir mucho si algo sale mal, sobre todo antes de golpes grandes."),
 ("Ve en sigilo y usa la Concentración", "Combate", "Muchos golpes se pueden hacer sin disparar: esquiva o neutraliza a los guardias antes de que den la alarma y usa la Concentración para ralentizar el tiempo."),
 ("Pon gasolina", "Coches", "Los coches gastan combustible. Mantén R2/RT unos diez segundos en una gasolinera. Los Pay 'n' Spray reparan y quitan la búsqueda del vehículo."),
 ("Cuida la relación con tu pareja", "Pareja", "La relación entre Jason y Lucía tiene cuatro niveles. Quedar, interesarse y mostrar cariño la mejora, y lo que hagáis el uno por el otro pesa en el final que ves."),
 ("Explora tu zona antes de correr", "Exploración", "El mapa es enorme. Exprime la región en la que estás: coleccionables fáciles, tiendas y secundarias cercanas."),
 ("Haz ya las secundarias que se pierden", "Ojo", "Las misiones de Shirley solo existen en el capítulo 1 y Race Against Yago es temporal."),
 ("Ajusta el mando", "PS5", "Los gatillos adaptativos y la vibración del DualSense se pueden ajustar en accesibilidad si se hacen pesados en sesiones largas."),
]
body = f"""
<section id="consejos-lista"><h2>Lo que conviene saber desde la primera <em>hora</em></h2>{cards([(t, g, x, "/consejos/") for t, g, x in TIPS])}</section>
<section id="duracion"><h2>Cuánto se tarda en <em>completarlo</em></h2>
{stats([("50–80 h","historia principal"),("5","capítulos"),("~100","misiones de historia"),("~200 h","lista del 100 %"),("300 h o más","100 % real")])}
</section>"""
PAGES.append(page("/consejos/", "Consejos de GTA 6 para empezar: lo que nadie te cuenta",
    "Los mejores consejos para empezar GTA 6: cómo despistar a la policía con el sistema de Heat, sigilo, gasolina, relación con tu pareja y las misiones que se pierden.",
    "Consejos para empezar GTA 6", "Consejos",
    "Cómo funciona la nueva policía, qué hacer en las primeras horas y los errores que te harán perder misiones o dinero.",
    body,
    faq=[("¿Cuánto dura GTA 6?", "La historia principal lleva entre 50 y 80 horas según tu ritmo, en cinco capítulos con unas 100 misiones. La lista del 100 % ronda las 200 horas."),
         ("¿Cuántos finales tiene GTA 6?", "Varios. Tu relación con tu pareja y las decisiones que tomas durante la historia influyen en el final que ves."),
         ("¿Cómo se pierde la búsqueda en GTA 6?", "Sal de la zona de búsqueda y cambia de ropa, de coche o de corte de pelo. Si os buscan como pareja, separaos.")]))

# =====================================================================
# PORTADA
# =====================================================================
SECTIONS = [
 ("/trucos/", "Trucos", f"Los {total} trucos con su código y cómo desbloquear cada uno. {known} confirmados."),
 ("/dinero/", "Dinero", "Del atraco a la gasolinera a las cámaras de 205.000 $."),
 ("/secretos/", "Secretos", "Bigfoot, el piso de Dexter, el huevo del rascacielos y más."),
 ("/secundarias/", "Secundarias", "Desconocidos y Locos por capítulo y las que se pierden."),
 ("/coleccionables/", "Coleccionables", "480 cartas, 125 flamencos, 34 relojes y qué desbloquean."),
 ("/mapa/", "Mapa", "Las seis regiones de Leonida y sus lugares clave."),
 ("/personajes/", "Personajes", "Lucía, Jason y quién es quién, sin destripes."),
 ("/consejos/", "Consejos", "La nueva policía, sigilo y errores que evitar."),
]
LATEST = [
 ("/secretos/#el-skunk-ape-bigfoot-existe", "Bigfoot existe en GTA 6: dónde encontrar al Skunk Ape"),
 ("/secretos/#el-piso-de-dexter-morgan", "El piso de Dexter Morgan está en Washington Island"),
 ("/secretos/#un-huevo-de-pascua-literal", "Hay un huevo de verdad en lo alto del rascacielos más alto"),
 ("/secretos/#dinero-bajo-el-suelo-de-jason", "Dinero escondido bajo el suelo del cuarto de Jason"),
 ("/secundarias/#perdibles", "Las secundarias que se pierden si avanzas en la historia"),
 ("/trucos/", f"{known} códigos de trucos confirmados de {total}"),
]
body = f"""
<section id="secciones"><div class="grid">{"".join(f'<a class="card link-card" href="{h}"><span class="tag">Sección</span><h3>{esc(n)}</h3><p>{esc(d)}</p></a>' for h, n, d in SECTIONS)}</div></section>
<section id="ultimo"><h2>Lo último <em>descubierto</em></h2><ul class="latest">{"".join(f'<li><a href="{h}">{esc(t)}</a></li>' for h, t in LATEST)}</ul></section>"""
PAGES.append(page("/", "Vicepedia: guía de GTA 6 en español con trucos y secretos",
    "Guía de GTA 6 en español: los 61 trucos y cómo desbloquearlos, cómo ganar dinero, secretos y easter eggs como Bigfoot, misiones secundarias, coleccionables y mapa de Leonida.",
    "Todo lo que esconde GTA 6", "Guía fan de GTA 6 en español",
    "Trucos, dinero, secretos, secundarias y coleccionables de Leonida, explicados sin destripes y actualizados cada día. Escribe arriba lo que buscas.",
    body,
    faq=[("¿Hay trucos en GTA 6?", f"Sí, {total}, pero solo se desbloquean al terminar la historia y cumplir el reto de cada uno. Usarlos desactiva los trofeos y el guardado."),
         ("¿Hay Bigfoot en GTA 6?", "Sí: el Skunk Ape aparece de verdad en los pantanos del sur de Grassrivers, cerca del lago Cottonmouth.")], crumbs=False))

# ---------- 404 ----------
open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(
    open(os.path.join(OUT, "index.html"), encoding="utf-8").read()
    .replace("<title>Vicepedia: guía de GTA 6 en español con trucos y secretos</title>", "<title>Página no encontrada · Vicepedia</title>")
    .replace("Todo lo que esconde GTA 6", "Esta página no existe (todavía)"))

# ---------- assets ----------
os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
css = open(os.path.join(HERE, "base.css"), encoding="utf-8").read()
css += """
nav.chips a[aria-current="page"]{border-color:var(--coral);color:var(--coral)}
header.hero{padding:36px 0 22px}
.search .results{position:absolute;left:0;right:0;top:calc(100% + 6px);background:var(--panel);border:1px solid var(--line);border-radius:12px;max-height:60vh;overflow:auto;box-shadow:0 12px 32px rgba(0,0,0,.45);z-index:20}
.search .results a{display:block;padding:10px 14px;color:var(--ink);text-decoration:none;border-bottom:1px solid var(--line)}
.search .results a:last-child{border-bottom:0}
.search .results a:hover,.search .results a:focus{background:rgba(79,214,196,.1);outline:none}
.search .results small{display:block;color:var(--mute);font-size:13px;margin-top:2px}
.search .results .none{padding:12px 14px;color:var(--mute)}
a.link-card{text-decoration:none;color:inherit;transition:border-color .15s}
a.link-card:hover{border-color:var(--coral)}
a.link-card h3{color:var(--ink)}
ul.latest{list-style:none;padding:0;margin:0;display:grid;gap:8px}
ul.latest a{display:block;padding:12px 16px;border:1px solid var(--line);border-radius:10px;color:var(--ink);text-decoration:none;font-weight:600}
ul.latest a:hover{border-color:var(--aqua)}
.tags{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 20px}
.chip-s{font-size:14px;border:1px solid var(--line);border-radius:999px;padding:5px 12px}
h3.sub{margin:8px 0 12px}
td small{max-width:60ch}
.foot-nav{display:flex;flex-wrap:wrap;gap:14px;margin-bottom:14px}
.foot-nav a{color:var(--ink);text-decoration:none;font-weight:600;font-size:14px}
.stats + .stats{margin-top:-8px}
"""
open(os.path.join(OUT, "assets", "style.css"), "w", encoding="utf-8").write(css)

js = "const IDX=" + json.dumps(INDEX, ensure_ascii=False) + ";\n" + r"""
(function(){
  function norm(s){return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'');}
  IDX.forEach(function(e){e.n=norm(e.t+' '+e.x);});
  var q=document.getElementById('q'), box=document.getElementById('results');
  function render(){
    var w=norm(q.value.trim()).split(/\s+/).filter(Boolean);
    if(!w.length){box.hidden=true;box.innerHTML='';return;}
    var hits=IDX.filter(function(e){return w.every(function(x){return e.n.indexOf(x)>-1;});}).slice(0,12);
    box.innerHTML=hits.length?hits.map(function(e){var s=e.x.length>110?e.x.slice(0,110)+'…':e.x;return '<a href="'+e.u+'">'+e.t.replace(/</g,'&lt;')+'<small>'+s.replace(/</g,'&lt;')+'</small></a>';}).join(''):'<div class="none">No hay nada todavía con esa búsqueda. Prueba con otra palabra.</div>';
    box.hidden=false;
  }
  q.addEventListener('input',render);
  q.addEventListener('focus',render);
  document.addEventListener('click',function(e){if(!e.target.closest('.search')) box.hidden=true;});
  document.addEventListener('keydown',function(e){
    if(e.key==='/' && document.activeElement!==q){e.preventDefault();q.focus();}
    if(e.key==='Escape'){box.hidden=true;q.blur();}
  });
  // filtros de la página de trucos
  var btns=document.querySelectorAll('.filters button');
  if(btns.length){
    var cat='all', only=false, rows=[].slice.call(document.querySelectorAll('.cheat-group tr.s'));
    function apply(){
      rows.forEach(function(r){var g=r.closest('.cheat-group');var ok=(cat==='all'||g.dataset.cat===cat)&&(!only||r.dataset.known==='1');r.style.display=ok?'':'none';});
      [].forEach.call(document.querySelectorAll('.cheat-group'),function(g){g.style.display=[].some.call(g.querySelectorAll('tr.s'),function(r){return r.style.display!=='none';})?'':'none';});
    }
    [].forEach.call(btns,function(b){b.addEventListener('click',function(){cat=b.dataset.f;[].forEach.call(btns,function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});apply();});});
    var ok=document.getElementById('onlyKnown'); if(ok) ok.addEventListener('change',function(e){only=e.target.checked;apply();});
  }
  // abre la pregunta enlazada
  if(location.hash){var t=document.getElementById(location.hash.slice(1)); if(t&&t.tagName==='DETAILS') t.open=true;}
})();
"""
open(os.path.join(OUT, "assets", "app.js"), "w", encoding="utf-8").write(js)

# ---------- sitemap y robots ----------
urls = "".join(f"  <url><loc>{BASE}{p}</loc><lastmod>{LASTMOD}</lastmod><changefreq>daily</changefreq><priority>{'1.0' if p=='/' else '0.8'}</priority></url>\n" for p in PAGES)
open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
print("páginas:", len(PAGES), "entradas de búsqueda:", len(INDEX), "trucos:", total, known)
