# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 14:06:14 2020

@author: zpc
"""

from jqdatasdk import *
import csv

auth('15098803876','123369qazQAZ')
stocks_all=get_margincash_stocks()
stocks_new=[]

for i in range(len(stocks_all)):
    mtss=get_mtss(stocks_all[i],'2015-01-01','2020-02-20')
    if(len(mtss)==1249):
        stocks_new.append(stocks_all[i])
    if(len(stocks_new)==100):#共100只股票
        break

#深证成指收盘价
mi=get_price('399001.XSHE',
             start_date='2015-01-01',
             end_date='2020-02-20',
             frequency='daily',
             fields=['close'],
             skip_paused=False,
             fq='pre',
             panel=True)

for i in range(len(stocks_new)):
    mtss=get_mtss(stocks_new[i],'2015-01-01','2020-02-20')
    mtss=mtss.set_index('date')
    del mtss['sec_code']
    #插入深证成指列
    mtss.insert(7,'market_index',mi['close'])
    info=get_price(stocks_new[i],
                   start_date='2015-01-01',
                   end_date='2020-02-20',
                   frequency='daily',
                   skip_paused=False,
                   fq='pre',
                   panel=True)
    mtss.insert(8,'open',info['open'])
    mtss.insert(9,'close',info['close'])
    mtss.insert(10,'high',info['high'])
    mtss.insert(11,'low',info['low'])
    mtss.insert(12,'volume',info['volume'])
    mtss.insert(13,'money',info['money'])
    mtss = (mtss - mtss.min()) / (mtss.max() - mtss.min())
    mtss.insert(14,'price',0)
    
    #增长情况
    for j in range(len(info)-2):
        if(j==0):
            mtss['price'][j]=0
        elif(info['close'][j+2]==info['close'][j+1]):#平
            mtss['price'][j]=0
        elif(info['close'][j+2]>info['close'][j+1]):#增
            mtss['price'][j]=1
        else:#跌
            mtss['price'][j]=0
    
    #处理缺失值
    mtss.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
    print(len(mtss),i)
    
    if(i==0):
        mtss.to_csv('train1.csv',index=None)
        
    else:
        mtss.to_csv('train1.csv',mode='a',index=None,header=False)