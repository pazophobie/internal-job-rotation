import numpy as np
import pandas as pd




def df_pairs_matrix(workers,managers,df1,df2):

    def rank_from___of___(a, b):
        if a in workers:
            if not df1.loc[df1[a] == b].empty:
                return int(df1.loc[df1[a] == b]['Rank'])
            else:
                return np.nan

        elif a in managers:
            if not df2.loc[df2[a] == b].empty:
                return int(df2.loc[df2[a] == b]['Rank'])
            else:
                return np.nan

    df_pairs = pd.DataFrame(index=workers, columns=managers)

    for w in workers:
        for m in managers:
            if m == managers[0]:
                if not np.isnan(rank_from___of___(w,m)) and not np.isnan(rank_from___of___(m,w)):
                    df_pairs.loc[w][m] = ''.join(['&[',str(rank_from___of___(w,m)),':', str(rank_from___of___(m,w)),']', '&'] )
                elif np.isnan(rank_from___of___(w,m)) and not np.isnan(rank_from___of___(m,w)):
                    df_pairs.loc[w][m] = ''.join(['&[-:', str(rank_from___of___(m, w)), ']', '&'])
                elif not np.isnan(rank_from___of___(w,m)) and  np.isnan(rank_from___of___(m,w)):
                    df_pairs.loc[w][m] = ''.join(['&[',str(rank_from___of___(w,m)),':-]', '&'])
                else:
                    df_pairs.loc[w][m] = ''.join(['& &'])

            elif m == managers[-1]:
                if not np.isnan(rank_from___of___(w,m)) and not np.isnan(rank_from___of___(m,w)):
                    df_pairs.loc[w][m] = ''.join(['[',str(rank_from___of___(w,m)),':', str(rank_from___of___(m,w)),']', '\\\\'] )
                elif np.isnan(rank_from___of___(w,m)) and not np.isnan(rank_from___of___(m,w)):
                    df_pairs.loc[w][m] = ''.join(['[-:', str(rank_from___of___(m, w)), ']', '\\\\'])
                elif not np.isnan(rank_from___of___(w,m)) and  np.isnan(rank_from___of___(m,w)):
                    df_pairs.loc[w][m] = ''.join(['[',str(rank_from___of___(w,m)),':-]', '\\\\'])
                else:
                    df_pairs.loc[w][m] = ''.join([' \\\\'])

            else:
                if not np.isnan(rank_from___of___(w, m)) and not np.isnan(rank_from___of___(m, w)):
                    df_pairs.loc[w][m] = ''.join(['[', str(rank_from___of___(w, m)), ':', str(rank_from___of___(m, w)), ']', '&'])
                elif np.isnan(rank_from___of___(w, m)) and not np.isnan(rank_from___of___(m, w)):
                    df_pairs.loc[w][m] = ''.join(['[-:', str(rank_from___of___(m, w)), ']', '&'])
                elif not np.isnan(rank_from___of___(w, m)) and np.isnan(rank_from___of___(m, w)):
                    df_pairs.loc[w][m] = ''.join(['[', str(rank_from___of___(w, m)), ':-]', '&'])
                else:
                    df_pairs.loc[w][m] = ''.join([' &'])

    return df_pairs

def total_grid(df3):
    print(''.join( [str(1), ' & ', str(df3.loc[0]['participant']), ' & ', str(df3.loc[0]['manager']), '&& $\\vdots$ &  $\\vdots$ &  $\\vdots$ \\\\']))

    for i in range(1, 32):
        j = i + 31
        print(''.join([ str(i+1), ' & ', str(df3.loc[i]['participant']), ' & ',str(df3.loc[i]['manager']), '&&', str(j+1), ' & ', str(df3.loc[j]['participant']), ' & ',str(df3.loc[j]['manager']), ' \\\\' ]))

    print(''.join([' $\\vdots$ &  $\\vdots$ &  $\\vdots$ &&&&  \\\\']))