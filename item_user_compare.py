import pandas as pd 
import numpy as np 
from sklearn.metrics import mean_squared_error
from math import sqrt 

def convert_to_binary_rating(df: pd.DataFrame):
    df.loc[df['rating']>3.5, 'rating'] = 1
    df.loc[df['rating']<3.5, 'rating'] = 0
    return df

def split_data_training (df:pd.DataFrame):
    df.loc[df['comment_date']=='#VALUE!', 'comment_date'] =  " Nov 20, 2019"
    df['comment_date'] = pd.to_datetime(df['comment_date'], format=' %b %d, %Y')
    idx = ['user']
    df1= df.sort_values('comment_date')
    group_by = df1.groupby(idx,as_index=False)
    df1 = df1.set_index(idx)
    df1['g_size'] = group_by.size()
    top_half = (group_by.cumcount() / df1.g_size.values).values < 0.7
    top = df1.loc[top_half].drop(['g_size','index'], axis=1).reset_index()
    return top

def split_data_testing (df:pd.DataFrame):
    df.loc[df['comment_date']=='#VALUE!', 'comment_date'] =  " Nov 20, 2019"
    df['comment_date'] = pd.to_datetime(df['comment_date'], format=' %b %d, %Y')
    idx = ['user']
    df1= df.sort_values('comment_date')
    group_by = df1.groupby(idx,as_index=False)
    df1 = df1.set_index(idx)
    df1['g_size'] = group_by.size()
    bottom_half = (group_by.cumcount() / df1.g_size.values).values >= 0.7
    bottom = df1.loc[bottom_half].drop(['g_size','index'], axis=1).reset_index()
    return bottom

def item_item (Ratings:pd.DataFrame, user:str):
    Mean = Ratings.groupby(['wine'], as_index = False, sort = False).mean().rename(columns = {'rating': 'rating_mean'})[['wine','rating_mean']]
    Ratings = pd.merge(Ratings,Mean,on = 'wine', how = 'left', sort = False)
    Ratings['rating_adjusted']= Ratings['rating']- Ratings['rating_mean']
    wine_data_all_append=pd.DataFrame()
    
    user_data=  Ratings[Ratings['user']!=user]
    distinct_wines=np.unique(user_data['wine'])
    i=1
    for wine in distinct_wines:
        
        if i%10==0:
            
            print (i , " out of ", len(distinct_wines))
        
        wine_data_all=pd.DataFrame()
        
        wine_data = Ratings[Ratings['wine']==wine]
        wine_data = wine_data[['user','wine','rating_adjusted']].drop_duplicates()
        wine_data=wine_data.rename(columns={'rating_adjusted':'rating_adjusted1'})
        wine_data=wine_data.rename(columns={'wine':'wineId1'})
        wine1_val=np.sqrt(np.sum(np.square(wine_data['rating_adjusted1']), axis=0))
        
        user_data1=  Ratings[Ratings['user']==user]
        distinct_wines1=np.unique(user_data1['wine'])
        
        for wine1 in distinct_wines1:
            
            wine_data1 = Ratings[Ratings['wine']==wine1]
            wine_data1 = wine_data1[['user','wine','rating_adjusted']].drop_duplicates()
            wine_data1=wine_data1.rename(columns={'rating_adjusted':'rating_adjusted2'})
            wine_data1=wine_data1.rename(columns={'wine':'wineId2'})
            wine2_val=np.sqrt(np.sum(np.square(wine_data1['rating_adjusted2']), axis=0))
            
            wine_data_merge = pd.merge(wine_data,wine_data1[['user','wineId2','rating_adjusted2']],on = 'user', how = 'inner', sort = False)
            
            wine_data_merge['vector_product']=(wine_data_merge['rating_adjusted1']*wine_data_merge['rating_adjusted2'])
    
    
            wine_data_merge= wine_data_merge.groupby(['wineId1','wineId2'], as_index = False, sort = False).sum()
    
            wine_data_merge['dot']=wine_data_merge['vector_product']/(wine1_val*wine2_val)
            
            wine_data_all = wine_data_all.append(wine_data_merge, ignore_index=True)
            
        
        wine_data_all=  wine_data_all[wine_data_all['dot']<1]
        wine_data_all = wine_data_all.sort_values(['dot'], ascending=False)
        wine_data_all = wine_data_all.head(20)
        
        wine_data_all_append = wine_data_all_append.append(wine_data_all, ignore_index=True)
        i=i+1
    wine_rating_all=pd.DataFrame()
    
    for wine in distinct_wines:
        wine_nbr=wine_data_all_append[wine_data_all_append['wineId1']== wine]
        wine_mean = Ratings[Ratings['wine']==wine]
        mean = wine_mean['rating'].mean()
        wine_nbr_dot = pd.merge(user_data1,wine_nbr[['dot','wineId2','wineId1']], how = 'inner',left_on='wine', right_on='wineId2', sort = False)
        wine_nbr_dot['wt_rating']=wine_nbr_dot['dot']*wine_nbr_dot['rating_adjusted']
        wine_nbr_dot['dot_abs']=wine_nbr_dot['dot'].abs()
        wine_nbr_dot= wine_nbr_dot.groupby(['wineId1'], as_index = False, sort = False).sum()[['wineId1','wt_rating','dot_abs']]
        wine_nbr_dot['Rating']=(wine_nbr_dot['wt_rating']/wine_nbr_dot['dot_abs'])+mean
        
        wine_rating_all = wine_rating_all.append(wine_nbr_dot, ignore_index=True)
        
    wine_rating_all = wine_rating_all.sort_values(['Rating'], ascending=False)
    return wine_rating_all

