import streamlit as st
from sshtunnel import SSHTunnelForwarder
import mysql.connector

# Konfiguraatiot
SSH_HOST = "staff.oamk.fi"
SSH_PORT = 22
SSH_USER = "villemaj"
SSH_PASSWORD = "M3r1h3lm1D4n13l"  # Vaihda salasanaan tai käytä ssh-avainta

MYSQL_HOST = "mysli.oamk.fi"
MYSQL_PORT = 3306
MYSQL_USER = "villemaj"
MYSQL_PASSWORD = "hZUELZdD8Zg5pWTx"
MYSQL_DATABASE = "opisk_villemaj"

# Funktio SQL-yhteyden luomiseksi SSH-tunnelin kautta
@st.cache_resource
def create_connection():
    # Avaa SSH-tunneli
    tunnel = SSHTunnelForwarder(
        (SSH_HOST, SSH_PORT),
        ssh_username=SSH_USER,
        ssh_password=SSH_PASSWORD,
        remote_bind_address=(MYSQL_HOST, MYSQL_PORT),
        local_bind_address=("127.0.0.1", 3307)
    )
    tunnel.start()

    # Luo MySQL-yhteys
    connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3307,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

    return connection, tunnel

# Streamlit-sovelluksen logiikka
def main():
    st.title("SQL-tietokantayhteys Streamlit-sovelluksessa")

    try:
        # Luo yhteys SQL-palvelimeen
        connection, tunnel = create_connection()
        cursor = connection.cursor()

        # Tee SQL-kysely
        cursor.execute("SELECT * FROM powerlifting LIMIT 10;")
        rows = cursor.fetchall()

        # Näytä tulokset Streamlitissä
        st.write("Tietokannan data:")
        for row in rows:
            st.write(row)

        # Sulje yhteydet
        cursor.close()
        connection.close()
        tunnel.stop()

    except Exception as e:
        st.error(f"Virhe: {e}")

if __name__ == "__main__":
    main()
