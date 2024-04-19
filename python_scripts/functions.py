import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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
    patient_ids = ["".join(random.choices("0123456789", k=9)) for _ in range(len(df))]

    # Create a new column in df for these IDs
    df["Patient_ID"] = patient_ids

    # Make 'Patient_ID' the first column and set it to index
    df = df.set_index("Patient_ID")

    return df


################################################################################
############################ Data Types Report #################################
################################################################################


def data_types(df):
    """
    This function provides a data types report on every column in the dataframe,
    showing column names, column data types, number of nulls, and percentage
    of nulls, respectively.
    Inputs:
        df: dataframe to run the datatypes report on
    Outputs:
        dat_type: report saved out to a dataframe showing column name,
                  data type, count of null values in the dataframe, and
                  percentage of null values in the dataframe
    """
    # Features' Data Types and Their Respective Null Counts
    dat_type = df.dtypes

    # create a new dataframe to inspect data types
    dat_type = pd.DataFrame(dat_type)

    # sum the number of nulls per column in df
    dat_type["Null_Values"] = df.isnull().sum()

    # reset index w/ inplace = True for more efficient memory usage
    dat_type.reset_index(inplace=True)

    # percentage of null values is produced and cast to new variable
    dat_type["perc_null"] = round(dat_type["Null_Values"] / len(df) * 100, 0)

    # columns are renamed for a cleaner appearance
    dat_type = dat_type.rename(
        columns={
            0: "Data Type",
            "index": "Column/Variable",
            "Null_Values": "# of Nulls",
            "perc_null": "Percent Null",
        }
    )

    return dat_type


################################################################################
############################# Stacked Bar Plot #################################
################################################################################


def stacked_plot(
    x,
    y,
    p,
    df,
    col,
    truth,
    condition,
    kind,
    width,
    rot,
    ascending=True,
    string=None,
    custom_order=None,
    legend_labels=False,
    image_path=None,
    img_string=None,
    save_formats=None,
    custom_title=None,
    color=None,
):
    """
    Generates a pair of stacked bar plots for a specified column against a ground
    truth column, with the first plot showing absolute distributions and the
    second plot showing normalized distributions. Offers customization options for
    plot titles, colors, and more.

    Parameters:
    - x (int): The width of the figure.
    - y (int): The height of the figure.
    - p (int): The padding between the subplots.
    - df (DataFrame): The pandas DataFrame containing the data.
    - col (str): The name of the column in the DataFrame to be analyzed.
    - truth (str): The name of the ground truth column in the DataFrame.
    - condition: Unused parameter, included for future use.
    - kind (str): The kind of plot to generate (e.g., 'bar', 'barh').
    - width (float): The width of the bars in the bar plot.
    - rot (int): The rotation angle of the x-axis labels.
    - ascending (bool, optional): Determines the sorting order of the DataFrame
      based on the 'col'. Defaults to True.
    - string (str, optional): Descriptive string to include in the title of the plots.
      If `custom_title` is not provided, this string is used as part of the
      constructed title.
    - custom_order (list, optional): Specifies a custom order for the categories
      in the 'col'. If provided, the DataFrame is sorted according to this order.
    - legend_labels (bool or list, optional): Specifies whether to display legend labels
      and what those labels should be. If False, no legend is displayed. If a
      list, the list values are used as legend labels.
    - image_path (str, optional): Directory path where generated plot image will be saved.
    - img_string (str, optional): Filename for the saved plot image.
    - save_formats (list, optional): List of file formats to save the plot images in.
    - custom_title (str, optional): Custom title for the plots. If provided, it overrides
      the title constructed from `string` and `truth`.
    - color (list, optional): List of colors to use for the plots. If not provided,
      a default color scheme is used.

    Returns:
    - None: The function creates & displays the plots but doesn't return any value.

    Note:
    - The function assumes the matplotlib and pandas libraries have been
      imported as plt and pd respectively.
    - The function automatically handles the layout and spacing of the subplots
      to prevent overlap.
    """

    # Default color settings
    if color is None:
        color = ["#00BFC4", "#F8766D"]  # Default colors

    # Setting custom order if provided
    if custom_order:
        df[col] = pd.Categorical(df[col], categories=custom_order, ordered=True)
        df.sort_values(
            by=col, inplace=True
        )  # Ensure the DataFrame respects the custom ordering

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(x, y))
    fig.tight_layout(w_pad=5, pad=p, h_pad=5)
    # fig.suptitle(
    #     "Absolute Distributions vs. Normalized Distributions",
    #     fontsize=12,
    # )

    # Crosstabulation of column of interest and ground truth
    crosstabdest = pd.crosstab(df[col], df[truth])

    # Normalized crosstabulation
    crosstabdestnorm = crosstabdest.div(crosstabdest.sum(1), axis=0)

    # Title construction logic with prioritization
    if custom_title is not None:
        # If custom_title is provided, use it directly for title1
        title1 = custom_title
        # Decide if you want title2 to automatically append "(Normalized)" or not
        title2 = custom_title + " (Normalized)"  # or just custom_title if you prefer
    else:
        # Construct titles using string and truth if custom_title is not provided
        base_title = (
            string if string else "Distribution"
        )  # Default title component if string is None
        title1 = f"{base_title} by {truth.capitalize()}"
        title2 = f"{base_title} by {truth.capitalize()} (Normalized)"

    xlabel1 = xlabel2 = f"{col}"
    ylabel1 = "Count"
    ylabel2 = "Frequency"

    # Plotting the first stacked bar graph
    crosstabdest.plot(
        kind=kind,
        stacked=True,
        title=title1,
        ax=axes[0],
        color=color,
        width=width,
        rot=rot,
        fontsize=12,
    )
    axes[0].set_title(title1, fontsize=12)
    axes[0].set_xlabel(xlabel1, fontsize=12)
    axes[0].set_ylabel(ylabel1, fontsize=12)
    axes[0].legend(legend_labels, fontsize=12)

    # Plotting the second, normalized stacked bar graph
    crosstabdestnorm.plot(
        kind=kind,
        stacked=True,
        title=title2,
        ylabel="Frequency",
        ax=axes[1],
        color=color,
        width=width,
        rot=rot,
        fontsize=12,
    )
    axes[1].set_title(label=title2, fontsize=12)
    axes[1].set_xlabel(xlabel2, fontsize=12)
    axes[1].set_ylabel(ylabel2, fontsize=12)
    axes[1].legend(legend_labels, fontsize=12)

    fig.align_ylabels()

    if img_string and save_formats and isinstance(image_path, dict):
        for save_format in save_formats:
            if save_format in image_path:
                # `save_path` should be the full file path including the
                # filename, not a directory.
                full_path = image_path[save_format]
                plt.savefig(full_path, bbox_inches="tight")

    plt.show()
