import pandas as pd
import numpy as np



def stability_test(workers,managers,df1,df2,df_matching_grid):

    matched_workers = df_matching_grid[0].tolist()
    matched_managers= df_matching_grid[1].tolist()

    df_blockingpairs = pd.DataFrame(index=workers, columns=managers)  # define matrix for blocking pairs


    def rank_from___of___(a, b):
        if a in workers:
            if not df1.loc[df1[a] == b].empty:
                return float(df1.loc[df1[a] == b]['Rank'])
            else:
                return np.nan
        elif a in managers:
            if not df2.loc[df2[a] == b].empty:
                return float(df2.loc[df2[a] == b]['Rank'])
            else:
                return np.nan


    def worker__s_match_rank(p):
        x = df_matching_grid.loc[df_matching_grid[0] == p][1].values[0]
        return rank_from___of___(p,x)


    def manager__s_match_rank(m):
        x = df_matching_grid.loc[df_matching_grid[1] == m][0].values[0]
        return rank_from___of___(m,x)

    

    n = 0
    for p in workers:
        for m in managers:
            if not pd.isnull(rank_from___of___(p,m)) and not pd.isnull(rank_from___of___(m,p)):  # both sides find each other acceptable

                if p in matched_workers and m in matched_managers:  # both have a match


                    if rank_from___of___(p,m) < worker__s_match_rank(p) and rank_from___of___(m,p) < manager__s_match_rank(m):
                        n =+1
                        df_blockingpairs.loc[p][m] = 'blocks'

                elif p in matched_workers:  # worker has a match

                    if rank_from___of___(p,m) < worker__s_match_rank(p):
                        n =+1
                        df_blockingpairs.loc[p][m] = 'blocks'

                elif m in matched_managers:  # manager has a match
                    #print(df_pref_managers.loc[p][m], managers_match_rank(m))
                    if rank_from___of___(m,p) < manager__s_match_rank(m):
                        n =+1
                        df_blockingpairs.loc[p][m] = 'blocks'

    if n > 0:

        #return df_blockingpairs
        return 'UNstable', df_blockingpairs
    else:
        return 'stable', df_blockingpairs

