import streamlit as st
from utils.utils import *
import pandas as pd

# ogni tab ha una funzione separata

def create_tab_prodotti(tab_prodotti):
    col1, col2, col3 = tab_prodotti.columns(3)
    
    # eseguo query richiesta e salvo l'oggetto risultante
    query = """
            SELECT SUM(amount) as TotalAmount, MAX(amount) as MaxAmount, AVG(amount) as AVGAmount 
            FROM payments;
            """
    payment_info = execute_query(st.session_state["connection"], query)
    
    # []   --> creo lista 
    # dict --> di dizionari 
    # zip  --> di coppie (nome attributo, valore) del risultato della query
    payment_info_dict = [dict(zip(payment_info.keys(), result)) for result in payment_info]

    # metriche dei prodotti
    col1.metric("Importo totale: ", f'$ {compact_form(payment_info_dict[0]["TotalAmount"])}')
    col2.metric("Importo massimo: ", f'$ {compact_form(payment_info_dict[0]["MaxAmount"])}')
    col3.metric("Importo medio: ", f'$ {compact_form(payment_info_dict[0]["AVGAmount"])}')

    # panoramica dei prodotti
    with tab_prodotti.expander("Panoramica prodotti", True):
        query_base = """
                     SELECT productCode as code, productName as name, quantityInStock as quantity, buyPrice as price, MSRP
                     FROM products
                     """
        # gestione input utente
        prod_col1, prod_col2 = st.columns([3, 3])
        sort_param = prod_col1.radio("Ordina per: ", ["code", "name", "quantity", "price"])
        sort_choice = prod_col2.selectbox("Ordine: ", ["crescente", "decrescente"])
        sort_dict = {
            "crescente": "ASC", 
            "descrescente":"DESC"
        }
        query = "%s ORDER BY %s %s" % (query_base, sort_param, sort_dict[sort_choice])
        # salvo risultato query
        products = execute_query(st.session_state["connection"], query)
        # salvo una tabella interattiva pandas
        products_df = pd.DataFrame(products)
        # creo un dataframe stramlit
        st.dataframe(products_df, use_container_width = True)

if __name__ == "__main__":
    st.title("📈 Analisi")

    # creazione dei tab distinti
    tab_prodotti,tab_staff,tab_clienti=st.tabs(["Prodotti","Staff","Clienti"])
    
    # connessione
    if check_connection():
        create_tab_prodotti(tab_prodotti)