from setuptools import setup, find_packages

setup(
    name='ProjectScrappy_doo',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'scrapy',
    ],
    entry_points={
        'console_scripts': [
            'scrape-quotes=scripts.scrape_quotes:run_spider',
        ],
    },
)
