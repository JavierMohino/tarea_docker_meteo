CREATE DATABASE IF NOT EXISTS weatherdb;
USE weatherdb;

CREATE TABLE IF NOT EXISTS info_meteorologica (
  id INT AUTO_INCREMENT PRIMARY KEY,
  fecha DATE NOT NULL,
  tmax_c DECIMAL(5,2) NOT NULL,
  tmin_c DECIMAL(5,2) NOT NULL,
  lluvia_mm DECIMAL(6,2) NOT NULL,
  weather_code INT NOT NULL,
  UNIQUE KEY uq_fecha (fecha)
);