def user_user (Ratings:pd.DataFrame, user:str):
    Mean = Ratings.groupby(['wine'], as_index = False, sort = False).mean().rename(columns = {'rating': 'rating_mean'})[['wine','rating_mean']]
    Ratings = pd.merge(Ratings,Mean,on = 'wine', how = 'left', sort = False)
    Ratings['rating_adjusted']= Ratings['rating']- Ratings['rating_mean']
    distinct_users=np.unique(Ratings['user'])
    user_data_append=pd.DataFrame()
    user_data_all=pd.DataFrame()
        
    user1_data=  Ratings[Ratings['user']==user]
    user1_mean=user1_data['rating'].mean()
    user1_data=user1_data.rename(columns={'rating_adjusted':'rating_adjusted1'})
    user1_data=user1_data.rename(columns={'user':'userId1'})
    user1_val=np.sqrt(np.sum(np.square(user1_data['rating_adjusted1']), axis=0))
    
    
    distinct_wine=np.unique(Ratings['wine'])
    
    i=1
    
    for wine in distinct_wine:
    
        item_user =  Ratings[Ratings['wine']==wine]
    
        distinct_users1=np.unique(item_user['user'])
        
        j=1
        
        for user2 in distinct_users1:
    
            if j%200==0:
    
                print (j ," out of ", len(distinct_users1), i , " out of ", len(distinct_wine))
    
            user2_data=  Ratings[Ratings['user']==user2]
            user2_data=user2_data.rename(columns={'rating_adjusted':'rating_adjusted2'})
            user2_data=user2_data.rename(columns={'user':'userId2'})
            user2_val=np.sqrt(np.sum(np.square(user2_data['rating_adjusted2']), axis=0))
    
            user_data = pd.merge(user1_data,user2_data[['rating_adjusted2','wine','userId2']],on = 'wine', how = 'inner', sort = False)
            user_data['vector_product']=(user_data['rating_adjusted1']*user_data['rating_adjusted2'])
    
    
            user_data= user_data.groupby(['userId1','userId2'], as_index = False, sort = False).sum()
    
            user_data['dot']=user_data['vector_product']/(user1_val*user2_val)
    
    
            user_data_all = user_data_all.append(user_data, ignore_index=True)
    
            j=j+1
    
        user_data_all=  user_data_all[user_data_all['dot']<1]
        user_data_all = user_data_all.sort_values(['dot'], ascending=False)
        user_data_all = user_data_all.head(30) # comapre neighbours hyper parameters
        user_data_all['wine']=wine
        user_data_append = user_data_append.append(user_data_all, ignore_index=True)
        i=i+1

    User_dot_adj_rating_all=pd.DataFrame()
    
    distinct_wines=np.unique(Ratings['wine'])
    
    j=1
    for wine in distinct_wines:
        
        user_data_append_wine=user_data_append[user_data_append['wine']==wine]
        User_dot_adj_rating = pd.merge(Ratings,user_data_append_wine[['dot','userId2','userId1']], how = 'inner',left_on='user', right_on='userId2', sort = False)
        
        if j%200==0:
        
            print (j , " out of ", len(distinct_wines))
            
        User_dot_adj_rating1=User_dot_adj_rating[User_dot_adj_rating['wine']==wine]
        
        if len(np.unique(User_dot_adj_rating1['user']))>=2:
            
            User_dot_adj_rating1['wt_rating']=User_dot_adj_rating1['dot']*User_dot_adj_rating1['rating_adjusted']
            
            User_dot_adj_rating1['dot_abs']=User_dot_adj_rating1['dot'].abs()
            User_dot_adj_rating1= User_dot_adj_rating1.groupby(['userId1'], as_index = False, sort = False).sum()[['userId1','wt_rating','dot_abs']]
            User_dot_adj_rating1['Rating']=(User_dot_adj_rating1['wt_rating']/User_dot_adj_rating1['dot_abs'])+user1_mean
            User_dot_adj_rating1['wine']=wine
            User_dot_adj_rating1 = User_dot_adj_rating1.drop(['wt_rating', 'dot_abs'], axis=1)
            
            User_dot_adj_rating_all = User_dot_adj_rating_all.append(User_dot_adj_rating1, ignore_index=True)
        
        j=j+1
            
    User_dot_adj_rating_all = User_dot_adj_rating_all.sort_values(['Rating'], ascending=False)
    return User_dot_adj_rating_all

