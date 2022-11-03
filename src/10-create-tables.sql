CREATE TABLE "sensor" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar,
  "type" varchar,
  "location_id" int,
  "installation_date" date
);

CREATE TABLE "measurement" (
  "id" SERIAL PRIMARY KEY,
  "value" float8,
  "unit" varchar,
  "sensor_id" int
  "timestmp" timestamp
);

CREATE TABLE "location" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar,
  "description" varchar,
  "x" float8,
  "y" float8,
  "z" float8
);

ALTER TABLE "measurement" ADD FOREIGN KEY ("sensor_id") REFERENCES "sensor" ("id");

ALTER TABLE "sensor" ADD FOREIGN KEY ("location_id") REFERENCES "location" ("id");
