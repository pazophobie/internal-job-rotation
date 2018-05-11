import pandas as pd
import numpy as np
desired_width = 500
pd.set_option('display.width', desired_width)


""" Import Excel File"""
xl = pd.ExcelFile('participants_preferences.xlsx')


""" define dataframes """

df1_raw = xl.parse('Workers')  # workers
df1 = df1_raw.drop([0,1])
df1 = df1.reset_index()
df1 = df1.drop(['index'], 1)

df2_raw = xl.parse('Managers')  # managers<
df2 = df2_raw.drop([0])
df2 = df2.reset_index()
df2 = df2.drop(['index'], 1)

the_grid = xl.parse('Grid')  # the grid


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





""" What to print"""

print('grid outcome:',gsc_matching)
print(gsc_story)
print('The Grid is ', gsc_stable)
print(gsc_blocking_paris)


#print('The acoa is ', stability_test(workers,managers,df1,df2,da_adjusted))


#result = pd.concat([da_normal_worker_proposing, da_adjusted,grid_matching], axis=1, join_axes=[da_normal_worker_proposing.index])
#result = result.drop([0],1)
#result.columns = ['DA','Adjusted','Grid']

#print(result)


