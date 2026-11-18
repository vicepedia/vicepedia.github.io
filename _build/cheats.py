# -*- coding: utf-8 -*-
# Datos de los trucos. Código: U=↑ D=↓ L=← R=→ separados por espacios; "" = por descubrir.
A = {"U": "↑", "D": "↓", "L": "←", "R": "→"}
def code(s):
    if not s:
        return '<span class="pend">Por descubrir</span>'
    arrows = " ".join(A[c] for c in s.split())
    return ('<span class="code">' + arrows + "</span>"
            '<small class="seq">PS5: ↑ (teléfono) · mantén L1 · R1 · ' + arrows + '</small>'
            '<small class="seq">Xbox: ↑ (teléfono) · mantén LB · RB · ' + arrows + '</small>')

CHEATS = {
 "Jugador": [
  ("250.000 $", "Te da 250.000 $ al instante (se puede repetir).", "U R D L U L D R", "Terminar la historia"),
  ("Borracho", "Jason y Lucía se emborrachan.", "", "Gastar 2.500 $ en alcohol"),
  ("Subir nivel de Heat", "Sube el nivel de calor en todo el mapa.", "L D R D U D U", "Escapar de 3 estrellas 25 veces"),
  ("Subir nivel de búsqueda", "Sube las estrellas de búsqueda.", "", "Escapar de 3 estrellas 50 veces"),
  ("Concentración ilimitada", "La concentración (Focus) no se agota.", "D U U D U D U D U R", "Terminar la historia"),
  ("Sin daño por caída", "Eres inmune a las caídas.", "", "Sobrevivir 20 veces a una caída libre de 40 pies (unos 12 m)"),
  ("Paracaídas", "Añade un paracaídas a tu equipo.", "", "50 saltos en paracaídas o BASE desde 300 pies (unos 90 m) o más"),
  ("Chaleco antibalas", "Añade chaleco a tu equipo.", "D U L U U U U U D D", "Completar 100 entrenamientos"),
  ("Reparar vehículo", "Repara por completo tu vehículo actual.", "", "Ganar 10 carreras en Gellhorn Raceway, Thrillbilly Mud Club y Boone Speedway"),
  ("Nitro ilimitado", "Nitro y combustible infinitos.", "", "Completar 50 saltos acrobáticos"),
 ],
 "Combate": [
  ("Munición máxima", "Llena toda la munición.", "D U R D L L U U D L", "25 medallas de bronce o mejores en galerías de tiro"),
  ("Munición infinita", "La munición no se acaba.", "D U R D L L U D D D", "25 medallas de plata o mejores en galerías de tiro"),
  ("Sin recarga", "Munición infinita y sin recargar.", "D U R D L L U D D U", "25 medallas de oro en galerías de tiro"),
  ("Todas las armas explosivas", "Todas las armas explosivas con munición llena.", "", "Lanzar 100 granadas"),
  ("Munición incendiaria", "Toda la munición es incendiaria.", "", "Quemar a 100 enemigos"),
  ("Botellas explosivas", "Las botellas explotan al dañarse.", "", "Lanzar 100 cócteles molotov"),
  ("Escopeta explosiva", "Mason & Keen Shortstraw con cartuchos explosivos.", "", "Alcanzar a 100 enemigos con daño explosivo"),
  ("Hauners H-AT", "Añade el lanzador Hauners H-AT.", "", "Volar 100 vehículos"),
  ("Fuerza de ataque", "Balas y golpes lanzan por los aires a los objetivos.", "D U L L R D D U D", "Terminar la historia"),
  ("Balones explosivos", "Los balones deportivos explotan al impactar.", "D U L L R D D U R", "Alcanzar a 20 enemigos con daño explosivo"),
  ("Fuerza de vehículo", "Los choques lanzan por los aires a los objetivos.", "D U L L R D L U D", "Matar a 25 enemigos con un vehículo"),
 ],
 "Vehículos": [
  ("Interstate Ambulance", "Ambulancia.", "", "Descubrirla en el menú de progreso"),
  ("Airboat 09", "Hidrodeslizador para los pantanos.", "", "5 desafíos de supervivencia"),
  ("Bravado Banshee", "Deportivo.", "", "Todos los desafíos de combate"),
  ("Tuff BMX", "Bici BMX.", "", "5 desafíos de fitness"),
  ("Maibatsu Boomazoom", "Vehículo Maibatsu.", "L U R D L L U L", "5 desafíos de compras"),
  ("Nagasaki Carbon RS", "Moto deportiva.", "", "Todos los desafíos de exploración"),
  ("'65 Vapid Dominator", "Muscle car clásico.", "", "Todos los desafíos de fitness"),
  ("Progen Emerus", "Superdeportivo.", "", "Todos los desafíos de vehículos"),
  ("Flamenco hinchable", "Un flamenco hinchable para el agua.", "", "Destruir 50 flamencos de cocaína"),
  ("MTL Pumper", "Camión de bomberos.", "L U R D L R R U", "Desconocido"),
  ("Vapid Stanier G2 Taxi", "Taxi.", "", "5 desafíos deportivos"),
  ("Hauners P-996 Lazer", "Caza militar.", "", "Todos los desafíos"),
  ("HVY Bulldozer", "Bulldozer.", "L U R D L R R D", "Descubrirlo en el menú de progreso"),
  ("Lapwing Mallard", "Avioneta.", "", "5 desafíos de vehículos"),
  ("Brimstone Golfer", "Carrito de golf.", "", "Todos los desafíos deportivos"),
  ("Hauners Rhino Tank", "Tanque.", "", "Todos los desafíos de supervivencia"),
  ("Maibatsu Sanchez", "Moto de cross.", "", "5 desafíos criminales"),
  ("Nagasaki Sea Sparrow", "Helicóptero anfibio.", "", "5 desafíos de exploración"),
  ("Speeder 700 GT", "Lancha.", "", "5 desafíos de combate"),
  ("Truffade Thrax", "Hiperdeportivo.", "", "Todos los desafíos de compras"),
  ("Western Zombie Bobber", "Moto custom.", "", "Todos los desafíos criminales"),
 ],
 "Entorno": [
  ("Adelantar la hora", "Avanza la hora del día.", "", "Encontrar 10 relojes coleccionables"),
  ("Pausar la hora", "Detiene el ciclo día/noche.", "", "Encontrar 20 relojes coleccionables"),
  ("Cambiar el clima", "Alterna entre climas.", "D R U D R U R", "Terminar la historia"),
 ],
 "Filtros": [
  ("Golden Hour", "Filtro dorado y formato panorámico.", "", "Pasar 4 horas cogidos de la mano"),
  ("Powdered Sugar", "Mundo blanco con destellos.", "", "Escanear toda la chatarra espacial con WAiNK"),
  ("Pinhole", "Filtro de cámara estenopeica.", "", "Limpiar 25 operaciones de bandas con tu pareja"),
  ("Neon Jungle", "Reflejos de neón en todo el mundo.", "", "Descubrir los 16 vehículos Girlypop"),
  ("Yesteryear", "Tele CRT en blanco y negro.", "", "Descubrir el Ridgeway"),
  ("Cataclysm", "Humo turbio por todas partes.", "D D U R R U L L R R", "Descubrir el Vamos de Martha en el menú de progreso"),
  ("Videotape", "Estilo cinta de vídeo.", "", "50 actividades con tu pareja"),
  ("Dark Mirror", "Da la vuelta al mundo y lo vuelve negro.", "", "Ganar 500.000 $ vendiendo vehículos"),
  ("Migraine", "Imagen borrosa y distorsionada.", "", "Sobrevivir 6 minutos con 6 estrellas"),
  ("Dollhouse", "Colores vivos y formato estrecho.", "D D U R R U L L D R", "Pasar 8 horas con tu pareja"),
  ("Bubblegum", "Mundo morado y amarillo con destellos.", "", "Las 24 cartas de los Vice City Flamingos"),
  ("Fast Forward", "Desenfoque de movimiento y nubes rápidas.", "", "Completar 50 meditaciones"),
  ("Fisheye", "Ojo de pez.", "", "Pescar 100 peces"),
  ("Faded Glory", "Tele CRT en color.", "D D U R R U L L L R", "Atracar 50 tiendas con tu pareja"),
  ("Pixel Art", "Imagen pixelada.", "", "Ganar 250.000 $ vendiendo coleccionables"),
  ("Hellscape", "Mundo rojo y naranja con calima.", "", "Robar 100 coches de policía"),
 ],
}

