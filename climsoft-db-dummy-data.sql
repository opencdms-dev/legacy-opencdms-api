CREATE DATABASE IF NOT EXISTS `mariadb_climsoft_test_db_v4` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `mariadb_climsoft_test_db_v4`;

TRUNCATE stationelement;

INSERT INTO stationelement
    (recordedFrom, describedBy, beginDate)
    SELECT t.recordedFrom, t.describedBy, MIN(t.beginDate) as beginDate FROM(
        SELECT recordedFrom, describedBy, DATE(obsDatetime) as beginDate
        FROM observationfinal
    ) t GROUP BY t.recordedFrom, t.describedBy;

TRUNCATE stationlocationhistory;

INSERT INTO stationlocationhistory
    (belongsTo, openingDatetime, stationType, geoLocationMethod, geoLocationAccuracy, closingDatetime, latitude, longitude, elevation, authority, adminRegion, drainageBasin)
VALUES
    ("67774010","1897-04-01 06:00:00","landFixed","GPS","4","1897-05-01 06:00:00","-17.830000","31.030000","1471","MSD","Harare Province","Manyame River Basin"),
    ("67774010","1897-05-01 06:00:00","landFixed","GPS","4","1897-06-01 06:00:00","-17.830000","31.040000","1471","MSD","Harare Province","Manyame River Basin"),
    ("67774010","1897-06-01 06:00:00","landFixed","GPS","4","1897-07-01 06:00:00","-17.830000","31.050000","1471","MSD","Harare Province","Manyame River Basin")
;


INSERT INTO instrument
    (instrumentName, instrumentId, serialNumber, abbreviation, model, manufacturer, instrumentUncertainty, installationDatetime, deinstallationDatetime, height, instrumentPicture, installedAt)
VALUES
    ("TEST INSTRUMENT 1", "1", "0FHA421", "TI1", "X1001", "TEST MANUFACTURER 1", 0.01, "1897-04-01 06:00:00", NULL, 101, NULL, "67774010"),
    ("TEST INSTRUMENT 2", "2", "0FHA422", "TI2", "X1002", "TEST MANUFACTURER 2", 0.02, "1897-04-02 06:00:00", NULL, 102, NULL, "67774010"),
    ("TEST INSTRUMENT 3", "3", "0FHA423", "TI3", "X1003", "TEST MANUFACTURER 3", 0.03, "1897-04-03 06:00:00", NULL, 103, NULL, "67774010")
;
