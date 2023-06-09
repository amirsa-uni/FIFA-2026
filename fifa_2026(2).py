

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import accuracy_score
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import math
import warnings
warnings.filterwarnings('ignore')

ListOfYear = []
for i in range(1930,1939,4):
  ListOfYear.append(i)
for i in range(1950,2023,4):
  ListOfYear.append(i)
ListOfYear

def addyear(df, x):
  year = [x for i in range(len(df))]
  df['Year']=year
  return df

FIFA = pd.DataFrame()
for i in range(1930,1939,4):
    temp = pd.read_csv('FIFA - '+str(i)+'.csv')
    temp = addyear(temp,i)
    FIFA = pd.concat([FIFA,temp],axis=0,ignore_index=True)

for i in range(1950,2019,4):
    temp = pd.read_csv('FIFA - '+str(i)+'.csv')
    temp = addyear(temp,i)
    FIFA = pd.concat([FIFA,temp],axis=0,ignore_index=True)

FIFA.info()

FIFA['Goal Difference'].value_counts()

FIFA['Goal Difference'] = FIFA['Goal Difference'].apply(lambda x: -int(x[1]) if x[0] in ['−','-'] else int(x))

i = 2022
temp = pd.read_csv('FIFA - '+str(i)+'.csv')
temp['Goal Difference'] = temp['Goal Difference'].astype('int64')
temp = addyear(temp,i)
FIFA = pd.concat([FIFA,temp],axis=0,ignore_index=True)

FIFA.info()

wc_summ = pd.read_csv("FIFA - World Cup Summary.csv", index_col="YEAR")
wc_summ.head()

# FIFA.loc[FIFA["Team"] == 'West Germany', "Team"] = 'Germany'
FIFA['Team'] = FIFA['Team'].apply(lambda x: 'Germany' if x in ['West Germany', 'East Germany'] else x)

label,count = pd.factorize(FIFA['Team'])

len(count)

wc_summ.loc[wc_summ["HOST"] == 'West Germany', "HOST"] = 'Germany'
wc_summ.loc[wc_summ["CHAMPION"] == 'West Germany', "CHAMPION"] = 'Germany'
wc_summ.loc[wc_summ["RUNNER UP"] == 'West Germany', "RUNNER UP"] = 'Germany'
wc_summ.loc[wc_summ["THIRD PLACE"] == 'West Germany', "THIRD PLACE"] = 'Germany'





Fifa2 = FIFA.copy()
Fifa2 = Fifa2.drop(columns=['Position','Year'])
FIFA_teams = Fifa2.groupby(['Team']).sum()
FIFA_teams

FIFA_teams['Win Rate'] = (FIFA_teams['Win']/FIFA_teams['Games Played'])*100
FIFA_teams.sort_values(['Games Played','Win'], ascending=False).head(20)
newfifateam = FIFA_teams.sort_values(['Games Played','Win'], ascending=False).head(20)
newfifateam

teams = [team for team in newfifateam.index]

plt.bar(teams[:15],newfifateam['Games Played'][:15])
plt.xticks(teams[:11], rotation = 'vertical', size = 10)
plt.ylabel('Games Played')
plt.xlabel('Teams')
plt.title('Top 10 teams number of worldcup appearances ')
plt.show()

FIFA_teams = FIFA_teams.sort_values(['Win'], ascending = False)

plt.bar(teams[:15],FIFA_teams['Win'][:15])
plt.xlabel('Teams')
plt.ylabel('Wins')
plt.xticks(teams[:11], rotation='vertical', size = 10)
plt.title('Top 10 World Cup teams with most wins ')
plt.show()

FIFA_teams = FIFA_teams.sort_values(['Win Rate'], ascending = False)

plt.bar(teams[:15],FIFA_teams['Win Rate'][:15])
plt.xlabel('Teams')
plt.ylabel('Win Rates')
plt.xticks(teams[:11], rotation='vertical', size = 10)
plt.title('Top 10 World Cup teams with highest win rates ')
plt.show()

table_HOST_wc_summ = wc_summ['HOST'].value_counts()

sns.countplot(data=wc_summ, x='HOST', order=table_HOST_wc_summ.index.values, color='y')
plt.title('Number of world cup hosts per team')
plt.xticks(rotation=90);

