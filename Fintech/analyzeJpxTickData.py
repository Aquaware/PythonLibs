# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 15:07:35 2019

@author: 
"""

import os
import datetime
import pandas as pd

class Tick:
    def __init__(self, time, volume, price):
        self.time = time
        self.volume = float(volume)
        self.price = float(price)
        pass
    
class FourPrices:
    def __init__(self, time, open_price, close_price, low_price, high_price, volume):
        self.time = time
        self.o = open_price
        self.c = close_price
        self.h = high_price
        self.l = low_price
        self.volume = volume
        pass

    
    def add(self, volume, price):
        self.volume += volume
        self.close = price
        if price > self.h:
            self.h = price
        if price < self.l:
            self.l = price
        pass
    
    def description(self):
        print('t: ', self.time, ' v:', self.volume, ' o: ', self.o, ' c: ' , self.c, ' h: ', self.h, ' l: ', self.l ) 
        pass
        
    
class Candle:
    def __init__(self, interval):
        self.interval = interval
        self.prices = []
        self.current = None
        self.current_time = None
        pass
    
    def roundTime(self, time):
        y = time.year
        m = time.month
        d = time.day
        h = time.hour
        minute = int(time.minute / self.interval) * self.interval
        t = datetime.datetime(y, m, d, h, minute, 0, 0)
        t += datetime.timedelta(minutes=self.interval)
        return t
        
    def addTick(self, tick):
        t = self.roundTime(tick.time)
        if self.current_time is None:
            self.current = FourPrices(t, tick.price, tick.price, tick.price, tick.price, tick.volume)
            self.current_time = t
        else:   
            if t == self.current_time:
                self.current.add(tick.volume, tick.price)
            else:
                self.prices.append(self.current)
                self.current_time += datetime.timedelta(minutes=self.interval)
                while t > self.current_time:
                    self.current = FourPrices(self.current_time, 0, 0, 0, 0, 0)
                    self.prices.append(self.current)
                    self.current_time += datetime.timedelta(minutes=self.interval)
                self.current = FourPrices(t, tick.price, tick.price, tick.price, tick.price, tick.volume)
        pass
        
def fileList(holder_path, extension):
    files = []
    for filename in os.listdir(holder_path):
        if os.path.isfile(os.path.join(holder_path, filename)):
            values = filename.split('.')
            if len(values) == 2:
                if values[1] == extension:
                    files.append(filename)

    return files

def makePath(holder_path, filename):
    if len(holder_path) == 0:
        return './' + filename
    if holder_path[-1] != '/':
        holder_path += '/'
    return holder_path + filename


def importTickData(holder_path):
    files = fileList( holder_path, 'csv')
    if len(files) == 0:
        return None
    
    df = None
    for file in files:
        df0 = pd.read_csv(makePath(holder_path, files[0]))
        df1 = df0[['Make_Date', 'Time', 'Trade_Price', 'Trade_Volume']]
        if df is None:
            df = df1
        else:
            df = df.append(df1)
    
    #print(df1)
    sorted_df = df.sort_values(['Make_Date', 'Time'])
    #print(sorted_df)
    return sorted_df

def valueString(int_value, digit):
    s = ''
    for i in range(digit):
        s += '0'
    s += str(int_value)
    return s[len(s) - digit: len(s)]
    
    
def value2time(date_str, time_str):
    h = time_str[0:2]
    m = time_str[2:4]
    s = time_str[4:6]
    ms = time_str[6:]
    t = pd.to_datetime(date_str + ' ' + h + ':' + m + ':' + s + '.' + ms , format='%Y%m%d %H:%M:%S')
    return t
    
def tickData(holder_path):
    df = importTickData(holder_path)
    dates = list(df['Make_Date'])
    ts = list(df['Time'])
    times = []
    for date, t in zip(dates, ts):
        time = value2time(valueString(date, 8), valueString(t, 9))
        times.append(time)
        
    prices = list(df['Trade_Price'])
    volumes = list(df['Trade_Volume'])
    
    ticks = []
    for time, volume, price in zip(times, volumes, prices):
        tick = Tick(time, volume, price)
        ticks.append(tick)
    return ticks    

def test():
    holder_path = './data/'
    ticks = tickData(holder_path)
    candle = Candle(30)
    for tick in ticks:
        candle.addTick(tick)
        #candle.current.description()
        
        
    for price in candle.prices:
        price.description()
        
    pass
    
    
if __name__ == '__main__':
    test()
    #ticks = tickData()
    #print(ticks)
    
    
    


    
    