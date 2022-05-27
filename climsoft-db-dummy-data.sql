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


INSERT INTO form_daily2
    (stationId, elementId, yyyy, mm, hh, day01, day02, day03, day04, day05, day06, day07, day08, day09, day10, day11, day12, day13, day14, day15, day16, day17, day18, day19, day20, day21, day22, day23, day24, day25, day26, day27, day28, day29, day30, day31, flag01, flag02, flag03, flag04, flag05, flag06, flag07, flag08, flag09, flag10, flag11, flag12, flag13, flag14, flag15, flag16, flag17, flag18, flag19, flag20, flag21, flag22, flag23, flag24, flag25, flag26, flag27, flag28, flag29, flag30, flag31, period01, period02, period03, period04, period05, period06, period07, period08, period09, period10, period11, period12, period13, period14, period15, period16, period17, period18, period19, period20, period21, period22, period23, period24, period25, period26, period27, period28, period29, period30, period31, total, signature, entryDatetime, temperatureUnits, precipUnits, cloudHeightUnits, visUnits)
VALUES
    ("67774010", 2, 2022, 5, 6, NULL, "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "M", "T", "E", "G", "D", "", NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "930", "VALID", "2000-01-01 00:00:00", "DEGREE CELCIUS", "MILIMETER", "KILOMETERS", "DEGREE"),
    ("67774010", 2, 2022, 4, 6, NULL, "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "M", "T", "E", "G", "D", "", NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "930", "VALID", "2000-01-02 00:00:00", "DEGREE CELCIUS", "MILIMETER", "KILOMETERS", "DEGREE"),
    ("67774010", 2, 2022, 3, 6, "", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "M", "T", "E", "G", "D", "", NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "930", "VALID", "2000-01-03 00:00:00", "DEGREE CELCIUS", "MILIMETER", "KILOMETERS", "DEGREE"),
    ("67774010", 3, 2022, 5, 6, "", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "M", "T", "E", "G", "D", "", NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "930", "VALID", "2000-01-04 00:00:00", "DEGREE CELCIUS", "MILIMETER", "KILOMETERS", "DEGREE"),
    ("67774010", 3, 2022, 4, 6, NULL, "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "30", "M", "T", "E", "G", "D", "", NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "FIRST", "930", "VALID", "2000-01-05 00:00:00", "DEGREE CELCIUS", "MILIMETER", "KILOMETERS", "DEGREE")
;
