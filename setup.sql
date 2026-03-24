CREATE DATABASE environment;
\c environment;
CREATE EXTENSION postgis;
CREATE TABLE IF NOT EXISTS enviroreadings(
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    altitude FLOAT,
    temperature FLOAT,
    humidity FLOAT,
    pressure FLOAT,
    nh3 FLOAT,
    PM1 FLOAT,
    PM25 FLOAT,
    PM10 FLOAT
);