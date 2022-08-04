import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from src.feature.outlier_detection import df
ranker = pd.read_csv("data/external/crawl_220615_edit.csv")
ranker_describe = ranker.describe()
df_ranker = df.copy()
ranker = ranker.drop("killPlace",axis=1)
# boxplot - high ranker's behavior indicator
def calculate_quantile(dataframe, columns_name):
    x = df.copy()
    describe = dataframe.describe()
    for i in x.columns:
        if i in columns_name.columns:
            # print(i)
            # df = df[df["assists"] > ranker_describe.loc["25%"]["assists"]][df["assists"] < ranker_describe.loc["75%"]["assists"]]
            x = x[x[i] >= describe.loc["25%"][i]][x[i] <= describe.loc["75%"][i]]
    IQR_1 = x.winPlacePerc.quantile(.25)
    IQR_3 = x.winPlacePerc.quantile(.75)
    return describe,IQR_1,IQR_3,x
overlap_describe, overlap_IQR_1, overlap_IQR_3, overlap_df = calculate_quantile(ranker,ranker)

# each columns limit standard
def each_calculate_quantile(dataframe):
    x = df.copy()
    describe = dataframe.describe()
    total = []
    for i in x.columns:
        if i in dataframe.columns:
            print(i)
            each_column = []
            column_name = "ranker_" + i
            each_column.append(column_name)
            column_name = x[x[i] >= describe.loc["25%"][i]][x[i] <= describe.loc["75%"][i]]
            each_column.append(column_name.winPlacePerc.quantile(.25).item())
            each_column.append(column_name.winPlacePerc.quantile(.75).item())
            total.append(each_column)
    total_df = pd.DataFrame(total, columns=["columns_name","1IQR","3IQR"])
    return total_df
each_overlap_df = each_calculate_quantile(ranker)

# after process drop columns
def calculate_quantile_part(low=0.6,high=0.9):
    feature = each_overlap_df[each_overlap_df["1IQR"] > low][each_overlap_df["3IQR"] > high]
    test = []
    for i in feature.columns_name:
        i = i.lstrip("ranker_")
        test.append(i)
    x = df.copy()
    for i in x.columns:
        if i in test:
            print(i)
            # df = df[df["assists"] > ranker_describe.loc["25%"]["assists"]][df["assists"] < ranker_describe.loc["75%"]["assists"]]
            x = x[x[i] >= overlap_describe.loc["25%"][i]][x[i] <= overlap_describe.loc["75%"][i]]
    IQR_1 = x.winPlacePerc.quantile(.25)
    IQR_3 = x.winPlacePerc.quantile(.75)
    return IQR_1,IQR_3,x
feature_IQR_1, feature_IQR_3, feature_df = calculate_quantile_part()

feature_min = feature_IQR_1 - (feature_IQR_3-feature_IQR_1)*1.5
feature_max = feature_IQR_3 + (feature_IQR_3-feature_IQR_1)*1.5
sns.boxplot(feature_df.winPlacePerc)
plt.title(f"['boosts', 'damageDealt', 'longestKill'] min: {feature_min}")
plt.show()

"""EDA"""
# EDA - all columns limit
plt.figure(figsize=(14,8))
plt.subplot(1,2,1)
sns.boxplot(overlap_df.winPlacePerc)
plt.xlim([0,1])
plt.title("high rankers(kaggle data & crawling data overlap winPlacePerc)")
plt.subplot(1,2,2)
sns.boxplot(df.winPlacePerc)
plt.xlim([0,1])
plt.title("kaggle data")
plt.show()