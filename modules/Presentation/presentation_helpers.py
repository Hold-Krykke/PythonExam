import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import nltk


def save_plot(fig, name):
    '''
    Save Plot

    Parameters: 
        fig: Figure. pyplot fig. 
        name: string. Name of file. No extension. 


    Returns: 
        Nothing. 
    '''
    if (isinstance(name, str)):
        from pathlib import Path
        # https://stackoverflow.com/a/273227/11255140
        # if plots folder doesn't exist, create it.
        Path("./plots").mkdir(parents=True, exist_ok=True)
        # bbox_inces="tight" ensures less white space in the image.
        fig.savefig("./plots/"+name+".png", bbox_inces='tight')
        print("Successfully saved Plot to ./plots/"+name+".png")
    else:
        print("Name has to be a string.")


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


def plot_settings():
    """
    Used to set common settings for a pyplot
    """
    # https://stackoverflow.com/a/332311/11255140
    plot_size = plt.rcParams["figure.figsize"]
    plot_size[0] = 8  # width in inches
    plot_size[1] = 6  # height in inches
    plt.rcParams["figure.figsize"] = plot_size
