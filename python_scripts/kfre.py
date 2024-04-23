import pandas as pd
import numpy as np


class RiskPredictor:
    """
    A class to represent a risk predictor for chronic kidney disease (CKD).

    This class uses the Tangri risk prediction model, which calculates risk
    based on various patient parameters. Results are accurate for both males
    and females, but the original paper calculated risk specifically for males.

    Attributes:
    data (DataFrame): The patient data.
    columns (dict): Dictionary to map expected parameter names to actual column
    names in the data.

    Methods:
    predict(years, use_extra_vars): Predicts the risk of CKD for the given
    number of years, optionally using extra variables for the prediction.
    """

    def __init__(self, data, columns,):
        """
        Constructs the necessary attributes for the RiskPredictor object.

        Parameters:
        data (DataFrame): The patient data.
        columns (dict): A dictionary specifying the column names in the dataset
        that correspond to the required parameters.
        Example: {'age': 'Age', 'sex': 'Gender', 'eGFR': 'eGFR',
        'uACR': 'Albumin_Ratio', 'region': 'Region', 'dm': 'Diabetes',
        'htn': 'Hypertension'}
        apply_conversions (bool, optional): Flag to apply unit conversions. 
        Default is False.
        """
        self.data = data
        self.columns = columns
        # if apply_conversions:
        #     # Perform the unit conversions with flexible column names
        #     self.data["uPCR (mg/g)"] = self.data[self.columns['uPCR_mmol']] * 4
        #     self.data["Calcium (mg/g)"] = self.data[self.columns['calcium_mmol']] * 4
        #     self.data["Phosphate (mg/g)"] = self.data[self.columns['phosphate_mmol']] * 3.1
        #     self.data["Albumin (g/dL)"] = self.data[self.columns['albumin_g_per_l']] / 10

    def perform_conversions(self):
        """
        Applies unit conversions to the biochemical markers in the dataset.

        Converts:
        - uPCR from mmol to mg/g
        - Calcium from mmol to mg/g
        - Phosphate from mmol to mg/g
        - Albumin from g/L to g/dL
        """
        self.data["uPCR (mg/g)"] = self.data[self.columns['uPCR_mmol']] * 8.84
        self.data["Calcium (mg/g)"] = self.data[self.columns['calcium_mmol']] * 4
        self.data["Phosphate (mg/g)"] = self.data[self.columns['phosphate_mmol']] * 3.1
        self.data["Albumin (g/dL)"] = self.data[self.columns['albumin_g_per_l']] / 10

    def predict(self, years, use_extra_vars=False):
        """
        Predicts the risk of CKD for the given number of years, optionally using
        extra variables for the prediction.

        Parameters:
        years (int): The number of years for which to predict the risk.
        use_extra_vars (bool, optional): Whether to use extra variables
                                         (diabetes and hypertension status)
                                         for the prediction.

        Returns:
        risk_prediction (float): The predicted risk of CKD.
        """
        # Accessing columns using user-defined mappings
        age = self.data[self.columns["age"]]
        sex = self.data[self.columns["sex"]].apply(
            lambda x: 1 if x is not None and x.lower() == "male" else 0
        )
        eGFR = self.data[self.columns["eGFR"]]
        uACR = self.data[self.columns["uACR"]]
        region = self.data.get(self.columns["region"], "Unknown")

        if use_extra_vars:
            dm = self.data.get(self.columns["dm"], None)
            htn = self.data.get(self.columns["htn"], None)
            return risk_pred(age, sex, eGFR, uACR, region, dm, htn, years)
        else:
            return risk_pred(age, sex, eGFR, uACR, region, years=years)


################################################################################
################################ uPCR to uACR ##################################


