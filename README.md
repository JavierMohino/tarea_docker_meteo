# Proyecto Docker ETL - Meteorología Villaviciosa de Odón
## Descripción

Este proyecto implementa un flujo ETL usando Docker y Docker Compose.

Incluye:
-Una base de datos MariaDB que tiene la tabla info_meteorologica.
-Un contenedor Python que consulta la API pública de Open-Meteo, transforma los datos y los inserta en la base de datos.

El objetivo es cargar los últimos 7 días (excluyendo hoy) de datos meteorológicos para la ciudad de Villaviciosa de Odón.

## Requisitos
-Tener instalado Docker Desktop (con Docker Compose integrado).
-Conexión a Internet (para entrar a la API de Open-Meteo).

## Instrucciones de ejecución

1-Construir las imágenes (BD y ETL):
-docker compose build

2-Levantar la base de datos:
-docker compose up -d db

3-Ejecutar el ETL (consulta la API y guarda datos en MariaDB):
-docker compose run --rm etl

4-Verificar los datos en la base de datos:
-docker exec -it mariadb_weather mariadb -uweather -pweatherpass -D weatherdb -e "SELECT * FROM info_meteorologica;"

## Estructura del proyecto
tarea_docker
 ├── db
 │   ├── Dockerfile          → Imagen de MariaDB con init.sql
 │   └── init.sql            → Script SQL que crea la BD y la tabla
 ├── etl
 │   ├── Dockerfile          → Imagen de Python para el ETL
 │   ├── requirements.txt    → Dependencias (requests, pymysql, sqlalchemy, dateutil)
 │   └── app.py              → Script ETL: extrae de Open-Meteo y carga en MariaDB
 ├── docker-compose.yml      → Orquesta la BD y el ETL
 └── README.md               → Documentación del proyecto

## Informacíon importante
.La tabla info_meteorologica tiene las columnas: fecha, tmax_c, tmin_c, lluvia_mm, weather_code.
.La columna fecha es única para evitar duplicados.
.El ETL está diseñado para no tener duplicados: si lo ejecutas varias veces, no duplica datos (solo se actualizan si cambian).
.La base de datos conserva los datos gracias al volumen db_data, por lo que los datos se mantienen aunque pares el contenedor.
.El script descarga siempre los últimos 7 días. Esto significa que la tabla se conserva un histórico de 7 días.
