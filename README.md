# Proyecto Scrappy Doo

Proyecto Scrappy Doo es un proyecto de web scraping desarrollado para extraer citas e información de autores del sitio web "http://quotes.toscrape.com". 

Este repositorio contiene el código de scraping, scripts de procesamiento de datos y un frontend básico para mostrar los datos recopilados.

## Tabla de Contenidos

1. [Estructura del Proyecto](#estructura-del-proyecto)
2. [Instalación](#instalación)
3. [Uso](#uso)
4. [Características](#características)
5. [Contribución](#contribución)
6. [Licencia](#licencia)

## Estructura del Proyecto

```plaintext
ProjectScrappy_doo/
├── data/
│   ├── raw/
│   │   ├── authors.json
│   │   ├── quotes.json
│   └── processed/
│       ├── cleaned_authors.json
│       ├── cleaned_quotes.json
├── frontend/
│   ├── css/
│   │   ├── style.css
│   ├── img/
│   ├── js/
│   └── index.html
├── logs/
│   ├── authors_scraper.log
│   ├── quotes_scraper.log
│   └── scraping.log
├── scripts/
│   ├── process_data.py
│   └── run_spider.py
├── src/
│   ├── pipelines/
│   │   └── jsonwriter_pipeline.py
│   ├── scraping/
│   │   ├── authors_scraper.py
│   │   └── quotes_scraper.py
├── venv/
├── requirements.txt
└── README.md
