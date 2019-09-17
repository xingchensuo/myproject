#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 15:44:04 2019

@author: zhangchen
"""
#import the data
import pandas as pd
names1880 = pd.read_csv('/Users/zhangchen/Downloads/names/yob1880.txt',names=['names','sex','births'])
birthsum = names1880.groupby('sex').births.sum()
#print(birthsum)

#add 'year' column and aggerate into one dataframe
years = range(1880,2011)
piece = []
items = ['names','sex','births']
for year in years:
    path = '/Users/zhangchen/Downloads/names/yob%d.txt'%year
    frame = pd.read_csv(path,names = items)
    frame['year'] = year
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
#names.groupby(['year','sex'])[:1000]

