# 导入函数库
from jqdata import *
import numpy as np
import pandas as pd
from six import BytesIO
import talib as tb

# 初始化函数，设定基准等等
def initialize(context):
    g.security=pd.read_csv(BytesIO(read_file('sec1.csv')))
    g.cash = context.portfolio.available_cash
    run_daily(period1,time='13:05')
    run_daily(period,time='14:50')

def get_macd(stock):
    array = get_bars(security=stock,count=300,unit='1d',fields=['close'],include_now=True,end_dt=None,fq_ref_date=None)
    close_list = array['close']
    dif, dea, macd = tb.MACD(close_list, fastperiod=4, slowperiod=8, signalperiod=3)
    if(dif[len(dif)-1]>dea[len(dea)-1] and dif[len(dif)-2]<dea[len(dea)-2]):
        #macd金叉
        return 1
    elif(dif[len(dif)-1]<dea[len(dea)-1] and dif[len(dif)-2]>dea[len(dea)-2]):
        #macd死叉
        return -1
    else:
        return 0

def period(context):
    arr=[]
    cash = g.cash/len(g.security)
    order_target('511880.XSHG',0)
    for i in range(len(g.security)):
        val=[]
        sec=g.security['sec'][i]
        macd=get_macd(sec)
        if(sec in context.portfolio.positions.keys()):
            continue
        mtss1=get_mtss(sec, start_date='2015-01-01', end_date=context.current_dt)
        if(macd==1):
            if(sec not in context.portfolio.positions.keys()):
                speed=(mtss1['fin_value'][len(mtss1)-2]-mtss1['fin_value'][len(mtss1)-1])/mtss1['fin_value'][len(mtss1)-1]#此处为融资余额相对变化率
                val.append(speed)
                val.append(sec)
                arr.append(val)
    axx=len(arr)
    for i in range(axx):
        sec=arr[i][1]
        order_value(sec, cash)
        log.info("Buying %s" % (sec))
    order_value('511880.XSHG',context.portfolio.available_cash)

def period1(context):
    for i in range(len(g.security)):
        sec=g.security['sec'][i]
        macd=get_macd(sec)
        if(sec not in context.portfolio.positions.keys()):
            continue
        if(macd==-1):
            order_target(sec, 0)
            log.info("Selling %s" % (sec))
