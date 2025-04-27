import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class EDGAR_visualization:
    def __init__(self):
        pass
    def lineplot(self, df):
        sns.lineplot(
        data = df,
        x = 'Year',
        y = 'Emission (MtCO2eq/yr)',
        hue = 'Country'
        )