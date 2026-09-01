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

# data['job_title'].value_counts().head(10).plot(
#     kind='bar',
#     figsize=(10, 5),
#     title='Top 10 Job Titles'
# )

# plt.xlabel('Job Title')
# plt.ylabel('Number of Records')
# plt.xticks(rotation=45, ha='right')
# plt.show()
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

print('=' * 50)
print(data['STATUS_YEAR'].value_counts())
print("=" * 50)

print("=" * 50)
conti_table5 = pd.crosstab(data['STATUS_YEAR'], data['STATUS'])
print(conti_table5)

print("=" * 50)
print(data.sort_values(['EmployeeID','STATUS_YEAR'])[
    ['EmployeeID', 'STATUS_YEAR', 'STATUS']
].head(30))
print("=" * 50)

print("=" * 50)
terminated_employee = data[data['STATUS'] == 'TERMINATED']

print(terminated_employee.sort_values(
    ['EmployeeID','STATUS_YEAR']
)[['EmployeeID', 'STATUS_YEAR', 'STATUS']].head(30))
print("=" * 50)

terminated = data[data['STATUS'] == 'TERMINATED']
previous_pairs = []

for _, row in terminated.iterrows():
    employee_id = row['EmployeeID']
    termination_year = row['STATUS_YEAR']

    previous_year = data[
        (data['EmployeeID'] == employee_id) &
        (data['STATUS_YEAR'] == termination_year - 1)
    ]

    if not previous_year.empty:
        previous_pairs.append((employee_id, termination_year))

previous_pairs = set(previous_pairs)

# print(pd.Series(previous_pairs).value_counts())

# 1338 employee memiliki pola ACTIVE (tahun T) -> TERMINATED (tahun T+1)

active = data[data['STATUS'] == 'ACTIVE']
next_pairs = []

for _, row in active.iterrows():
    employee_id = row['EmployeeID']
    active_year = row['STATUS_YEAR']

    next_year = data[
        (data['EmployeeID'] == employee_id) &
        (data['STATUS_YEAR'] == active_year + 1)
    ]

    if not next_year.empty:
        status = next_year['STATUS'].iloc[0]

        if status == 'TERMINATED':
            next_pairs.append((employee_id, active_year + 1))

next_pairs = set(next_pairs)

missing_pairs = previous_pairs - next_pairs
print(missing_pairs)

# print(pd.Series(next_status).value_counts())

print(len(previous_pairs))
print(len(next_pairs))

# terdapat selisih 4 employee pada employee yang ACTIVE (tahun t) --> TERMINATED (tahun T + 1)
# employee id : 3008, 3401, 7007, 7023

missing_employee_id = [employee_id for employee_id, year in missing_pairs]

missing = data[data['EmployeeID'].isin(missing_employee_id)]

print(missing[['EmployeeID', 'STATUS', 'STATUS_YEAR']].sort_values(
    ['EmployeeID', 'STATUS_YEAR']
))

# setelah ditelusuri data tiap employee, ternyata terdapat duplicate data employee pada tahun yang sama.
# contoh : employee ID "3008" muncul 2x STATUS_YEAR 2007

duplicates = missing[
    missing.duplicated(
        subset=['EmployeeID', 'STATUS_YEAR'],
        keep=False
    )
]

# print(missing[missing['EmployeeID'] == 7023].T.to_string())

print(data['recorddate_key'].value_counts().head(30))
print(data['recorddate_key'].nunique())

print("=" * 50)
conti_table6 = pd.crosstab(data['recorddate_key'], data['STATUS'])
print(conti_table6)
print("=" * 50)

terminated = data[data['STATUS'] == 'TERMINATED']

print(
    terminated[
        terminated['recorddate_key'].str.startswith('12/31')
        ][['EmployeeID', 'recorddate_key', 'STATUS']]
)

active = data[data['STATUS'] == 'ACTIVE']

print(
    active[
        ~active['recorddate_key'].str.startswith('12/31')
    ][['EmployeeID', 'recorddate_key', 'STATUS']]
)

# record date pada waktu tertentu (awal/tengah tahun) merupakan catatan ketika employee mengalami termination
# record date pada waktu akhir tahun menunjukkan data employee yang masih 'ACTIVE'

# print("=" * 50)
# print(data['STATUS'].value_counts())
# print("=" * 50)

# print("=" * 50)
prediction_point = data[
    (data['STATUS'] == 'ACTIVE') & 
    (data['recorddate_key'].str.startswith('12/31'))
]

# print(prediction_point[['EmployeeID', 'recorddate_key', 'STATUS']])
# print("=" * 50)

# print("=" * 50)
# next_status = []

# for _, row in prediction_point.iterrows():
#     employee_id = row['EmployeeID']
#     prediction_year = row['STATUS_YEAR']

#     next_year = data[
#         (data['EmployeeID'] == employee_id) &
#         (data['STATUS_YEAR'] == prediction_year + 1)
#     ]

#     if not next_year.empty: 
#         status = next_year['STATUS'].iloc[0]
#         next_status.append((employee_id, prediction_year, status))

# print(next_status)
# print("=" * 50)

print("=" * 50)
prediction_point = prediction_point.copy()

prediction_point['target_year'] = prediction_point['STATUS_YEAR'] + 1
next_data = data[['EmployeeID', 'STATUS_YEAR', 'STATUS']]

result = prediction_point.merge(
    next_data,
    left_on=['EmployeeID', 'target_year'],
    right_on=['EmployeeID', 'STATUS_YEAR'],
    how='left'
)

print(result)

print("=" * 50)