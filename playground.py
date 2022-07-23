from sqlalchemy import create_engine
from sqlalchemy import text as sa_text
from sqlalchemy.orm import sessionmaker, Session

if __name__ == "__main__":
    climsoft_engine = create_engine("mysql+mysqldb://root:password@127.0.0.1:23306/mariadb_climsoft_test_db_v4")
    ClimsoftSessionLocal = sessionmaker(climsoft_engine)
    session: Session = ClimsoftSessionLocal()
    username = "root"
    password = "password"
    user = session.execute(sa_text(f'''
        SELECT * 
        FROM mysql.user 
        WHERE User="{username}" AND Password=password("{password}")
    '''))

    print(user.all())
