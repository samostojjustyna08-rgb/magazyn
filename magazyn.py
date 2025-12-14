import streamlit as st
import pandas as pd
import os

# Konfiguracja strony
st.set_page_config(page_title="Magazyn", page_icon="🦆")

# --- CSS: TŁO W KACZKI ---
st.markdown(
    """
    <style>
    .stApp {
        /* Kolor tła: Jasny błękit (jak woda dla kaczek) */
        background-color: #E0F7FA;
        
        /* Wzorek w kaczki (używamy emoji kaczki jako SVG) */
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80' viewBox='0 0 100 100'%3E%3Ctext y='50%25' x='50%25' dy='.3em' text-anchor='middle' font-size='50'%3E🦆%3C/text%3E%3C/svg%3E");
        
        /* Rozmiar powtarzania */
        background-size: 80px 80px;
    }
    
    /* Białe, półprzezroczyste tło pod elementami, żeby tekst był czytelny */
    .stDataFrame, .stForm, div[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 15px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- TYTUŁ ---
st.title("Magazyn")

# Nazwa pliku z danymi
DATA_FILE = "magazyn.csv"

# --- KROK 1: Wczytanie danych ---
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Produkt", "Ilość"])

# --- KROK 2: Panel boczny (Dodawanie) ---
st.sidebar.header("Dodaj nowy towar")
with st.sidebar.form("add_form", clear_on_submit=True):
    new_product = st.text_input("Nazwa produktu")
    new_qty = st.number_input("Ilość", min_value=1, step=1)
    submit_add = st.form_submit_button("Zapisz w pliku")

    if submit_add and new_product:
        new_row = pd.DataFrame({"Produkt": [new_product], "Ilość": [new_qty]})
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.sidebar.success("Kaczka dodała towar! 🦆")
        st.rerun()

# --- KROK 3: Wyświetlanie danych ---
st.subheader("Stan magazynowy")

if not df.empty:
    st.dataframe(df, use_container_width=True)

    # --- KROK 4: Usuwanie ---
    st.divider()
    st.subheader("Usuwanie towaru")
    
    product_to_remove = st.selectbox("Wybierz produkt do usunięcia", df["Produkt"].unique())
    
    if st.button("Usuń wybrany produkt"):
        df = df[df["Produkt"] != product_to_remove]
        df.to_csv(DATA_FILE, index=False)
        st.success(f"Usunięto {product_to_remove}")
        st.rerun()
else:
    st.info("Magazyn jest pusty. Użyj panelu bocznego, aby dodać towary.")
