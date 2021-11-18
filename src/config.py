import os

app_config = {
    "APP_SECRET": os.getenv(
        "APP_SECRET",
        "MGExYmQ4ZDRiNjQ5NGE1YzkxMDFmM2IxMTcxMTYyNjMxOTA5MGQxZGVmYzI0Njk3OWRlNWYyYjZmY2YxNDQ0Y2NiNGYzYzY0ZTg0NjQ0NjU4NzQ4YmJkYTVkZjQzMWI3"
    ),
    "CLIMSOFT_DB_URI": os.getenv(
        "CLIMSOFT_DB_URI",
        "mysql+mysqldb://root:password@127.0.0.1:13306/climsoft"
    ),
    "AUTH_DB_URI": os.getenv(
        "AUTH_DB_URI",
        "postgresql+psycopg2://postgres:password@localhost:15432/auth"
    )
}
