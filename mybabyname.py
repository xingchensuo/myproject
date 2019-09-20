#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 15:44:04 2019

@author: zhangchen
"""
#import the data
import pandas as pd
import numpy as np
names1880 = pd.read_csv('/Users/zhangchen/Downloads/names/yob1880.txt',names=['name','sex','births'])
birthsum = names1880.groupby('sex').births.sum()
#print(birthsum)

#add 'year' column and aggerate into one dataframe
years = range(1880,2011)
piece = []
items = ['name','sex','births']
for year in years:
    path = '/Users/zhangchen/Downloads/names/yob%d.txt'%year
    frame = pd.read_csv(path,names = items)
    frame['year'] = year #frmae is an object of type "DataFrame"
    piece.append(frame)
names = pd.concat(piece, ignore_index=True)
names.info(verbose=True)

#group by year and sex
total_birth = names.pivot_table('births', index = 'year', columns = 'sex', aggfunc = sum)
total_birth.tail()
total_birth.plot(title='Total births by sex and year')
#give each name a prop within group year and sex
def add_prop(group):
    group['prop']= group.births/group.births.sum()
    return(group)
names = names.groupby(['year','sex']).apply(add_prop)
names.info()

#what the top 1000 of the names? get the top 1000 grouped by year and sex
def get_top1000(group):
    return group.sort_index(by = 'births', ascending = False)[:1000]
top1000 = names.groupby(['year','sex']).apply(get_top1000)
top1000.reset_index(drop = True, inplace = True)
#boys = top1000(top1000['sex' == 'M'])
#girls = top1000(top1000['sex' == 'F'])

#How a specific name count changed along with year?
table = top1000.pivot_table('births', index = 'year', columns = 'name', aggfunc = sum)
subtabel = table[['John', 'Harry', 'Mary', 'Marilyn']]
subtabel.plot(subplots = True, figsize = (12,10), grid = False, title = "Number of births per year")

#how much proportion for the top 1000 take in total?
topprop = top1000.pivot_table('prop', index = 'year', columns = 'sex', aggfunc = sum)
topprop.plot(title = "Sum of table1000.prop by year and sex", yticks = np.linspace(0,1.2,13), xticks = np.arange(1880,2011,10))

#how many of the most popular name it takes to reach 50%
def fifpoint(group,p=0.5):
    table = group.sort_index(by = 'prop', ascending = False).prop.cumsum()    
    return(table.searchsorted(p)+1)
pointable = top1000.groupby(['year','sex']).apply(fifpoint)
pointable = pointable.unstack('sex')
pointable.plot(title='count to reach 50%')

#get the last letter num and prop based on year and sex
get_last_name = lambda x: x[-1]
last_latters = names.name.map(get_last_name)
last_latters.name = 'last_letter'
lettertable = names.pivot_table('births', index = last_latters, columns = ['sex', 'year'], aggfunc = sum)
subletter = lettertable.reindex(columns = [1910, 1960, 2010], level = 'year')
subletter.head()
letterprop = subletter/subletter.sum()
letterprop.head()
#visualize this last letter prop
import matplotlib.pyplot as plt
fig, axs = plt.subplots(2,1,figsize=(10,8))
letterprop['M'].plot(kind='bar', ax=axs[0], title = 'Male')
letterprop['F'].plot(kind='bar', ax=axs[1], title = 'Female', legend = False)
#specific letters with 'd,n,y' changed by year
filtable = lettertable/lettertable.sum()
submale = filtable.ix[['d','n','y'],'M'].T
submale.head()
submale.plot()

# how popular names change among boys and girls, lesley_like for example.
all_names = top1000.name.unique()
mask = np.array(['lesl' in x.lower() for x in all_names])
lesllike = all_names[mask]
filtered = top1000[top1000.name.isin(lesllike)]
filtered.groupby('name').births.sum()
table = filtered.pivot_table('births', index = 'year', columns = 'sex', aggfunc = sum)
table = table.div(table.sum(1),axis = 0)
table.plot(title='name change associate with sex', style = {'M':'k-','F':'k--'})



    





