# General
import io
import gc
import timeit
import pandas as pd
import numpy as np
from math import prod

# Visualizations
import matplotlib.pyplot as plt
import seaborn as sns


def df_analysis(df, name_df, *args, **kwargs):
    """
    Method used to analyze on the DataFrame.

    Parameters:
    -----------------
        df (pandas.DataFrame): Dataset to analyze
        name_df (str): Dataset name

        *args, **kwargs:
        -----------------
            columns (list): Dataframe keys in list format
            flag (str): Flag to show complete information about
                        the dataset to analyse "complete" shows
                        all information about the dataset
                        
                analysis_type (str) : the analysis type are 
                                      ["complete", "summarized", "header"]
                                      By defaut "complete"

    Returns:
    -----------------
        None.
        Print the analysis on the Dataset.
    """

    # Getting the variables
    columns = kwargs.get("columns", None)

    # Getting the variables
    # the analysis type are ["complete", "summarized", "header"]
    # By defaut "complete"
    analysis_type = kwargs.get("analysis_type", None)

    columns_reduced = [
        "name", "type", "records", "unique"
    ]

    columns_complete = columns_reduced + ["# NaN", "% NaN", "mean",
                                          "min", "25%", "50%",
                                          "75%", "max", "std"]

    # Identifying the columns name length
    columns_name_length = []
    for col in df.columns:
        columns_name_length.append(len(col))

    # Calculating the memory usage based on dataframe.info()
    buf = io.StringIO()
    df.info(buf=buf)
    memory_usage = buf.getvalue().split("\n")[-2]

    if df.empty:
        print("The", name_df, "dataset is empty. Please verify the file.")
    else:
        empty_cols = [col for col in df.columns
                      if df[col].isna().all()]  # identifying empty columns
        df_rows_duplicates = df[df.duplicated()]  # identifying duplicates rows
        

        # Creating a dataset based on Type object and records by columns
        type_cols = df.dtypes.apply(lambda x: x.name).to_dict()
        df_resume = pd.DataFrame(list(type_cols.items()),
                                 columns=["name", "type"])
        df_resume["records"] = list(df.count())
        df_resume["unique"] = list(df.nunique())
        df_resume["# NaN"] = list(df.isnull().sum())
        df_resume["% NaN"] = list(((df.isnull().sum()
                                    / len(df.index))*100).round(2))
        
        print("\nAnalysis Header of", name_df, "dataset")
        print(80*"-")

        print("- Dataset shape:\t\t\t", df.shape[0], "rows and",
              df.shape[1], "columns")
        print("- Total of NaN values:\t\t\t", df.isna().sum().sum())
        print("- Percentage of NaN:\t\t\t",
              round((df.isna().sum().sum()/prod(df.shape))
                    * 100, 2), "%")
        print("- Total of infinite values:\t\t", np.isinf(df).values.sum())
        print("- Percentage of infinite values:\t",
              round((np.isinf(df).values.sum()/prod(df.shape))
                    * 100, 2), "%")
        print("- Total of full duplicates rows:\t",
              df_rows_duplicates.shape[0])

        if df.dropna(axis="rows", how="all").shape[0] < df.shape[0]:
            print("- Total of empty rows:\t\t\t",
                  df.shape[0] - df.dropna(axis="rows", how="all"))
        else:
            print("- Total of empty rows:\t\t\t", "0")

        print("- Total of empty columns:\t\t", len(empty_cols))

        if len(empty_cols) == 1 or len(empty_cols) >= 1:
            print("\t+ The empty column is:\t\t", empty_cols)
        else:
            None

        print("- Unique indexes:\t\t\t", df.index.is_unique)
        print("- Memory usage:\t\t\t\t",
              memory_usage.split("memory usage: ")[1])

        if columns is not None:
            string_present = "present multiple times in the dataframe."
            string_used = "be used as a primary key."
            string_error = "Column does not exist"

            try:

                if df.size == df.drop_duplicates(columns).size:
                    print("\n- The key(s):\t", columns, "is not",
                          string_present, "\n\t\t It CAN", string_used)
                else:
                    print("\n- The key(s):\t", columns, "is", string_present,
                          "\n\t\t It CANNOT", string_used)
            except Exception:
                print("\n- The key(s):\t\033[31m", string_error,
                      "\033[0m", sep="")

        # Enabling the visualizacion of
        # all columns, rows, cell and floar format
        pd.set_option("display.max_rows", None)  # all rows
        pd.set_option("display.max_columns", None)  # all cols
        pd.set_option("display.max_colwidth", None)  # whole cell
        pd.set_option("display.float_format",
                      lambda x: "%.5f" % x)  # full floating number

        if analysis_type == "complete" or analysis_type is None:
            df_resume["unique"] = list(df.nunique())

            # Adding describing columns
            if (df.select_dtypes(["int64"]).shape[1] > 0 or
                    df.select_dtypes(["float64"]).shape[1] > 0):

                df_desc = pd.DataFrame(df.describe().T).reset_index()
                df_desc = df_desc.rename(columns={"index": "name"})
                df_resume = df_resume.merge(right=df_desc[["name", "mean",
                                                           "min", "25%",
                                                           "50%", "75%",
                                                           "max", "std"]],
                                            on="name", how="left")
                df_resume = df_resume[columns_complete]

                if max(columns_name_length) > 18:
                    n = 132
                else:
                    n = 120
            else:
                df_resume = df_resume[columns_reduced]
                n = 70

            print("\nDetailed analysis of", name_df, "dataset")
            print(n*"-")

            display(df_resume.sort_values("records", ascending=False))

            if (df.select_dtypes(["int64"]).shape[1] > 0 or
                    df.select_dtypes(["float64"]).shape[1] > 0):
                del [[df_resume, df_desc]]
            else:
                del [[df_resume]]

            gc.collect()
            df_resume, df_desc = (pd.DataFrame() for i in range(2))

        elif analysis_type == "header":
            del df_resume
            gc.collect()
            df_resume = pd.DataFrame()

        pd.reset_option("display.max_rows")  # reset max of showing rows
        pd.reset_option("display.max_columns")  # reset max of showing cols
        pd.reset_option("display.max_colwidth")  # reset width of showing cols
        pd.reset_option("display.float_format")  # reset float format in cell
        

