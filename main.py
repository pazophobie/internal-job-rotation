import pandas as pd
import numpy as np
desired_width = 500
pd.set_option('display.width', desired_width)


""" Import Excel File"""
xl = pd.ExcelFile('excelsheets/pref_part_without_initial_match.xlsx')


""" define dataframes and make them workable... """
df1_raw = xl.parse('Sheet1')  # workers
df1 = df1_raw.drop([0,1])
df1 = df1.reset_index()
df1 = df1.drop(['index'], 1)

df2_raw = xl.parse('Sheet2')  # managers<
df2 = df2_raw.drop([0])
df2 = df2.reset_index()
df2 = df2.drop(['index'], 1)

the_grid = xl.parse('Sheet3')  # the grid


""" Create lists of all participants and all managers"""
workers = list(df1.columns.values)
del workers[0]
managers = list(df2.columns.values)
del managers[0]


"""Create list of Volunteers"""
volunteers = []
for w in workers:
    if df1_raw.loc[1][w] == 'yes':
        volunteers.append(w)


#print(df1)


"""DA_NORMAL"""
from DA_normal import DA_normal
da_normal_worker_proposing = DA_normal(workers,managers,df1,df2)
#da_normal_manager_proposing = DA_normal(managers,workers,df2,df1)
#print(da_normal_worker_proposing)



"""DA ADJUSTED"""
from DA_adjusted import DA_adjusted
da_adjusted = DA_adjusted(workers,managers,df1,df2,df1_raw,volunteers)
#print(da_adjusted)


"""THE GRID"""
from the_grid_algo import the_grid_algo
grid_matching, grid_story = the_grid_algo(workers,managers,df1,df2,the_grid)




"""Is the outcome stable?"""
from stability_test import stability_test
grid_stable, blocking_paris_grid = stability_test(workers,managers,df1,df2,grid_matching)





""" What to print"""

print('grid outcome:',grid_matching)
print(grid_story)
print('The Grid is ', grid_stable)
print(blocking_paris_grid)


#print('The Adjusted DA is ', stability_test(workers,managers,df1,df2,da_adjusted))


#result = pd.concat([da_normal_worker_proposing, da_adjusted,grid_matching], axis=1, join_axes=[da_normal_worker_proposing.index])
#result = result.drop([0],1)
#result.columns = ['DA','Adjusted','Grid']

#print(result)





''' LATEX OUTPUT'''

'''grid pairing matrix'''

""" Pairing Matrix"""
from latex_output import df_pairs_matrix
from latex_output import total_grid
print(df_pairs_matrix(workers,managers,df1,df2))
#total_grid(the_grid)

