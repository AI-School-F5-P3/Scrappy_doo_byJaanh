# ProjectScrappy_doo

## Descripción

Este proyecto de scraping extrae frases, autores y tags de `http://quotes.toscrape.com` utilizando Scrapy y organiza los datos para su posterior análisis.

## Estructura del Proyecto

'''
ProjectScrappy_doo/
├── README.md
├── requirements.txt
├── .gitignore
├── setup.py
├── config/
│   └── config.yaml
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   ├── presentation.pdf
│   └── architecture.md
├── logs/
│   └── scraping.log
├── notebooks/
│   └── data_analysis.ipynb
├── scripts/
│   ├── scrape_quotes.py
│   ├── process_data.py
│   ├── update_db.py
│   └── visualize_data.py
├── src/
│   ├── __init__.py
│   ├── config/
│   │   └── config_loader.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── data_cleaning.py
│   ├── scraping/
│   │   ├── __init__.py
│   │   ├── scraper.py
│   │   ├── parser.py
│   │   └── utils.py
│   └── visualization/
│       ├── __init__.py
│       └── dashboard.py
├── tests/
│   ├── test_scraper.py
│   ├── test_data_processing.py
│   └── test_database.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
└── webapp/
    ├── templates/
    │   └── index.html
    ├── static/
    │   ├── css/
    │   └── js/
    └── app.py
└── venv/
'''