def barplot_and_pie(df, title, subtitle_keyword):
    """
    Method used to plot a bar and pie graph.

    Parameters:
    -----------------
        df (pandas.DataFrame): Column dataset to analyze
        title (str): Graph name
        subtitle_keyword (str); Subtitle graph name

    Returns:
    -----------------
        None.
        PLot the graphs.
    """

    # Getting the data to plot them
    data = df.sort_values(ascending=False).value_counts().values.tolist()
    labels = df.sort_values(ascending=False).value_counts().index.tolist()

    if len(data) > 10:
        figsize = [25, 10]
    else:
        figsize = [9, 5]

    # defining the color palette
    colors = sns.color_palette()

    # Setting up the fig
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=figsize)
    fig.suptitle(title, size=25)

    # Setting up the pieplot
    ax1.set_title(subtitle_keyword + " by percentage (%)", size=14)
    ax1.pie(x=data, labels=labels, colors=colors, autopct='%1.1f%%')

    # Setting up the barplot
    ax2.set_title(subtitle_keyword + " by quantity (#)", size=14)
    plot = sns.barplot(x=labels, y=data, ax=ax2, palette=colors)
    plot.set_xticklabels(labels=labels, rotation=70, size=12,
                         horizontalalignment="right")

    for index, d in enumerate(data):
        plt.text(x=index, y=d+1, s=f"{d}", horizontalalignment="center",
                 fontdict=dict(fontsize=10, color="gray"))

    plt.tight_layout()
    plt.show()
