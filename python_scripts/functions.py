import pandas as pd
import numpy as np
import random  # for generating random numbers and performing random operations
import os
import sys

################################################################################
############################# Path Directories #################################


def ensure_directory(path):
    """Ensure that the directory exists. If not, create it."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
    else:
        print(f"Directory exists: {path}")


################################################################################
######################## Generate Random Patient IDs ###########################
################################################################################

def add_patient_ids(df, seed=None):
    """
    Add a column of unique, 9-digit patient IDs to the dataframe.

    This function sets a random seed and then generates a 9-digit patient ID for 
    each row in the dataframe. The new IDs are added as a new 'Patient_ID' 
    column, which is placed as the first column in the dataframe.

    Args:
        df (pd.DataFrame): The dataframe to add patient IDs to.
        seed (int, optional): The seed for the random number generator. 
        Defaults to 222.

    Returns:
        pd.DataFrame: The updated dataframe with the new 'Patient_ID' column.
    """
    random.seed(seed)

    # Generate a list of unique IDs
    patient_ids = [''.join(random.choices('0123456789', k=9)) 
                   for _ in range(len(df))]

    # Create a new column in df for these IDs
    df['Patient_ID'] = patient_ids

    # Make 'Patient_ID' the first column and set it to index
    df = df.set_index('Patient_ID')

    return df