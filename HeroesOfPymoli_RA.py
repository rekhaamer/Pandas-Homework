
# coding: utf-8

# # Heroes Of Pymoli Data Analysis
# * Of the 1163 active players, the vast majority are male (82%). There also exists, a smaller, but notable proportion of female players (16%).
# 
# * Our peak age demographic falls between 20-24 (42%) with secondary groups falling between 15-19 (17.80%) and 25-29 (15.48%).
# 
# * Our players are putting in significant cash during the lifetime of their gameplay. Across all major age and gender demographics, the average purchase for a user is roughly $491.   
# -----

# In[50]:


import pandas as pd
import os
file=os.path.join('purchase_data.json')
file_df=pd.read_json(file)
file_df.head()


print("Player Count")
print()

# In[51]:


TotalPlayers=len(file_df['SN'].value_counts())
TP=pd.DataFrame([{'Total Players':TotalPlayers}])
print(TP)

print("Purchasing Analysis (Total)")

# In[49]:


UniqueItems=len(file_df['Item ID'].value_counts())
AvgPrice=file_df['Price'].mean()
# AvgPrice=AvgPrice.map('{:,.2f}'.format)
CountPurchases=file_df['Item Name'].count()
Revenue=file_df['Price'].sum()
summ = pd.DataFrame([{'01-Number of Unique Items':UniqueItems,'02-Average Price':AvgPrice,
                      '03-Number of Purchases':CountPurchases,'04-Total Revenue':Revenue}])
summ['02-Average Price'] = summ['02-Average Price'].map('${:,.2f}'.format)
summ['04-Total Revenue'] = summ['04-Total Revenue'].map('${:,.2f}'.format)
print(summ)


print("Gender Demographics")

# In[55]:


Gender=file_df.groupby('Gender').agg('nunique')
GenderCount=Gender['SN']
GenderPct=(GenderCount/TotalPlayers*100).map('{:,.2f}'.format)
GenderSumm=pd.DataFrame({'Percentage of Players':GenderPct, 'Total Count':GenderCount})
GenderSumm=GenderSumm.sort_values('Percentage of Players', ascending=False)
print(GenderSumm)


# 
print("Purchasing Analysis (Gender)")

# In[59]:


GenderPurchaseCount=file_df.groupby('Gender').count()['Item Name']
GenderAvgPurchasePrice=file_df.groupby('Gender').mean()['Price']
GenderPurchaseValue=file_df.groupby('Gender').sum()['Price']
NormalizedTotal=GenderPurchaseValue/GenderCount
PAGender=pd.DataFrame({'01-Purchase Count':GenderPurchaseCount,'02-Average Purchase Price':GenderAvgPurchasePrice,
              '03-Total Purchase Value':GenderPurchaseValue,'04-Normalized Total':NormalizedTotal})
PAGender['02-Average Purchase Price'] = PAGender['02-Average Purchase Price'].map('${:,.2f}'.format)
PAGender['03-Total Purchase Value'] = PAGender['03-Total Purchase Value'].map('${:,.2f}'.format)
PAGender['04-Normalized Total'] = PAGender['04-Normalized Total'].map('${:,.2f}'.format)
print(PAGender)


print("Age Demographics")

# In[63]:


bins=[0,9,14,19,24,29,34,39,45]
BinName=["<10","10-14","15-19","20-24","25-29","30-34","35-39","40+"]
file_df['Bins']=pd.cut(file_df['Age'],bins,labels=BinName)
CountByAge=file_df[['SN','Bins']].drop_duplicates().groupby(['Bins']).count()
AgePct=(CountByAge/TotalPlayers*100)
AgeSumm=pd.DataFrame({'Percentage of Players': AgePct['SN'], 'Total Count':CountByAge['SN']})
AgeSumm['Percentage of Players'] = AgeSumm['Percentage of Players'].map('{:,.2f}'.format)
print(AgeSumm)


print("Purchasing Analysis (Age)")

# In[65]:


PurchaseValueByAge=file_df.groupby(['Bins']).sum()['Price']
PurchaseCountByAge=file_df.groupby(['Bins']).count()['Price']
PurchaseAvgPriceByAge=file_df.groupby(['Bins']).mean()['Price']
NormalizedTotalByAge=PurchaseValueByAge/CountByAge['SN']
PA_DF=pd.DataFrame({'01-Purchase Count':PurchaseCountByAge,'02-Average Purchase Price':PurchaseAvgPriceByAge,
             '03-Total Purchase Value':PurchaseValueByAge, '04-Normalized Total':NormalizedTotalByAge})
PA_DF['02-Average Purchase Price']=PA_DF['02-Average Purchase Price'].map('${:,.2f}'.format)
PA_DF['03-Total Purchase Value']=PA_DF['03-Total Purchase Value'].map('${:,.2f}'.format)
PA_DF['04-Normalized Total']=PA_DF['04-Normalized Total'].map('${:,.2f}'.format)
print(PA_DF)


print("Top Spenders")

# In[68]:


TopSpenderCount=file_df.groupby('SN').count()
TopSpenderRevenue=file_df.groupby('SN').sum()
TopSpenderPrice=file_df.groupby('SN').sum()/file_df.groupby('SN').count()
TopSpenderDF=pd.DataFrame({'01-Purchase Count':TopSpenderCount['Price'],'02-Average Purchase Price':TopSpenderPrice['Price'],
             '03-Total Purchase Value':TopSpenderRevenue['Price']})
TopSpenderDF=TopSpenderDF.sort_values('03-Total Purchase Value', ascending=False)
TopSpenderDF['02-Average Purchase Price']=TopSpenderDF['02-Average Purchase Price'].map('${:,.2f}'.format)
TopSpenderDF['03-Total Purchase Value']=TopSpenderDF['03-Total Purchase Value'].map('${:,.2f}'.format)
print(TopSpenderDF.head())


print("Most Popular Items")

# In[71]:


PopularItemCount=file_df.groupby(['Item ID','Item Name']).count()['Price']
PopularItemPrice=file_df.groupby(['Item ID','Item Name']).mean()['Price']
PopularItemRevenue=file_df.groupby(['Item ID','Item Name']).sum()['Price']
PopularDF=pd.DataFrame({'01-Purchase Count':PopularItemCount,'02-Item Price':PopularItemPrice,
                        '03-Total Purchase Value':PopularItemRevenue})
PopularDF=PopularDF.sort_values('01-Purchase Count', ascending=False)
PopularDF['02-Item Price']=PopularDF['02-Item Price'].map('${:,.2f}'.format)
PopularDF['03-Total Purchase Value']=PopularDF['03-Total Purchase Value'].map('${:,.2f}'.format)
print(PopularDF.head())


print("Most Profitable Items")

# In[74]:


ProfitableItemCount=file_df.groupby(['Item ID','Item Name']).count()['Price']
ProfitableItemPrice=file_df.groupby(['Item ID','Item Name']).mean()['Price']
ProfitableItemRevenue=file_df.groupby(['Item ID','Item Name']).sum()['Price']
ProfitableDF=pd.DataFrame({'01-Purchase Count':ProfitableItemCount,'02-Item Price':ProfitableItemPrice,
                        '03-Total Purchase Value':ProfitableItemRevenue})
ProfitableDF=ProfitableDF.sort_values('03-Total Purchase Value', ascending=False)
ProfitableDF['02-Item Price']=ProfitableDF['02-Item Price'].map('${:,.2f}'.format)
ProfitableDF['03-Total Purchase Value']=ProfitableDF['03-Total Purchase Value'].map('${:,.2f}'.format)
print(ProfitableDF.head())

