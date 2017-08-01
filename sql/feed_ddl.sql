DROP TABLE IF EXISTS trips;
CREATE TABLE trips
(
  route_id        BIGINT,
  service_id      BIGINT,
  trip_id         TEXT,
  trip_headsign   TEXT,
  trip_short_name BIGINT,
  direction_id    DOUBLE PRECISION,
  block_id        BIGINT,
  shape_id        DOUBLE PRECISION,
  trip_type       BIGINT
);
DROP TABLE IF EXISTS stop_times;
CREATE TABLE stop_times
(
  trip_id             TEXT,
  arrival_time        TEXT,
  departure_time      TEXT,
  stop_id             BIGINT,
  stop_sequence       BIGINT,
  stop_headsign       DOUBLE PRECISION,
  pickup_type         BIGINT,
  drop_off_type       BIGINT,
  shape_dist_traveled DOUBLE PRECISION
);
DROP TABLE IF EXISTS stop_time_overrides;
CREATE TABLE stop_time_overrides
(
  trip_id       TEXT,
  stop_sequence BIGINT,
  service_id    BIGINT,
  stop_id       TEXT
);

DROP TABLE IF EXISTS stops;
CREATE TABLE stops
(
  stop_id        TEXT,
  stop_code      DOUBLE PRECISION,
  stop_name      TEXT,
  stop_desc      DOUBLE PRECISION,
  stop_lat       DOUBLE PRECISION,
  stop_lon       DOUBLE PRECISION,
  zone_id        DOUBLE PRECISION,
  stop_url       DOUBLE PRECISION,
  location_type  BIGINT,
  parent_station TEXT,
  platform_code  TEXT
);

DROP TABLE IF EXISTS routes;
CREATE TABLE routes
(
  route_id         BIGINT,
  agency_id        TEXT,
  route_short_name TEXT,
  route_long_name  TEXT,
  route_desc       DOUBLE PRECISION,
  route_type       BIGINT,
  route_url        DOUBLE PRECISION,
  route_color      DOUBLE PRECISION,
  route_text_color DOUBLE PRECISION
);

DROP TABLE IF EXISTS agency;
CREATE TABLE agency
(
  agency_id       TEXT,
  agency_name     TEXT,
  agency_url      TEXT,
  agency_timezone TEXT,
  agency_lang     TEXT,
  agency_phone    DOUBLE PRECISION
);

DROP TABLE IF EXISTS transfers;
CREATE TABLE transfers
(
  from_stop_id      BIGINT,
  to_stop_id        BIGINT,
  transfer_type     BIGINT,
  min_transfer_time BIGINT,
  from_trip_id      DOUBLE PRECISION,
  to_trip_id        DOUBLE PRECISION
);

DROP TABLE IF EXISTS calendar;
CREATE TABLE calendar
(
  service_id BIGINT,
  monday     BIGINT,
  tuesday    BIGINT,
  wednesday  BIGINT,
  thursday   BIGINT,
  friday     BIGINT,
  saturday   BIGINT,
  sunday     BIGINT,
  start_date BIGINT,
  end_date   BIGINT
);

DROP TABLE IF EXISTS calendar_dates;
CREATE TABLE calendar_dates
(
  service_id     BIGINT,
  date           TIMESTAMP,
  exception_type BIGINT
);

DROP TABLE IF EXISTS translations;
CREATE TABLE translations
(
  trans_id    TEXT,
  lang        TEXT,
  translation TEXT
);
