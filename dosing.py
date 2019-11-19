import sys
import pandas as pd
import plotly
import plotly.graph_objs as go


# MAKE SURE THIS VERSION 4.3.0
plotly.__version__ 

file1 = pd.read_csv("t2_ec 20190619.csv")
file2 = pd.read_csv("t2_registry 20190619.csv")


registry_df = file2
ec_df = file1

file1.columns
file2.columns

# Example of value_counts() 
# 1) bl is NOT in the piechart 
# 2) filter out rows where SVPERF is not Y 

file2["VISCODE"].value_counts() 

len(file2)

# concatenating multiple conditionals to do selection
rows_of_interest = file2[(file2["SVPERF"] == "Y") & (file2["VISCODE"] != "bl")]

rows_of_interest["VISCODE"]
rows_of_interest["VISCODE"].value_counts()

type(rows_of_interest["VISCODE"].value_counts())
rows_of_interest["VISCODE"].value_counts() / len(rows_of_interest)


type(pd.DataFrame(rows_of_interest["VISCODE"].value_counts()))

pie_chart_data = pd.DataFrame(rows_of_interest["VISCODE"].value_counts())

pie_chart_data

# Native 
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.pie.html
pie_chart_data.plot.pie(y="VISCODE", figsize=(5,5))

pie_chart_data

# turn the index labels from an pandas.Index object, into a normal list, because
# plotly Pie chart API requires labels to be passed in as a normal list
labels = list(pie_chart_data.index)

type(pie_chart_data.index)

values = list(pie_chart_data["VISCODE"].values)

# actual creation of the Chart 
fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

fig.show()

result = pd.merge(registry_df, ec_df, how="left", on=["RID", "VISCODE"])

# filtering 
conditions = (result["VISCODE"] == "w02") & (result["SVDOSE"] == "Y") & (result["ECSDSTXT"] != 280)

result = result[conditions]

# specifying which columns to include
# shrink it down
columns_to_include = ["ID_x", "RID", "USERID_x", "VISCODE", "SVDOSE", "ECSDSTXT"]
result = result[columns_to_include]

# rename columns
result = result.rename(columns={"ID_x": "ID", "USERID_x": "USERID"})

result

# output the csv file without index 
result.to_csv("report.csv", index=False)

def output_csv(viscode, svdose, ecsdstxt, output_filename):
    
    # Plotly Piechart:
    pie_chart_data.plot.pie(y="VISCODE", figsize=(5,5))
    
    # read the files
    file2 = pd.read_csv("t2_registry 20190619.csv")
    file1 = pd.read_csv("t2_ec 20190619.csv")
    
    # rename dataframes
    registry_df = file2
    ec_df = file1
    
    # merging
    result = pd.merge(registry_df, ec_df, how="left", on=["RID", "VISCODE"])
    
    # filtering 
    conditions = (result["VISCODE"] == viscode) & (result["SVDOSE"] == svdose) \
            & (result["ECSDSTXT"] != ecsdstxt)

    result = result[conditions]
    
    columns_to_include = ["ID_x", "RID", "USERID_x", "VISCODE", "SVDOSE", "ECSDSTXT"]
    result = result[columns_to_include]

    # rename columns
    result = result.rename(columns={"ID_x": "ID", "USERID_x": "USERID"})    
    
    # output the csv file without index 
    result.to_csv(output_filename, index=False)

if __name__ == "__main__":
    # write code for reading the arguments
    
    commandLineArguments =  sys.argv[1:] # it will loop throught he arguments
    viscode = commandLineArguments[0]
    svdose =  commandLineArguments[1]
    ecsdstxt =commandLineArguments[2]
    output_filename = commandLineArguments[3]
    
    # invoke the report generating routine 
    output_csv(viscode, svdose, ecsdstxt, output_filename)
 
    result.to_csv("results.csv", index = False)