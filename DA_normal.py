import pandas as pd
import numpy as np




def DA_normal(workers,managers,df1,df2):

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

    """  create empty row and add to df1' """

    df_workers_len_index = len(df1.index)
    emtpy_row = pd.DataFrame(index=[df_workers_len_index], columns=df1.columns)
    df1 = df1.append(emtpy_row)

    """  Create functions for the algorithm"""


    def A(p):  # move everything one up!
        for i in range(0, df_workers_len_index):
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


    story = pd.DataFrame(index=[(0)], columns=[(0)])
    story_line = pd.DataFrame(index=[(0)], columns=[(0)])




    """" DA algorithm """

    while True:



        for p in workers :
            if p in unmatched_workers:
                if not pd.isnull(df1.loc[0][p]):  # p does not want to choose himself..
                    m = (df1.loc[0][p])  # p will propose to m

                    story_line[0] = ''.join([p, ' proposes to ', m])
                    story = story.append(story_line)

                    if pd.isnull(rank_from___of___(m,p)):
                        A(p)

                        story_line[0] = ''.join([m, ' finds ', p, ' unacceptable'])
                        story = story.append(story_line)

                    else:
                        if m in unmatched_managers:
                            # print('Its a match!')
                            B(m)
                            C(m, p)

                            story_line[0] = ''.join([m, ' currently holds no contract and holds ', p])
                            story = story.append(story_line)

                        elif m is not df_matching_DA.loc[p][1]:
                            q = current_match_of_accepter(m)
                            if rank_from___of___(m,p) > rank_from___of___(m,q):
                                A(p)

                                story_line[0] = ''.join([m, ' is already matched. Rejects ', p])
                                story = story.append(story_line)
                            else:
                                C(m, p)
                                D(q)

                                story_line[0] = ''.join([m, ' is already matched to ',q,'. Accepts ', p,'. Drops ',q])
                                story = story.append(story_line)


        if all(pd.isnull(df1.loc[0][p]) for p in unmatched_workers):
            break

    """ Replace all NaN in df_matching_DA since they were never accepted"""
    df_matching_DA = df_matching_DA.replace(np.nan, 'NaN.', regex=True)

    """ Add the DA matchings to the total matchings"""

    story = story.reset_index()
    story = story.drop(['index'], 1)
    return df_matching_DA
    
