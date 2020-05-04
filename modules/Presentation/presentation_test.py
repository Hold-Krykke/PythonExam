# Presentation file
# Contains charts
# Start-point is this tutorial: https://stackabuse.com/python-for-nlp-sentiment-analysis-with-scikit-learn//
# IMPORTS:
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import nltk

# Test Data Path
test_data_path = "../../data/test_tweets/presentation_test_tweets.csv"


def get_data_from_csv(test_data_path):
    """
    Importing CSV data as pandas DataFrame. 

    Parameters:
    test_data_path (string): Path to the CSV data you want to import. 

    Returns:
    Pandas DataFrame
    """

    test_tweets = pd.read_csv(test_data_path)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    return test_tweets


# Getting the test_data.
test_data = get_data_from_csv(test_data_path)
# Manually testing if we got it how we want it.
print(test_data.head())
