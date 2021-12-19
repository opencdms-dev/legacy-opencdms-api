FROM opencdms/mysql:5.1.73
COPY create_mch_english_basic_tables.sql /scripts/create_mch_english_basic_tables.sql
COPY migrate.sh /scripts/migrate.sh

ENTRYPOINT ["bash", "/scripts/migrate.sh"]
