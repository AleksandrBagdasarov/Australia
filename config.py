import random

DB_CONNECTION_URL = 'postgresql+psycopg2://User:asfuasfo1adp8am@postgresdb1.accelerator-introlab.ml:5432/news'



proxies = (
    '134.209.69.183',
    '149.56.1.48',
    '198.50.177.44',
    '165.227.35.11',
    '70.35.213.226',
    '152.26.66.140',
    '168.169.146.12',
    '64.235.204.107',
    '205.202.38.126',
    '100.20.170.195',
    '67.207.83.225',
    '168.169.96.2',
    '173.236.176.60',
    '199.119.74.245',
    '50.205.119.150',
    '54.39.184.122',
)

DEFAULT_PROXIES = {'http': '149.56.1.48'}

RANDOM_PROXIES = lambda: {'http': random.choice(proxies)}