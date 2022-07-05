# OA3801 (Comp Methods II)
# Naval Postgraduate School
# LT Jonathan Shepherd 
# Email: Jonathan.Shepherd@nps.edu
import pandas as pd
import os.path
import numpy as np
import glob
import os
import sys
import shutil
from operator import itemgetter 


def calc_pop(dirname, k):
    

 
    
    path = dirname # This will be an input
    file = os.path.abspath(path) # provides the file path for 'popdata' no matter location. 
    os.chdir(file) # Changes file path to popdata
#     os.getcwd() # Ensures directory.

    state_folder = glob.glob('./*.csv.txt*') # looks for all .csv.txt in the dir
    # state_folder

    
    
    state_folder_dfs = [] # Putting the folders in a list allows me to bunch (append) the files into one dataframe
    for states in state_folder:
    #     print(states)
        state_folder_dfs.append(pd.read_csv(states,encoding='latin-1')) # I got a ''utf-8' codec can't decode byte 0xf1 in position 5: invalid continuation byte' error. So i needed to change the encoding to 'latin-1' in order for the files to be read
    data_frame = pd.concat(state_folder_dfs, ignore_index=True) #ignore_index forces a 1-n index 

#     data_frame.info()
    

    pop_2013 = data_frame.loc[:,'POPESTIMATE2013'] # Gives me a series of int for 2013
    pop_2010 = data_frame.loc[:,'POPESTIMATE2010'] # Gives me a series of int for 2010

    diff = pop_2013 - pop_2010
    diffpct = diff / pop_2010

    #Adding another two cols to my data frame
    data_frame['DIFF_2010_2013'] = diff
    data_frame['DIFFPCT_2010_2013'] = diffpct
    
    


    # Question 2

    state_pop = data_frame.loc[:,'SUMLEV']==40
    df1 = data_frame.loc[state_pop,['NAME','DIFF_2010_2013']]
    df1 = df1.sort_values(by='DIFF_2010_2013',ascending=False)
    print('Greastest Increase')
    print(df1.head(k))
    print('')

    #Decreasing order
    print('Greastest Decrease')
    bottom_k = df1.loc[state_pop,:].tail(k)
    bottom_k = bottom_k.sort_values(by='DIFF_2010_2013',ascending=True)
    print(bottom_k)

    print('')
    df1 = data_frame.loc[state_pop,['NAME','DIFFPCT_2010_2013']]
    df1 = df1.sort_values(by='DIFFPCT_2010_2013',ascending=False)
    print('Greastest Percent Increase')
    print(df1.head(k))
    print('')

    #Decreasing order
    print('Greastest Decrease')
    bottom_k = df1.loc[state_pop,:].tail(k)
    bottom_k = bottom_k.sort_values(by='DIFFPCT_2010_2013',ascending=True)
    print(bottom_k)

    print("")
    print('******************************************')
    print("")
    
       
    
    # Question 1 and 3
    States_1 = data_frame.groupby('STATE') 
    for number, data_1 in States_1:
        data_1 = data_1.sort_values(by = 'DIFF_2010_2013',ascending=False)

        state_pop = data_1.loc[:,'SUMLEV']==40
        county_pop = data_1.loc[:,'SUMLEV'] == 50
    #     print(pop_2010)


    #     print(diff)
        state_name = data_1.loc[state_pop,'NAME']
        county_name = data_1.loc[county_pop, 'NAME']
    #    print(state_name)
        print(state_name.values[0])
        print('Total population change:', data_1.loc[state_pop, 'DIFF_2010_2013'].values[0])       # Returned was a series type. used values to just get the data    print(type(diff))
    #    for x in diff:
    #        print(x)

        print()
        print("Top %d Growth for %s" % (k, state_name.values[0]) )
        top3 = data_1.loc[county_pop,:].head(k)
        print(top3.loc[:, ['NAME','DIFF_2010_2013']])

        print()
        print("Bottom %d Growth for %s" % (k, state_name.values[0]) )
        bottom3 = data_1.loc[county_pop,:].tail(k)
        bottom3= bottom3.sort_values(by='DIFF_2010_2013',ascending=True)
        print(bottom3.loc[:, ['NAME','DIFF_2010_2013']])


        '''County'''
        data_1 = data_1.sort_values(by = 'DIFFPCT_2010_2013',ascending=False)
        county_pop = data_1.loc[:,'SUMLEV'] == 50


        print()
        print("Top %d Percent Growth for %s" % (k, state_name.values[0]) )
        top3 = data_1.loc[county_pop,:].head(k)
        print(top3.loc[:, ['NAME','DIFFPCT_2010_2013']])


        print()
        print("Bottom %d Percent Growth for %s" % (k, state_name.values[0]) )
        bottom3 = data_1.loc[county_pop,:].tail(k)
        bottom3 = bottom3.sort_values(by='DIFFPCT_2010_2013',ascending=True)
        print(bottom3.loc[:, ['NAME','DIFFPCT_2010_2013']])
        print("")
        print('******************************************')
        print("")
    #    break





    

# Do not change anything below this line!
if __name__ == '__main__':
    if len(sys.argv) != 3:
        msg = "USAGE: python %s [directory_name] [k]" % os.path.basename(sys.argv[0])
        sys.exit(msg)

    dirname = sys.argv[1]
    bestk = int(sys.argv[2])

    calc_pop(dirname, bestk)

    print('normal completion.')