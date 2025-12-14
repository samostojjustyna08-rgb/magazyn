import streamlit as st
import pandas as pd
import os

# Konfiguracja strony
st.set_page_config(page_title="Magazyn (Bez Sesji)", page_icon="📦")
st.title("📦 Prosty Magazyn (Bez Session State)")

# Nazwa pliku z danymi
DATA_FILE = "magazyn.csv"

# --- KROK 1: Wczytanie danych na starcie skryptu ---
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    # Utworzenie pustego DataFrame jeśli plik nie istnieje
    df = pd.DataFrame(columns=["Produkt", "Ilość"])

# --- KROK 2: Sekcja Dodawania (Panel Boczny) ---
st.sidebar.header("Dodaj nowy towar")
with st.sidebar.form("add_form", clear_on_submit=True):
    new_product = st.text_input("Nazwa produktu")
    new_qty = st.number_input("Ilość", min_value=1, step=1)
    submit_add = st.form_submit_button("Zapisz w pliku")

    if submit_add and new_product:
        # Tworzymy nowy rekord
        new_row = pd.DataFrame({"Produkt": [new_product], "Ilość": [new_qty]})
        # Dołączamy do obecnych danych
        df = pd.concat([df, new_row], ignore_index=True)
        # Zapisujemy NATYCHMIAST do pliku
        df.to_csv(DATA_FILE, index=False)
        st.sidebar.success("Dodano i zapisano!")
        # Wymuszamy odświeżenie strony, aby tabela główna zobaczyła zmiany
        st.rerun()

# --- KROK 3: Wyświetlanie danych ---
st.subheader("Stan magazynowy")

if not df.empty:
    st.dataframe(df, use_container_width=True)

    # --- KROK 4: Sekcja Usuwania ---
    st.divider()
    st.subheader("Usuwanie towaru")
    
    # Lista rozwijana z produktami dostępnymi w pliku
    product_to_remove = st.selectbox("Wybierz produkt do usunięcia", df["Produkt"].unique())
    
    if st.button("Usuń wybrany produkt"):
        # Filtrujemy dane (usuwamy wybrany wiersz)
        df = df[df["Produkt"] != product_to_remove]
        # Zapisujemy zmiany do pliku
        df.to_csv(DATA_FILE, index=False)
        st.success(f"Usunięto {product_to_remove}")
        # Wymuszamy odświeżenie strony
        st.rerun()
else:
    st.info("Magazyn jest pusty. Użyj panelu bocznego, aby dodać towary.")
