class RiskPredictor:
    """
    A class to represent a risk predictor for chronic kidney disease (CKD).

    This class uses the Tangri risk prediction model, which calculates risk
    based on various patient parameters. Results are accurate for both males
    and females, but the original paper calculated risk specifically for males.

    Attributes:
    data (DataFrame): The patient data.
    Sex (Series): The sex of the patients, determined from the data.

    Methods:
    predict(years, use_extra_vars): Predicts the risk of CKD for the given
                                    number of years, optionally using extra
                                    variables for the prediction.
    """

    def __init__(self, data, sex):
        """
        Constructs the necessary attributes for the RiskPredictor object.

        Parameters:
        data (DataFrame): The patient data.
        Sex (str): Column name in the data for the sex of the patients.
        """
        self.data = data
        self.sex = self.data[sex] == "male"

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
        if use_extra_vars:
            return risk_pred(
                self.data["age"],
                self.sex,
                self.data["eGFR"],
                self.data["uACR"],
                self.data["Region"],
                self.data["dm"],
                self.data["htn"],
                years=years,
            )
        else:
            return risk_pred(
                self.data["age"],
                self.sex,
                self.data["eGFR"],
                self.data["uACR"],
                self.data["Region"],
                years=years,
            )