table_RUNNER_UP_wc_summ = wc_summ['RUNNER UP'].value_counts()

sns.countplot(data=wc_summ, x='RUNNER UP', order=table_RUNNER_UP_wc_summ.index.values, color='g')
plt.title('Number of world cup RUNNER UP per team')
plt.xticks(rotation=90);

table_THIRD_PLACE_wc_summ = wc_summ['THIRD PLACE'].value_counts()

sns.countplot(data=wc_summ, x='THIRD PLACE', order=table_THIRD_PLACE_wc_summ.index.values, color='r')
plt.title('Number of world cup THIRD PLACEs per team')
plt.xticks(rotation=90);

plt.figure(figsize=(12,10))
dataplot = sns.heatmap(FIFA_teams.corr())

table1 = wc_summ['CHAMPION'].value_counts()
table1
plt.pie(table1, labels=['Brazil', 'Italy', 'Germany', 'Argentina', 'Uruguay', 'France', 'England', 'Spain'], autopct='%.2f %%')
plt.title('World Cup Champion Distribution');





# Generate a count plot of World Cup wins per Team

plt.figure(figsize=(14,9))
plt.title("Number of World Cup Wins per Team")
sns.countplot(data=wc_summ, x="CHAMPION", order=wc_summ['CHAMPION'].value_counts().index)
plt.xlabel("Team")



# Add a new column to the dataframe which represents a boolean if host country won 

host_won = []
for index, row in wc_summ.iterrows():
    host_won.append(row["HOST"] == row["CHAMPION"])
wc_summ["HOST WON"] = host_won

# Generate a count plot of booleans that indicates that the host country won

plt.figure(figsize=(10,9))
plt.title("Number of Host Country Wins")
sns.countplot(data=wc_summ, x="HOST WON")
plt.xlabel("Boolean for Host Country Wins")

# Calculating percentage of Host Country Wins

host_win_total = len(wc_summ[wc_summ["HOST WON"] == True]) 
tournament_total = len(wc_summ) 
host_win_percentage = (host_win_total/tournament_total)*100
host_win_percentage

# Generate list of teams and unique teams

list_of_teams = []


for i in ListOfYear:
  temp = pd.read_csv('FIFA - '+str(i)+'.csv')
  for team in temp['Team']:
    list_of_teams.append(team)


unique_teams = list(set(list_of_teams))
print(f"There are {len(unique_teams)} unique teams out of the {len(list_of_teams)} that have participated in the history of the World Cup.")

# Calculate number of appearances per team in the World Cup 

team_apps = {
    "Team": [],
    "Appearances": []
}
for team in unique_teams:
    team_apps["Team"].append(team)
    team_apps["Appearances"].append(list_of_teams.count(team))
team_apps_data = pd.DataFrame(team_apps).sort_values(by="Appearances", ascending=False).reset_index(drop=True)

team_apps_data

team_apps_data.tail()

# Generate plot for total goals per year

plt.figure(figsize=(14,9))
plt.title("Total Goals per Year")
sns.scatterplot(x=wc_summ.index, y=wc_summ["GOALS SCORED"])
sns.regplot(x=wc_summ.index, y=wc_summ["GOALS SCORED"])
plt.xlabel("Year")
plt.ylabel("Goals Scored")

# Generate plot for average number of goals per game per year

plt.figure(figsize=(14,9))
plt.title("Average Goals per Game")
sns.scatterplot(x=wc_summ.index, y=wc_summ["AVG GOALS PER GAME"])
sns.regplot(x=wc_summ.index, y=wc_summ["AVG GOALS PER GAME"])
plt.xlabel("Year")
plt.ylabel("Average Goals per Game")

# Generate plot for total matches per year

plt.figure(figsize=(14,9))
plt.title("Total Matches per Year")
sns.scatterplot(x=wc_summ.index, y=wc_summ["MATCHES PLAYED"])
sns.regplot(x=wc_summ.index, y=wc_summ["MATCHES PLAYED"])
plt.xlabel("Year")
plt.ylabel("Matches per Year")

# Generate champion data

champion_data = {
    "Year": ListOfYear,
    "Team": [],
    "Goals Scored": [],
    "Goals Conceded": [],
}

