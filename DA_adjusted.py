import pandas as pd
import numpy as np

def DA_adjusted(workers,managers,df1,df2,df1_raw,volunteers):


    """ create a data frame for the final matchings """
    df_matching_DA = pd.DataFrame(index=workers, columns=[0, 1])
    for s in workers:
        df_matching_DA.loc[s][0] = s

    """  create lists in which unmatched participants and managers will be put into during the algorithm """
    matched_workers = []
    matched_managers = []
    unmatched_workers = []
    unmatched_managers = []
    unmatched_workers.extend(workers)
    unmatched_managers.extend(managers)

    """  create empty row and add to df1 """

    df_proposer_len_index = len(df1.index)
    emtpy_row = pd.DataFrame(index=[df_proposer_len_index], columns=df1.columns)
    df1 = df1.append(emtpy_row)
    df1.loc[4]['Rank'] = df_proposer_len_index+1

    """  create empty row and add to df2"""

    df2_len_index = len(df2.index)
    emtpy_row = pd.DataFrame(index=[df2_len_index], columns=df2.columns)
    df2 = df2.append(emtpy_row)
    df2.loc[df2_len_index][0] = df2_len_index +1

    """For df2 move all entries down for managers with volunteer initial match"""
    """First element will become initial match"""

    for n in volunteers:
        initial_job = df1_raw.loc[0][n]
        for i in reversed(range(1, df2_len_index)):
            j = i - 1
            df2.loc[i][initial_job] = df2.loc[j][initial_job]
        df2.loc[0][initial_job] = n




    """  Create functions for the algorithm"""


    def A(p):  # move everything one up for workers!
        for i in range(0, df_proposer_len_index):
            j = i + 1
            df1.at[i, p] = df1.loc[j][p]


    def B(m):
        unmatched_managers.remove(m)
        matched_managers.append(m)


    def C(m, p):
        unmatched_workers.remove(p)
        matched_workers.append(p)
        df_matching_DA.loc[p][1] = m


    def D(x):
        matched_workers.remove(x)
        unmatched_workers.append(x)
        df_matching_DA.loc[x][1] = 'No match (Lost his match)'


    def current_match_of_accepter(m):
        q = ''.join(df_matching_DA.loc[df_matching_DA[1] == m][0].values)
        return q

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





    """" DA algorithm """

    while True:
        for p in workers:

            if not pd.isnull(df1.loc[0][p]):  # p does not want to choose himself..
                m = (df1.loc[0][p])  # p will propose to m

                if pd.isnull(rank_from___of___(m,p)):
                    A(p)

                else:
                    if m in unmatched_managers:
                        # print('Its a match!')
                        B(m)
                        C(m, p)

                    elif m is not df_matching_DA.loc[p][1]:
                        q = current_match_of_accepter(m)
                        if rank_from___of___(m,p) > rank_from___of___(m,q):
                            A(p)
                        else:
                            C(m, p)
                            D(q)

        if all(pd.isnull(df1.loc[0][p]) for p in unmatched_workers):
            break

    """ Replace all NaN in df_matching_DA since they were never accepted"""
    df_matching_DA = df_matching_DA.replace(np.nan, 'NaN.', regex=True)

    """ Add the DA matchings to the total matchings"""

    return df_matching_DA

