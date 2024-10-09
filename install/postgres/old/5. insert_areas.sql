COPY area (areaid, name, description)
FROM './areas.csv'
DELIMITER ','
CSV HEADER;