for i in ListOfYear: 
  tournament = pd.read_csv('FIFA - '+str(i)+'.csv')
  champion_data["Team"].append(tournament.iloc[0]["Team"])
  champion_data["Goals Scored"].append(tournament.iloc[0]["Goals For"])
  champion_data["Goals Conceded"].append(tournament.iloc[0]["Goals Against"])

champion_df = pd.DataFrame(champion_data).set_index("Year")
champion_df.head()

# Generate probability density of champions' goals scored and conceded

plt.title("Probability Density of Champions' Goal Stats")
sns.kdeplot(data=champion_df["Goals Scored"], color='r', fill=True, label="Goals Scored")
sns.kdeplot(data=champion_df["Goals Conceded"], color='b', fill=True, label="Goals Conceded")
plt.legend()
plt.xlabel("Goals")
plt.ylabel("Probability Density")

#distribution of each variable
FIFA.hist(figsize = (12,10), color = 'royalblue')
plt.show()



FIFA

labels,counts = pd.factorize(FIFA['Team'])
namess = FIFA['Team'].iloc[:].values
teamnamess = {}
for i in range(len(labels)):
  teamnamess[i]= namess[i]
  
print(teamnamess)

#use it before feeding it to any algorithm else avoid it
labels,counts = pd.factorize(FIFA['Team'])
FIFA['Team'] = labels

FIFA

"""## **MODELSS**"""

# To predict “points” class our model performs:
FIFAsplit = FIFA.copy()
X = FIFAsplit.drop('Points', axis = 1)
y = FIFAsplit['Points']
X = X.iloc[:,:].values
y = y.iloc[:].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)
print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)

#Linear Regression
lr = LinearRegression()
lr.fit(X_train, y_train)
lr.score(X_test, y_test)

#Ridge Regression
ridge = Ridge(alpha = 0.5)
ridge.fit(X_train, y_train)
ridge.score(X_test, y_test)

#Lasso Regression
lasso = Lasso(alpha = 0.5)
lasso.fit(X_train, y_train)
lasso.score(X_test, y_test)

#KNN
from sklearn.neighbors import KNeighborsRegressor
neigh = KNeighborsRegressor(n_neighbors=3)
neigh.fit(X_train, y_train)
neigh.score(X_test, y_test)

#SVR
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
regr = make_pipeline(StandardScaler(), SVR(C=1.0, epsilon=0.2))
regr.fit(X_train, y_train)
regr.score(X_test, y_test)

#prediction
y_pred = lr.predict(X_test)
print(y_pred)

"""Goal Difference Prediction"""

#To predict “Goal Difference” class our model performs:
FIFAsplit = FIFA.copy()
X = FIFAsplit.drop('Goal Difference', axis = 1)
y = FIFAsplit['Goal Difference']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)
print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)

#Linear Regression
lr = LinearRegression()
lr.fit(X_train, y_train)
lr.score(X_test, y_test)

#Ridge Regression
ridge = Ridge(alpha = 0.5)
ridge.fit(X_train, y_train)
ridge.score(X_test, y_test)

#Lasso Regression
lasso = Lasso(alpha = 0.5)
lasso.fit(X_train, y_train)
lasso.score(X_test, y_test)

#KNN
from sklearn.neighbors import KNeighborsRegressor
neigh = KNeighborsRegressor(n_neighbors=3)
neigh.fit(X_train, y_train)
neigh.score(X_test, y_test)

#SVR
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
regr = make_pipeline(StandardScaler(), SVR(C=1.0, epsilon=0.2))
regr.fit(X_train, y_train)
regr.score(X_test, y_test)

#prediction
y_pred = lr.predict(X_test)
print(y_pred)

"""Win Column Prediction"""

#To predict “Win” class our model performs:
FIFAsplit = FIFA.copy()
X = FIFAsplit.drop('Win', axis = 1)
y = FIFAsplit['Win']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)
print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)

#Linear Regression
lr = LinearRegression()
lr.fit(X_train, y_train)
lr.score(X_test, y_test)

#Ridge Regression
ridge = Ridge(alpha = 0.5)
ridge.fit(X_train, y_train)
ridge.score(X_test, y_test)

