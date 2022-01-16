FROM mariadb:latest

COPY create_mch_english_basic_tables.sql /docker-entrypoint-initdb.d/1.sql