# Define the generalized conversion function from uPCR to uACR
def uPCR_to_uACR(
    row,
    sex_col,
    diabetes_col,
    hypertension_col,
    uPCR_col,
    female_str,
):
    """
    Converts urinary protein-creatinine ratio (uPCR) to urinary
    albumin-creatinine ratio (uACR) using a specified formula that considers
    patient demographics and conditions.

    Parameters:
    - row (pd.Series): A single row from a pandas DataFrame representing one
      patient's data.
    - sex_col (str): Column name containing the patient's gender.
    - diabetes_col (str): Column name indicating whether the patient has
      diabetes (1 for yes, 0 for no).
    - hypertension_col (str): Column name indicating whether the patient has
      hypertension (1 for yes, 0 for no).
    - uPCR_col (str): Column name containing the urinary protein-creatinine ratio.
    - female_str (str): The exact string used in the dataset to identify a
      patient as female, critical for accurate calculations.

    Returns:
    - float: The computed urinary albumin-creatinine ratio (uACR).

    This function applies a complex logarithmic and exponential calculation to
    derive the uACR from the uPCR, adjusting for factors such as gender,
    diabetes, and hypertension status. The accuracy of the function relies on
    the exact match of the 'female_str' with the dataset's representation of
    female gender.
    """
    uPCR = row[uPCR_col]
    female = 1 if row[sex_col] == female_str else 0
    diabetic = row[diabetes_col]
    hypertensive = row[hypertension_col]

    # Applying the provided formula
    uACR = np.exp(
        5.2659
        + 0.2934 * np.log(np.minimum(uPCR / 50, 1))
        + 1.5643 * np.log(np.maximum(np.minimum(uPCR / 500, 1), 0.1))
        + 1.1109 * np.log(np.maximum(uPCR / 500, 1))
        - 0.0773 * female
        + 0.0797 * diabetic
        + 0.1265 * hypertensive
    )
    return uACR


################################################################################
############################## KFRE Risk Predictor #############################
################################################################################


def risk_pred(age, sex, eGFR, uACR, Region, dm=None, htn=None, years=2):
    """
    This function calculates the risk prediction based on various parameters.
    Different coefficients are used in the calculation based on the geographical
    region and the duration (in years) for which the risk is being predicted.

    Parameters:
    Age (float): Age of the individual.
    Sex (float): Biological sex of the individual, usually coded as 1 for male
    and 0 for female.
    entry_egfrckdepi2009_mean (float):
    Mean eGFR (estimated Glomerular Filtration Rate) value.
    entry_uacr_mean (float): Mean uacr (Urinary Albumin-to-Creatinine Ratio)
    value.
    Region (str): Geographical region of the individual
    ('North American' or other).
    entry_dmid_flag (float, optional):
    Diabetes mellitus status of the individual.
    entry_htnid_flag (float, optional):
    Hypertension status of the individual.
    years (int, optional):
    Duration for which the risk is being predicted, either 2 or 5 years.

    Returns:
    risk_prediction (float): Calculated risk prediction.
    """

    # Determine the value of alpha based on the region and the duration
    if years == 2:
        alpha = np.where(Region == "North American", 0.9750, 0.9832)
    elif years == 5:
        alpha = np.where(Region == "North American", 0.9240, 0.9365)
    else:
        # Raise an error if an invalid duration is provided
        raise ValueError("Invalid years value. Choose 2 or 5.")

    # Calculate the diabetes factor, or set it to 0 if no diabetes
    # information is provided
    dm_factor = 0 if dm is None else -0.1475 * (dm - 0.5106)

    # Calculate the hypertension factor, or set it to 0 if no
    # hypertension information is provided
    htn_factor = 0 if htn is None else 0.1426 * (htn - 0.8501)

    # Return the calculated risk prediction
    return 1 - alpha ** np.exp(
        -0.2201 * (age / 10 - 7.036)
        + 0.2467 * (sex - 0.5642)
        - 0.5567 * (eGFR / 5 - 7.222)
        + 0.4510 * (np.log(uACR) - 5.137)
        + dm_factor
        + htn_factor
    )
