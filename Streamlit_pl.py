import streamlit as st
from sshtunnel import SSHTunnelForwarder
import mysql.connector
from mysql.connector import MySQLConnection
import socket
import time
import mariadb

# Konfiguraatiot
SSH_HOST = st.secrets["SSH_HOST"]
SSH_PORT = 22
SSH_USER = st.secrets["SSH_USER"]
SSH_PASSWORD = st.secrets["SSH_PASSWORD"]

MYSQL_HOST = st.secrets["MYSQL_HOST"]
MYSQL_PORT = 3306
MYSQL_USER = st.secrets["MYSQL_USER"]
MYSQL_PASSWORD = st.secrets["MYSQL_PASSWORD"]
MYSQL_DATABASE = st.secrets["MYSQL_DATABASE"]


# connection parameters
conn_params= {
    "user" : st.secrets["MYSQL_USER"],
    "password" : st.secrets["MYSQL_PASSWORD"],
    "host" : "127.0.1.1",
    "database" : st.secrets["MYSQL_DATABASE"],
    "port" : 3307,
    "connect_timeout" : 60,  # Yhteyden aikakatkaisu (sekunteina)
    "read_timeout" : 30,     # Lukemisen aikakatkaisu
    "write_timeout" : 30     # Kirjoittamisen aikakatkaisu
}


@st.cache_resource
def create_connection():
    # Avaa SSH-tunneli
    st.title("Avataan SSH-tunneli...")
    tunnel = SSHTunnelForwarder(
        (SSH_HOST, SSH_PORT),
        ssh_username=SSH_USER,
        ssh_password=SSH_PASSWORD,
        remote_bind_address=(MYSQL_HOST, MYSQL_PORT),
        local_bind_address=("127.0.1.1", 3307),
        set_keepalive=1  # Lähetä keepalive-paketteja 30 sekunnin välein

    )
    tunnel.start()
    #time.sleep(1)

    

    #st.title("Avataan SQL...")
    # Luo MySQL-yhteys
    #connection = st.connection('mysql', type='sql')

    # Establish a connection
    
    connection= mariadb.connect(**conn_params)
            
    

    # connection = MySQLConnection(
    #     host="127.0.0.1",
    #     port=3307,
    #     user=MYSQL_USER,
    #     password=MYSQL_PASSWORD,
    #     database=MYSQL_DATABASE
    # )
    connection.auto_reconnect = True

    cursor = connection.cursor()
    cursor.execute("SELECT TotalKg FROM powerlifting LIMIT 100;")
    rows = cursor.fetchall()

    for row in rows:
        st.write(row)

    # # Sulje yhteydet
    cursor.close()
    connection.close()
    tunnel.stop()

    return connection, tunnel

def main():
    st.title("SQL-tietokantayhteys Streamlit-sovelluksessa")

    #try:
    # Luo yhteys SQL-palvelimeen
    connection, tunnel = create_connection()

    st.title("Query data from SQL database")
    # Tee SQL-kysely
    
    # cursor = connection.cursor()
    # cursor.execute("SELECT * FROM powerlifting LIMIT 10;")
    # rows = cursor.fetchall()
    

    # Perform query.
    #df = connection.query('SELECT * from powerlifting LIMIT 20;', return_pandas=True)

    # Print results.
    # for row in df.itertuples():
    #     st.write(f"{row.name} has a :{row.pet}:")

    # Näytä tulokset Streamlitissä
    # st.write("Tietokannan data:")
    # for row in rows:
    #     st.write(row)

    # # # Sulje yhteydet
    # cursor.close()
    # connection.close()
    # tunnel.stop()

    # except Exception as e:
    #     st.error(f"Virhe: {e}")

if __name__ == "__main__":
    main()
