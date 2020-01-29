import pandas as pd 
import numpy as np 
from sklearn.metrics import mean_squared_error
from math import sqrt 
from sklearn.metrics.pairwise import pairwise_distances 
import matplotlib.pyplot as plt

def split_data_training (df:pd.DataFrame):
    df.loc[df['comment_date']=='#VALUE!', 'comment_date'] =  " Nov 20, 2019"
    df['comment_date'] = pd.to_datetime(df['comment_date'], format=' %b %d, %Y')
    idx = ['user_id']
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
    idx = ['user_id']
    df1= df.sort_values('comment_date')
    group_by = df1.groupby(idx,as_index=False)
    df1 = df1.set_index(idx)
    df1['g_size'] = group_by.size()
    bottom_half = (group_by.cumcount() / df1.g_size.values).values >= 0.7
    bottom = df1.loc[bottom_half].drop(['g_size','index'], axis=1).reset_index()
    return bottom

def model (ratings: pd.DataFrame, type: str):
    data_matrix = ratings.pivot_table(index='user_id', columns='wine_id', values='rating')
    data_matrix = data_matrix.fillna(0)
    user_similarity = pairwise_distances(data_matrix, metric='cosine')
    item_similarity = pairwise_distances(data_matrix.T, metric='cosine')
    if type == 'user':
        similarity = user_similarity
        mean_user_rating = data_matrix.mean(axis=1)
        #We use np.newaxis so that mean_user_rating has same format as ratings
        ratings_diff = (data_matrix - mean_user_rating[:, np.newaxis])
        pred = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array([np.abs(similarity).sum(axis=1)]).T
    elif type == 'item':
        similarity = item_similarity
        pred = data_matrix.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])
    return pred

def percision_recall_at_k (actual:list, prediction:list, k:int):
    return 

if __name__ == "__main__":
    df = pd.read_csv('rating600.csv', sep=',', names=['index', 'wine_id','user_id','unfiltered_date','rating','comment_date'])
    #df= df[:30000]
    print(len((df['user_id'].drop_duplicates()).to_list()))
    '''df = df[df.groupby('user_id')['user_id'].transform('size') > 1]
    training = split_data_training(df)
    #print(model(training,'user'))
    score_matrix = model(training,'user')
    org_rating = training.pivot_table(index='user_id', columns='wine_id', values='rating')
    org_rating  = (org_rating.fillna(0)).as_matrix()
    rmse = sqrt((np.square(score_matrix - org_rating)).mean(axis=None))
    print(rmse)'''
    '''wine_feature = pd.read_csv('winefeature.csv', sep=',', names=['index', 'wine_id','region','country','type','winery','grape'])
    
    bycountry = wine_feature[['region', 'wine_id']].groupby('winery').count()
    plt.pie(bycountry.iloc[:,0].to_list(), labels=bycountry.index.to_list())
    plt.title('Classification of Wine by Winery')
    plt.axis('equal')
    plt.show()'''
    ##############
    '''data = [0,1,2,3,4]
    user = [0.5270,	0.6914,	0.8042,	0.8523,	0.9387]
    item = [0.5268,	0.6936,	0.8123,	0.8645,	0.9563]
    line1, = plt.plot(data, user, label="User-User", linestyle='--')
    line2, = plt.plot(data, item, label="Item-Item", linewidth=1)

    # Create a legend for the first line.
    first_legend = plt.legend(handles=[line1], loc='upper right')

    # Add the legend manually to the current Axes.
    ax = plt.gca().add_artist(first_legend)

    # Create another legend for the second line.
    plt.legend(handles=[line2], loc='lower right')
    plt.title("RMSE vs. Number of Review Threshold")

    plt.show()'''
    ###############
    '''ratings = pd.DataFrame(df.groupby('user_id')['rating'].mean())
    ratings['number_of_ratings'] = df.groupby('user_id')['rating'].count()
    x = ratings['number_of_ratings'].to_list()
    #print(ratings.sort_values(by=['number_of_ratings']))
    num_bins = 100
    arr = plt.hist(x, num_bins, facecolor='blue', alpha=0.5)
    for i in range(num_bins):
        if(arr[0][i] != 0):
            plt.text(arr[1][i],arr[0][i],str(arr[0][i]))
    plt.title("Number of Reviews Per User Distribution")
    plt.xlabel("number of reviews")
    plt.ylabel("count of reviewers")
    plt.show()'''
    '''ratings = pd.DataFrame(df.groupby('user_id')['rating'].mean())
    ratings['number_of_ratings'] = df.groupby('user_id')['rating'].count()
    x = ratings['number_of_ratings'].to_list()
    y = ratings['rating'].to_list()
    plt.scatter(x,y)
    plt.xlabel("number of ratings")
    plt.ylabel("average rating")
    plt.title("Rating Average vs. Number of Ratings")
    plt.show()'''

    


    