#Lasso Regression
lasso = Lasso(alpha = 0.5)
lasso.fit(X_train, y_train)
lasso.score(X_test, y_test)

#KNN
from sklearn.neighbors import KNeighborsRegressor
neigh = KNeighborsRegressor(n_neighbors=3)
neigh.fit(X_train, y_train)
neigh.score(X_test, y_test)

#SVR
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
regr = make_pipeline(StandardScaler(), SVR(C=1.0, epsilon=0.2))
regr.fit(X_train, y_train)
regr.score(X_test, y_test)

#prediction
y_pred = lr.predict(X_test)
print(y_pred)

"""Team Column Prediction"""

# #Make sure that other results in below and above box are commented out
FIFAsplit = FIFA.copy()
X = FIFAsplit.drop('Team', axis = 1)
y = FIFAsplit['Team']

X

X = X.iloc[:,:].values
y = y.iloc[:].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)
print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)

X_train

#Linear Regression
lr = LinearRegression()
lr.fit(X_train, y_train)
lr.score(X_test, y_test)

t = np.array([[10,4,4,0,0,10,2,8,8,2026]]) # it's a sample to predict who would win in 2026
ans = lr.predict(t)

import math
teamnamess[math.ceil(ans)]

#Ridge Regression
ridge = Ridge(alpha = 0.5)
ridge.fit(X_train, y_train)
ridge.score(X_test, y_test)

#Lasso Regression
lasso = Lasso(alpha = 0.5)
lasso.fit(X_train, y_train)
lasso.score(X_test, y_test)

#KNN
from sklearn.neighbors import KNeighborsRegressor
neigh = KNeighborsRegressor(n_neighbors=3)
neigh.fit(X_train, y_train)
neigh.score(X_test, y_test)

#SVR
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
regr = make_pipeline(StandardScaler(), SVR(C=1.0, epsilon=0.2))
regr.fit(X_train, y_train)
regr.score(X_test, y_test)

#prediction
y_pred = lr.predict(X_test)
print(y_pred)

#check MAE, MSE and RMSE
print('Mean Absolute Error :', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error :', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error :', math.sqrt(metrics.mean_squared_error(y_test, y_pred)))

#visualize model
x = y_test
y = y_pred

plt.title('Linear Regression Model', fontsize = 15, color = 'g', pad = 12)
plt.plot(x, y, 'o', color = 'r')

m, b = np.polyfit(x, y, 1)
plt.plot(x, m * x + b, color = 'darkblue')
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.show()



from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
Model = RandomForestClassifier(random_state=100,n_jobs=-1)

params = {'n_estimators':[200],
          'max_depth':[3,6,10,15,20,25,30],
          'max_features':[0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7]}

grid_search = GridSearchCV(estimator=Model,param_grid=params,verbose=1,n_jobs=-1,scoring='accuracy')
grid_search.fit(X_train,y_train)
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)
print(accuracy_score(y_test,y_pred))

rresults=[]
for i in range(10):
    t = np.array([[i,4,4,0,0,10,2,10,8,2026]]) # it's a sample to predict who would win in 2026
    ans = lr.predict(t)
    rresults.append(teamnamess[math.ceil(ans)])
print(rresults)

run_query = input("Do you want to run a query(y/n): ").lower()

while(run_query!='n'):
    
    #10,4,4,0,0,10,2,8,8,2026
    x1 = int(input('\nEnter the value for Position(Range 1 to 32): '))
    x2 = int(input('Enter the value for Games Played: '))
    x3 = int(input('Enter the value for Win: '))
    x4 = int(input('Enter the value for Draw: '))
    x5 = int(input('Enter the value for Loss: '))
    x6 = int(input('Enter the value for Goals For: '))
    x7 = int(input('Enter the value for Goals Against: '))
    x8 = int(input('Enter the value for Goal Difference: '))
    x9 = int(input('Enter the value for Points: '))
    x10 = int(input('Enter the value for Year: '))
    t = np.array([[x1,x2,x3,x4,x5,x6,x7,x8,x9,x10]]) # it's a sample to predict who would win in 2026
    ans = lr.predict(t)
    print("TEAM : ",teamnamess[math.ceil(ans)])    
    run_query = input("\nDo you want to run a query again (y/n): ").lower()

print("Search Completed!!!")

