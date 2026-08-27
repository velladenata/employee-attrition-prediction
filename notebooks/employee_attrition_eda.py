# data manipulation
import pandas as pd 
import numpy as np

# data visualization
import matplotlib.pyplot as plt

data = pd.read_csv("data/MFG10YearTerminationData.csv")

print("=" * 50)
print("Data information :\n")
data.info()
print("=" * 50)

print("=" * 50)
print("Data : \n")
print(data.head())
print("=" * 50)

print("=" * 50)
print("Data NULL :\n")
print(data.isnull().sum())
print("=" * 50)

print("=" * 50)
print("Data Describe :")
data_describe = data.describe(include='str')
print(data_describe)
print("=" * 50)

print("=" * 50)
data_duplicated = data.duplicated().sum()
print(f"Duplicate Sum :  {data_duplicated}")
print("=" * 50)

print("=" * 50)
employee_unique = data['EmployeeID'].nunique()
print(f"Employee unique : {employee_unique}")

shape = data.shape
print(f"Shape Data : {shape}")
print("=" * 50)

print("=" * 50)
print(data['STATUS'].value_counts())
print("=" * 50)

print("=" * 50)
print(data['gender_short'].value_counts())
print("=" * 50)

print("=" * 50)
conti_table1 = pd.crosstab(data['STATUS'], data['gender_short'])
print(conti_table1)
print("=" * 50)
# pada gender, gender "Female" memiliki termination rate lebih tinggi dibandingkan "Male", tetapi Active Rate nya juga sama. total Female lebih banyak daripada Male.

print("=" * 50)
print(data['department_name'].value_counts())
print("=" * 50)

print("=" * 50)
conti_table2 = pd.crosstab(data['department_name'], data['STATUS'], normalize='index')
print(conti_table2)
print("=" * 50)
# pada department, department "Produce" memiliki termination rate yang lebih tinggi dibandingkan department dengan jumlah anggota besar lainnya

print("=" * 50)
print(data['job_title'].value_counts())
print("=" * 50)

print("=" * 50)
conti_table3 = pd.crosstab(data['job_title'], data['STATUS'], normalize='index')
print(conti_table3)
print("=" * 50)
# pada job title, "Produce Clerk" punya termination rate tertinggi dari antara job title dengan jumlah yang besar. Direktur dan SA punya termination rate tinggi, tapi jumlah job titlenya sedikit.
# kita pilih "Produce Clerk" karena jumlah job titlenya lebih banyak, jadi observasi lebih stabil.

print("=" * 50)
# print(data['age'].max())
ageGroup = pd.cut(
    data['age'],
    bins=[0,25,35,45,55,100],
    labels=['<25', '25-34', '35-44', '45-54', '>=55'],
    right=False
)

data['age_group'] = ageGroup
print(data['age_group'].value_counts())
print("=" * 50)

print("=" * 50)
conti_table4 = pd.crosstab(data['age_group'], data['STATUS'], normalize='index')
print(conti_table4)
print("=" * 50)
# pada age group, kelompok usia ">= 55" memiliki termination rate yang lebih tinggi

print("=" * 50)
print("Max = ", data['length_of_service'].max())
print("Min = ", data['length_of_service'].min())
print(data['length_of_service'].value_counts())
print("=" * 50)

print("=" * 50)
lengthOfServiceGroup = pd.cut(
    data['length_of_service'],
    bins=[0,5,10,15,20,30],
    labels=['0-4 tahun', '5-9 tahun', '10-14 tahun', '15-19 tahun', '20+ tahun'],
    right=False
)

data['length_of_service_group'] = lengthOfServiceGroup
print(data['length_of_service_group'].value_counts())
print("=" * 50)

print("=" * 50)
conti_table5 = pd.crosstab(data['length_of_service_group'], data['STATUS'], normalize='index')
print(conti_table5)
print("=" * 50)
# pada length of service group, kelompok "10-14 tahun" memiliki termination rate paling tinggi dibandingkan kelompok lainnya
# sebenarnya, kelompok "20+ tahun" memiliki termination rate tertinggi, tetapi sample datanya hanya 4000, dibandingkan dengan kelompok lain yang samplenya sedikit lebih tinggi
