import os
import requests
import datetime as dt
from dateutil.relativedelta import relativedelta
from sqlalchemy import create_engine, text

# ---------------- CONFIGURACIÓN ---------------- #

# Conexión a la base de datos (valores de docker-compose.yml)
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "weatherdb")
DB_USER = os.getenv("DB_USER", "weather")
DB_PASS = os.getenv("DB_PASS", "weatherpass")

# Coordenadas de Villaviciosa de Odón
LAT, LON = 40.357, -3.904

# Variables que queremos de Open-Meteo
VARIABLES_DIARIAS = [
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "weathercode"
]

# ---------------- FUNCIONES ---------------- #

def obtener_motor_bd():
    """Crea la conexión (engine) a MariaDB usando SQLAlchemy."""
    url = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url, pool_pre_ping=True)

def calcular_rango_ultimos7():
    """Devuelve las fechas desde hoy-7 hasta hoy-1 (excluye hoy)."""
    hoy = dt.date.today()
    inicio = hoy - relativedelta(days=7)
    fin = hoy - relativedelta(days=1)
    return inicio, fin

def pedir_datos_openmeteo(inicio, fin):
    """Llama a la API de Open-Meteo y devuelve la respuesta JSON."""
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}&longitude={LON}"
        f"&start_date={inicio}&end_date={fin}"
        f"&daily={','.join(VARIABLES_DIARIAS)}"
        f"&timezone=auto"
    )
    respuesta = requests.get(url, timeout=30)
    respuesta.raise_for_status()
    return respuesta.json()

def transformar_respuesta(datos):
    """Convierte el JSON de Open-Meteo en filas con el formato de nuestra tabla."""
    diario = datos["daily"]
    filas = []
    for i, fecha in enumerate(diario["time"]):
        filas.append({
            "fecha": fecha,
            "tmax_c": diario["temperature_2m_max"][i],
            "tmin_c": diario["temperature_2m_min"][i],
            "lluvia_mm": diario["precipitation_sum"][i],
            "weather_code": diario["weathercode"][i],
        })
    return filas

def insertar_filas(motor, filas):
    """Inserta o actualiza filas en la tabla info_meteorologica."""
    sql = """
    INSERT INTO info_meteorologica (fecha, tmax_c, tmin_c, lluvia_mm, weather_code)
    VALUES (:fecha, :tmax_c, :tmin_c, :lluvia_mm, :weather_code)
    ON DUPLICATE KEY UPDATE
      tmax_c=VALUES(tmax_c),
      tmin_c=VALUES(tmin_c),
      lluvia_mm=VALUES(lluvia_mm),
      weather_code=VALUES(weather_code);
    """
    with motor.begin() as conn:
        for fila in filas:
            conn.execute(text(sql), fila)

# ---------------- PROGRAMA PRINCIPAL ---------------- #

def main():
    print("🔗 Conectando a la base de datos...")
    print(f"   Host: {DB_HOST}, Puerto: {DB_PORT}, DB: {DB_NAME}")

    try:
        motor = obtener_motor_bd()
        with motor.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Conexión a la base de datos OK")
    except Exception as e:
        print("❌ Error al conectar a la base de datos:", e)
        return

    inicio, fin = calcular_rango_ultimos7()
    print(f"📅 Fechas pedidas a la API: {inicio} → {fin}")

    try:
        datos = pedir_datos_openmeteo(inicio.isoformat(), fin.isoformat())
        print("🌐 API respondió correctamente")
        print(str(datos)[:200])  # mostramos los primeros 200 chars del JSON
    except Exception as e:
        print("❌ Error al llamar a la API:", e)
        return

    filas = transformar_respuesta(datos)
    print(f"📊 Filas a insertar: {len(filas)}")

    try:
        insertar_filas(motor, filas)
        print(f"✅ Se insertaron/actualizaron {len(filas)} filas en la tabla info_meteorologica")
    except Exception as e:
        print("❌ Error al insertar filas en la base de datos:", e)

# ---------------- EJECUCIÓN ---------------- #

if __name__ == "__main__":
    main()
