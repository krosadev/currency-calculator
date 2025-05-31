
# Currency Converter App (NBP API)
Simple web application built with Streamlit that allows users to convert between Polish Zloty (PLN) and major foreign currencies using live exchange rates from the National Bank of Poland (NBP). The app also provides an interactive chart showing recent exchange rate trends.


## Features

- Convert between PLN and selected currency or vice versa
- Supports all currencies from NBP's official exchange rate table
- Interactive chart (7, 14, 30, or 90 days) of exchange rate history using [plotly](https://github.com/plotly/plotly.py)
- Live data from [api.nbp.pl](http://api.nbp.pl)
- Lightweight, browser-based interface with [Streamlit](https://github.com/streamlit/streamlit)


## Requirements

To run locally, install the required packages:

```bash
  pip install streamlit requests plotly
```


## How to Run Locally

Clone the project:

```bash
  git clone https://github.com/krosadev/currency-calculator.git
  cd currency-calculator
```

Run the app:

```bash
  streamlit run calculator-streamlit.py
```


## Live Demo

Check out the live version of the application: [Demo](https://currency-calculator-kzfzenijvvuqup5pjd4bdu.streamlit.app/)

