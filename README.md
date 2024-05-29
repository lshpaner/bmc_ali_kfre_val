# KFRE Validation for Advanced CKD Study by Ali et al.


--------
## Table of Contents

1. [Overview](#Overview)
2. [Repository Structure](#repository-structure)
3. [Features](#Features)
4. [Getting Started](#Getting-Started) 
   - [Prerequisites](#prerequisites) 
5. [Installation](#installation)
6. [Usage](#usage)
   - [Data Exploration](https://github.com/lshpaner/bmc_ali_kfre_val/blob/main/notebooks/eda.ipynb)
   - [Preprocessing](https://github.com/lshpaner/bmc_ali_kfre_val/blob/main/notebooks/preprocessing.ipynb)
   - [Validation](https://github.com/lshpaner/bmc_ali_kfre_val/blob/main/notebooks/kfre_reproduction.ipynb)
7. [License](#license)
8. [Data Usage](#data-usage)
9. [Contributions](#contributions)
10. [References](#references)
--------

## Overview

This repository contains the validation of the Kidney Failure Risk Equation (KFRE) using the dataset provided in the study "A Validation Study of the Kidney Failure Risk Equation in Advanced Chronic Kidney Disease According to Disease Aetiology with Evaluation of Discrimination, Calibration and Clinical Utility" by Dr. Ibrahim Ali.

The Kidney Failure Risk Equation (KFRE) is a valuable tool for predicting the risk of kidney failure in patients with chronic kidney disease (CKD). This repository demonstrates the use of the `kfre` Python library to validate Dr. Ali's dataset, showcasing its efficacy and potential applications in clinical and research settings.

## Repository Structure

``` bash
kfre-validation/
├── data/                      # Contains the dataset used for validation
│   ├── 12882_2021_2402_MOESM8_ESM.csv
│   ├── df.parquet
│   ├── df_eda.parquet
│   ├── df_kfre.csv
│   ├── new_df.csv
│   └── outcomes_by_age_group.xlsx
├── images/                    # Contains images generated during validation
│   ├── png_images/
│   └── svg_images/
├── notebooks/                 # Jupyter notebooks for interactive analysis
│   ├── eda.ipynb
│   ├── kfre_reproduction.ipynb
│   └── preprocessing.ipynb
├── python_scripts/            # Python scripts for data processing and validation
│   └── functions.py
├── .gitignore                 # Git ignore file
├── README.md                  # This README file
└── requirements.txt           # Required Python packages

```

## Features
- **Reproduction of KFRE Equations:** Utilizing the kfre Python library to accurately reproduce the KFRE equations developed by Tangri et al.
- **Validation of Dataset:** Applying the KFRE to Dr. Ali's dataset to evaluate its discrimination, calibration, and clinical utility.
- **Comprehensive Analysis:** Detailed analysis and results presented through various statistical metrics and visualizations.

## Getting Started

### Prerequisites
Ensure you have the following installed:

- Python 3.6+
- kfre library
- Jupyter Notebook (optional, for running notebooks)

## Installation

1. Clone the repository

```bash

git clone https://github.com/lshpaner/kfre-validation.git
cd kfre-validation

```

2. Install the kfre Library:

```bash

pip install kfre

```

## Usage

Explore the Jupyter Notebooks:

- [Data Exploration](https://github.com/lshpaner/bmc_ali_kfre_val/blob/main/notebooks/eda.ipynb)
- [Preprocessing](https://github.com/lshpaner/bmc_ali_kfre_val/blob/main/notebooks/preprocessing.ipynb)
- [Validation](https://github.com/lshpaner/bmc_ali_kfre_val/blob/main/notebooks/kfre_reproduction.ipynb)

## License

The code in this repository is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

## Data Usage
The dataset used for validation belongs to Dr. Ibrahim Ali and is used with permission. Any use of this data should comply with the guidelines and permissions set by the original author.

## Contributions
Contributions to this project are welcome. If you have any suggestions, improvements, or issues, please open a pull request or an issue on GitHub.

## References

Ali, I., Donne, R. L., & Kalra, P. A. (2021). A validation study of the kidney failure risk equation in advanced chronic kidney disease according to disease aetiology with evaluation of discrimination, calibration and clinical utility. *BMC Nephrology, 22(1),* 194.  doi: 10.1186/s12882-021-02402-1