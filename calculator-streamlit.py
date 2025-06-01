import streamlit as st
import requests
import plotly.express as px
from datetime import datetime, timedelta

# --- Funkcje pomocnicze ---

# Pobieranie listy dostępnych walut z tabeli A NBP
@st.cache_data
def pobierz_dostepne_waluty():
    url = "http://api.nbp.pl/api/exchangerates/tables/A/?format=json"
    response = requests.get(url)
    if response.status_code == 200:
        dane = response.json()
        # Umieszczenie popularnych walut na górze listy
        wszystkie = [entry['code'] for entry in dane[0]['rates']]
        popularne = ['EUR', 'USD', 'GBP', 'CHF']
        reszta = sorted([w for w in wszystkie if w not in popularne])
        return popularne + reszta
    # W przypadku błędu zwracanie domyślnej listy    
    return ['EUR', 'USD', 'GBP', 'CHF']

# Pobieranie bieżącego kursu wybranej waluty względem PLN
def pobierz_kurs(waluta):
    url = f"http://api.nbp.pl/api/exchangerates/rates/A/{waluta}/?format=json"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()['rates'][0]['mid']
    return None

# Pobieranie danych historycznych kursu waluty
def pobierz_kursy_historyczne(waluta, dni):
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=dni)).strftime("%Y-%m-%d")
    url = f"http://api.nbp.pl/api/exchangerates/rates/A/{waluta}/{start_date}/{end_date}/?format=json"
    r = requests.get(url)
    if r.status_code == 200:
        dane = r.json()['rates']
        daty = [d['effectiveDate'] for d in dane]
        kursy = [d['mid'] for d in dane]
        return daty, kursy
    return [], []

# --- Interfejs Streamlit ---

# Ustawienia strony
st.set_page_config(page_title="Kalkulator Walutowy", layout="centered")
st.title("Kalkulator Walutowy")

# Wybór waluty z listy
waluty = pobierz_dostepne_waluty()
kod_waluty = st.selectbox("Wybierz walutę:", waluty)

# Wybór kierunku konwersji
kierunek = st.radio("Kierunek konwersji:", ["PLN ➝ Waluta", "Waluta ➝ PLN"])

# Wprowadzenie kwoty
kwota = st.number_input("Wpisz kwotę:", min_value=0.01, value=100.0)

# Pobranie kursu i obliczenie wyniku
kurs = pobierz_kurs(kod_waluty)
if kurs:
    if kierunek == "PLN ➝ Waluta":
        wynik = kwota / kurs
        st.success(f"{kwota:.2f} PLN = {wynik:.2f} {kod_waluty} (kurs: {kurs:.2f})")
    else:
        wynik = kwota * kurs
        st.success(f"{kwota:.2f} {kod_waluty} = {wynik:.2f} PLN (kurs: {kurs:.2f})")
else:
    st.error("Nie udało się pobrać kursu.")

# --- Wykres ---

# Wybór przedziału czasu
okres_map = {"7 dni": 7, "14 dni": 14, "30 dni": 30, "90 dni": 90}
okres_wybor = st.selectbox("Wybierz okres do wykresu:", list(okres_map.keys()))
dni = okres_map[okres_wybor]

# Przycisk wywołujący wykres
if st.button("Pokaż wykres kursu"):
    daty, kursy = pobierz_kursy_historyczne(kod_waluty, dni)
    if daty:
        # Tworzenie wykresu liniowego przy użyciu Plotly
        fig = px.line(
            x=daty,
            y=kursy,
            labels={'x': 'Data', 'y': f'Kurs {kod_waluty} w PLN'},
            title=f"Kurs {kod_waluty} z ostatnich {dni} dni"
        )
        fig.update_traces(mode='lines+markers')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Nie udało się pobrać danych historycznych.")
