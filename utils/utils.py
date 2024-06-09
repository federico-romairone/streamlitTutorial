import streamlit as st
from sqlalchemy import create_engine,text

"""Raccoglie le principali funzioni condivise dalle varie pagine"""

def connect_db(dialect, username, password, host, dbname):
    """
    Crea un connessione al db.
    
    :param dialect: specifico modo di comunicare del db
    :return: False se ci sono eccezioni, connessione al db altrimenti
    """
    try:
        # engine (motore) = punto di collegamento tra app e database
        engine = create_engine(f'{dialect}://{username}:{password}@{host}/{dbname}')
        conn = engine.connect()
        return conn
    except:
        return False
    
def check_connection():
    """
    Crea un button e verifica che sia stata richiesta una connessione al db tramite onclick event.
    Mosta un messaggio di successo o insuccesso a seconda dell'esito della connessione.

    :return: True per connessione con successo, False altrimenti
    """
    # inizializzo variabile per connessione
    if "connection" not in st.session_state.keys():
        st.session_state["connection"] = False
    
    # creo il bottone e verifico se sia stato cliccato
    if st.sidebar.button("Connetti al database"):
        myconnection = connect_db("mysql+pymysql", "student", "user_pwd", "localhost", "classicmodels")
        if myconnection is not False:
            st.session_state["connection"] = myconnection
        else:
            st.session_state["connection"]=False
            st.sidebar.error("Errore nella connessione al DB")
    
        # se connessione creata, messaggio di successo, altrimenti fallimento
        if st.session_state["connection"]:
            st.sidebar.success("Connesso al DB")
            return True

def execute_query(conn, query):
    """
    Esegue una query sul database connesso.
    """
    return conn.execute(text(query))

def compact_form(num):
    """
    Restituisce un numero dato in forma compatta.
    """
    num = float(num)
    if abs(num) >= 1e9:
        return "%.2fB" % (num / 1e9)
    elif abs(num) >= 1e6:
        return "%.2fM" % (num / 1e6)
    elif abs(num) >= 1e3:
        return "%.2fK" % (num / 1e3)
    else:
        return "%.2f" % num
