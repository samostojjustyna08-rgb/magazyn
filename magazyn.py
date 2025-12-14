import streamlit as st
import pandas as pd
import os

# Konfiguracja strony
st.set_page_config(page_title="Magazyn", page_icon="📦")

# --- CSS: TŁO I STYL ---
# Tutaj dzieje się magia z tłem. Używamy SVG (grafiki wektorowej) w kodzie,
# aby narysować serduszka bez zewnętrznych plików.
st.markdown(
    """
    <style>
    .stApp {
        /* Kolor tła: Jasny fiolet (Lavender) */
        background-color: #E6E6FA;
        
        /* Wzorek w serduszka (zakodowany obrazek SVG) */
        background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z' fill='%23FF69B4' fill-opacity='0.4'/%3E%3C/svg%3E");
        
        /* Rozmiar i powtarzanie wzorka */
        background-size: 60px 60px;
    }
    
    /* Opcjonalnie: Białe tło pod tabelką, żeby była czytelna na tle serduszek */
    .stDataFrame, .stForm {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 10px;
        border-radius: 10px;
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
        st.sidebar.success("Dodano!")
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
