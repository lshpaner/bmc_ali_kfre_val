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

    def __init__(
        self,
        data,
        columns,
    ):
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

    def perform_conversions(self):
        """
        Applies unit conversions to the biochemical markers in the dataset.

        Converts:
        - uPCR from mmol to mg/g
        - Calcium from mmol to mg/g
        - Phosphate from mmol to mg/g
        - Albumin from g/L to g/dL
        """
        self.data["uPCR (mg/g)"] = self.data[self.columns["uPCR_mmol"]] * 8.84
        self.data["Calcium (mg/dL)"] = self.data[self.columns["calcium_mmol"]] * 4
        self.data["Phosphate (mg/dL)"] = self.data[self.columns["phosphate_mmol"]] * 3.1
        self.data["Albumin (g/dL)"] = self.data[self.columns["albumin_g_per_l"]] / 10

    def predict_kfre(self, years, use_extra_vars=False, num_vars=4):
        """
        Predicts the risk of CKD for the given number of years, optionally using
        extra variables for the prediction.

        Parameters:
        years (int): The number of years for which to predict the risk.
        use_extra_vars (bool, optional): Whether to use extra variables
                                         (diabetes and hypertension status)
                                         for the prediction.
        num_vars (int, optional): The number of variables to use for the prediction.

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

        if use_extra_vars and num_vars == 6:
            dm = self.data.get(self.columns["dm"], None)
            htn = self.data.get(self.columns["htn"], None)
            return risk_pred(
                age,
                sex,
                eGFR,
                uACR,
                region,
                dm,
                htn,
                years=years,
            )

        elif use_extra_vars and num_vars == 8:
            albumin = self.data.get(self.columns["albumin"], None)
            phosphorous = self.data.get(self.columns["phosphorous"], None)
            bicarbonate = self.data.get(self.columns["bicarbonate"], None)
            calcium = self.data.get(self.columns["calcium"], None)
            return risk_pred(
                age,
                sex,
                eGFR,
                uACR,
                region,
                albumin=albumin,
                phosphorous=phosphorous,
                bicarbonate=bicarbonate,
                calcium=calcium,
                years=years,
            )

        else:
            return risk_pred(age, sex, eGFR, uACR, region, years=years)


################################################################################
################################ uPCR to uACR ##################################
################################################################################


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


def risk_pred(
    age,
    sex,
    eGFR,
    uACR,
    Region,
    dm=None,
    htn=None,
    albumin=None,
    phosphorous=None,
    bicarbonate=None,
    calcium=None,
    years=2,
):
    """
    Calculates a risk prediction for a patient based on demographic and clinical
    data using either a 4-variable, 6-variable, or 8-variable model.

    Parameters:
    - age (float): Age of the patient.
    - sex (int): Biological sex of the patient, 0 for female and 1 for male.
    - eGFR (float): Estimated Glomerular Filtration Rate, a measure of kidney function.
    - uACR (float): Urinary Albumin to Creatinine Ratio, an indicator of kidney damage.
    - Region (str): Geographic region of the patient, influences model constants.
    - dm (float, optional): Diabetes mellitus indicator (0 or 1).
    - htn (float, optional): Hypertension indicator (0 or 1).
    - albumin (float, optional): Serum albumin level, required for the 8-variable model.
    - phosphorous (float, optional): Serum phosphorous level, required for the 8-variable model.
    - bicarbonate (float, optional): Serum bicarbonate level, required for the 8-variable model.
    - calcium (float, optional): Serum calcium level, required for the 8-variable model.
    - years (int, default=2): The time horizon of the risk prediction, typically 2 or 5 years.

    Returns:
    - risk_prediction (float): The computed risk of developing the condition, as a probability between 0 and 1.

    Notes:
    The function dynamically selects between a 4-variable, 6-variable, or 8-variable model based
    on the availability of optional parameters. The risk factors and coefficients are adjusted
    based on the patient's geographic region and the specified number of years for prediction.
    """
    # Determine alpha based on region, years, and the variables used
    if dm is not None and htn is not None:
        # 6-variable model (uses 4-var coefficients for risk factors)
        alpha_values = {
            (True, 2): 0.9750,
            (True, 5): 0.9240,
            (False, 2): 0.9830,
            (False, 5): 0.9370,
        }
        base_risk_factors = {
            "age": -0.2201,
            "sex": 0.2467,
            "eGFR": -0.5567,
            "uACR": 0.4510,
        }
    elif (
        albumin is not None
        and phosphorous is not None
        and bicarbonate is not None
        and calcium is not None
    ):
        # 8-variable model (uses specific coefficients for risk factors)
        alpha_values = {
            (True, 2): 0.9780,
            (True, 5): 0.9301,
            (False, 2): 0.9827,
            (False, 5): 0.9245,
        }
        base_risk_factors = {
            "age": -0.1992,
            "sex": 0.1602,
            "eGFR": -0.4919,
            "uACR": 0.3364,
        }
    else:
        # 4-variable model (standard coefficients for risk factors)
        alpha_values = {
            (True, 2): 0.9750,
            (True, 5): 0.9240,
            (False, 2): 0.9832,
            (False, 5): 0.9365,
        }
        base_risk_factors = {
            "age": -0.2201,
            "sex": 0.2467,
            "eGFR": -0.5567,
            "uACR": 0.4510,
        }

    # Check if the region is North American
    is_north_american = Region == "North American"
    # Set alpha based on region and years

    alpha = np.where(
        is_north_american,
        np.where(years == 2, alpha_values[(True, 2)], alpha_values[(True, 5)]),
        np.where(years == 2, alpha_values[(False, 2)], alpha_values[(False, 5)]),
    )

    # Make sure uACR is positive to take the log
    uACR = np.where(uACR <= 0, 1e-6, uACR)
    log_uACR = np.log(uACR)

    # Initialize risk prediction factors
    risk_factors = (
        base_risk_factors["age"] * (age / 10 - 7.036)
        + base_risk_factors["sex"] * (sex - 0.5642)
        + base_risk_factors["eGFR"] * (eGFR / 5 - 7.222)
        + base_risk_factors["uACR"] * (log_uACR - 5.137)
    )

    if dm is not None and htn is not None:
        dm_factor = -0.1475 * (dm - 0.5106)
        htn_factor = 0.1426 * (htn - 0.8501)
        risk_factors += dm_factor + htn_factor
    if (
        albumin is not None
        and phosphorous is not None
        and bicarbonate is not None
        and calcium is not None
    ):
        albumin_factor = -0.3441 * (albumin - 3.997)
        phosph_factor = +0.2604 * (phosphorous - 3.916)
        bicarb_factor = -0.07354 * (bicarbonate - 25.57)
        calcium_factor = -0.2228 * (calcium - 9.355)
        risk_factors += albumin_factor + phosph_factor + bicarb_factor + calcium_factor

    risk_prediction = 1 - alpha ** np.exp(risk_factors)
    return risk_prediction
