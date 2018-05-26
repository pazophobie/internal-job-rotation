import pandas as pd
import numpy as np
from openpyxl import load_workbook

desired_width = 500
pd.set_option('display.width', desired_width)


""" Import Excel File"""
main_excel_file = 'participants_preferences.xlsx'
xl = pd.ExcelFile(main_excel_file)


""" define dataframes """

df1_raw = xl.parse('Workers')  # workers
df1 = df1_raw.drop([0,1])
df1 = df1.reset_index()
df1 = df1.drop(['index'], 1)
df1 = df1.loc[:, ~df1.columns.str.contains('^Unnamed')]

df2_raw = xl.parse('Managers')  # managers<
df2 = df2_raw.drop([0])
df2 = df2.reset_index()
df2 = df2.drop(['index'], 1)
df2 = df2.loc[:, ~df2.columns.str.contains('^Unnamed')]


the_grid = xl.parse('The Grid')  # the grid


""" Create lists of all workers and all managers"""

workers = list(df1.columns.values)
del workers[0]
managers = list(df2.columns.values)
del managers[0]


"""Create list of Volunteers"""
volunteers = []
for w in workers:
    if df1_raw.loc[1][w] == 'yes':
        volunteers.append(w)



"""COA"""
from coa import coa
coa = coa(workers,managers,df1,df2)
#coa_normal_manager_proposing = coa_normal(managers,workers,df2,df1)

"""ACOA"""
from acoa import acoa
acoa = acoa(workers,managers,df1,df2,df1_raw,volunteers)

"""GSC Algorithm"""
from gsc_algorithm import gsc_algorithm
gsc_matching, gsc_story = gsc_algorithm(workers,managers,df1,df2,the_grid)


"""Is the outcome stable?"""
from stability_test import stability_test
gsc_stable, gsc_blocking_paris = stability_test(workers,managers,df1,df2,gsc_matching)



"""Combining Algorithms"""

result = pd.concat([gsc_matching, coa, acoa], axis=1, join_axes=[coa.index])
result = result.drop([0],1)
result.columns = ['GSC','COA','ACOA']

####################################
########""" Output """##############
####################################




print('\n The results of the three different alorithms: \n \n ', result)


print('\n The GSC mechanism outcome is', gsc_stable, '\n \n','The blocking pairs are: \n', gsc_blocking_paris)
print(gsc_story)