def records_of_one_user(name:str, df: pd.DataFrame):
    df1 = df[(df['user'] == name )]
    return df1

def RMSE_evaluation_single_user (test_data: pd.DataFrame, recc_result: pd.DataFrame, method:str):
    if (method == 'user_user'):
        test_data.set_index('wine', inplace=True)
        recc_result.set_index('wine', inplace=True)
        combine = pd.merge(test_data,recc_result, left_on='wine',right_on='wine', how='left')
        simple_combine=combine[['user','rating','Rating']]
        simple_combine = simple_combine.dropna(thresh=3)
        rating = (simple_combine['rating']).tolist()
        est_rating = (simple_combine['Rating']).tolist()
        rms = sqrt(mean_squared_error(rating, est_rating))
    elif (method == 'item_item'):
        test_data.set_index('wine', inplace=True)
        recc_result.set_index('wineId1', inplace=True)
        combine = pd.concat([test_data, recc_result], axis = 1)
        simple_combine=combine[['user','rating','Rating']]
        simple_combine = simple_combine.dropna(thresh=3)
        rating = (simple_combine['rating']).tolist()
        est_rating = (simple_combine['Rating']).tolist()
        rms = sqrt(mean_squared_error(rating, est_rating))
    return rms

def RMSE_evaluation_multi_user (training:pd.DataFrame, testing:pd.DataFrame, user_list:list, method:str):
    rms_list = []
    for user in user_list:
        test_data_user = testing.loc[testing['user'] == user]
        if (method == 'user_user'):
            user_result = user_user(training, user)
            try:
                rms = RMSE_evaluation_single_user(test_data_user, user_result,method)
                print(rms)
                rms_list.append(rms)
            except:
                return rms_list
        elif (method == 'item_item'):
            item_result = item_item(training, user)
            rms = RMSE_evaluation_single_user(test_data_user, item_result,method)
            print(rms)
            rms_list.append(rms)
        else:
            rms_list = []
    return rms_list

if __name__ == "__main__":
    df = pd.read_csv('ratings_copy.csv', sep=',', names=['index', 'wine','user','unfiltered_date','rating','comment_date'])
    df = df[df.groupby('user')['user'].transform('size') > 2]
    training = split_data_training(df)
    user = 'Vivino User'
    user_list = ['Vivino User','Mike Benson','Mark Gudgel', 'WhatAreYouDoingThisSunday', 'Rock and Roll Wino', 'David',
        'Sommelier Claudia Arce', 'Rocky', 'Sam', 'Jesper Moonen', 'Gretchen Bilhardt', 'Doug Walker']
    testing = split_data_testing(df)
    #test_data_user = testing.loc[testing['user'] == user]
    #item_result = item_item(training, user)
    print(RMSE_evaluation_multi_user(training, testing, user_list,'user_user'))
    
    #user_result =user_user(training, user)
    #print(RMSE_evaluation_single_user(testing, user_result,'user_user'))
    
    
    