import matplotlib.pyplot as plt
import pandas as pd

# stage 1

f1 = "test/general.csv"
f2 = "test/prenatal.csv"
f3 = "test/sports.csv"

general_df = pd.read_csv(f1)
prenatal_df = pd.read_csv(f2)
sports_df = pd.read_csv(f3)

# print(general_df.head(20))
# print(prenatal_df.head(20))
# print(sports_df.head(20))

# stage 2
prenatal_df.rename(
    columns={
        "HOSPITAL": "hospital",
        "Sex": "gender",
    },
    inplace=True
)
sports_df.rename(
    columns={
        "Hospital": "hospital",
        "Male/female": "gender",
    },
    inplace=True
)

# print(general_df.columns)
# print(prenatal_df.columns)
# print(sports_df.columns)

final_df = pd.concat(objs=[general_df, prenatal_df, sports_df], axis=0, ignore_index=True)

# dropping column which contains old indexes
final_df.drop(columns='Unnamed: 0', inplace=True)

# print(final_df.sample(n=20, random_state=30))

# stage 3
final_df.dropna(
    axis=0,
    how='all',  # all: if all cells empty, any: if any cell is empty
    inplace=True
)

r = final_df["gender"].unique().tolist()
final_df["gender"] = final_df["gender"].apply(lambda x: "m" if x in ["man", "male"] else x)
final_df["gender"] = final_df["gender"].apply(lambda x: "f" if x in ["woman", "female"] else x)
final_df["gender"] = final_df["gender"].apply(lambda x: "f" if pd.isna(x) else x)
columns = ["bmi", "diagnosis", "blood_test", "ecg", "ultrasound", "mri", "xray", "children", "months"]
for c in columns:
    final_df[c] = final_df[c].apply(lambda x: 0 if pd.isna(x) else x)
# print(final_df.shape)
# print(final_df.sample(n=20, random_state=30))

# stage 4
one = final_df.groupby("hospital").aggregate({"hospital": "count"}).idxmax()[0]

a = final_df["diagnosis"][(final_df["hospital"] == "general") & (final_df["diagnosis"] == "stomach")]
# a = final_df["diagnosis"][(final_df["hospital"] == "general")].value_counts("stomach")
b = final_df["diagnosis"][final_df["hospital"] == "general"]
two = round(a.count() / b.count(), 3)

a = final_df["diagnosis"][(final_df["hospital"] == "sports") & (final_df["diagnosis"] == "dislocation")]
b = final_df["diagnosis"][final_df["hospital"] == "sports"]
three = round(a.count() / b.count(), 3)

a = final_df[final_df["hospital"] == "general"].aggregate({"age": "median"}).values[0]
b = final_df[final_df["hospital"] == "sports"].aggregate({"age": "median"}).values[0]
four = a - b

a = final_df[["hospital", "blood_test"]][final_df["blood_test"] == "t"] \
    .groupby("hospital") \
    .aggregate({"blood_test": "count"})
five = a.idxmax()[0]
six = a.max()[0]

"""Alternative
1st question:
    df.hospital.value_counts().index[0]
2nd question:
    df.diagnosis.loc[df.hospital == 'general'].value_counts()["stomach"] / df.loc[df.hospital == 'general'].diagnosis.count()).round(3)
3rd question:
    df.diagnosis.loc[df.hospital == 'sports'].value_counts()["dislocation"] / df.loc[df.hospital == 'sports'].diagnosis.count()).round(3)
4th question:
    df.age.loc[df.hospital == 'general'].median() - df.age.loc[df.hospital == 'sports'].median()
5th question:
    df.groupby("hospital")["blood_test"].value_counts().sort_values(ascending=False).index[0][0]
    df.groupby("hospital")["blood_test"].value_counts().sort_values(ascending=False)[0]
"""

# print(f"The answer to the 1st question is {one}")
# print(f"The answer to the 2st question is {two}")
# print(f"The answer to the 3st question is {three}")
# print(f"The answer to the 4st question is {four}")
# print(f"The answer to the 5st question is {five}, {six} blood tests")

# stage 5

"""What is the most common age of a patient among all hospitals? Plot a histogram and choose one of the following age ranges: 0-15, 15-35, 35-55, 55-70, or 70-80
What is the most common diagnosis among patients in all hospitals? Create a pie chart
Build a violin plot of height distribution by hospitals."""

# plot with pandas
# final_df.plot(y=['age'], kind='hist', bins=8, alpha=1)
# final_df.plot(y=['age'], kind='hist', bins=[0, 15, 35, 55, 70, 80])

# histogram
plt.hist(x=final_df["age"], bins=[0, 15, 35, 55, 70, 80], range=[0, 80])

# pie chart
plt.figure()
diagnosis = final_df.groupby("diagnosis").aggregate({"diagnosis": "count"})
labels = diagnosis.index.tolist()
x = [value[0] for value in diagnosis.values]
plt.pie(x=x, labels=labels)
plt.savefig("figure.png")

diagnosis = final_df.groupby("diagnosis").aggregate({"diagnosis": "count"})
labels = diagnosis.index.tolist()
x = [value[0] for value in diagnosis.values]
plt.pie(x=x, labels=labels)
plt.savefig("figure.png")

# violin plot
general = final_df["height"][final_df["hospital"] == "general"].tolist()
prenatal = final_df["height"][final_df["hospital"] == "prenatal"].tolist()
sports = final_df["height"][final_df["hospital"] == "sports"].tolist()
labels = final_df["hospital"].unique()
fig, axes = plt.subplots()
plt.violinplot(dataset=[general, prenatal, sports], showextrema=True, showmeans=True, showmedians=True)
axes.set_xticks((1, 2, 3))
axes.set_xticklabels(labels)
axes.set_ylabel("Height by hospital")
axes.set_title('Violin plot')

# alternative
# total_data = final_df.pivot(columns='hospital', values='height')
# gen_data = total_data.general.dropna()
# pren_data = total_data.prenatal.dropna()
# sport_data = total_data.sports.dropna()
#
# fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(20, 10))
# ax1.violinplot(gen_data, showextrema=True, showmeans=True, showmedians=True)
# ax1.set_title('General')
#
# ax2.violinplot(pren_data, showextrema=True, showmeans=True, showmedians=True)
# ax2.set_title('Prenatal')
#
# ax3.violinplot(sport_data, showextrema=True, showmeans=True, showmedians=True)
# ax3.set_title('Sports')

plt.show()

print(f"The answer to the 1st question: 15-35")
print("The answer to the 2nd question: pregnancy")
print("The answer to the 3rd question: It's because different units")
