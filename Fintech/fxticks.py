# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 11:58:27 2019

@author: docs9
"""

import requests
import pandas as pd
from datetime import datetime, date
import zipfile


def downloadData(save_path, filenames):
    home = 'http://ratedata.gaincapital.com/'
    count = 1
    data = []
    for filename in filenames:
        url = home + '2016/12 December/' + filename
        res = requests.get(url)
        f = open()
        path = save_path + filename
        f = open(path, 'wb')
        f.write(res.content)
        f.close()
        
        csv = 'USD_JPY_Week%d.csv' % count
        try:
            f = zipfile.ZipFile(path).open(csv)
            dfx = pd.read_csv(f, index_col=3)[['RateBid']]
            f.close()
            data.append(dfx)
        except:
            return None
        
        count += 1
    return data

if __name__ == '__main__':
    files = ['USD_JPY_Week1.zip', 'USD_JPY_Week2.zip']
    holder = './data/'
    data = downloadData(holder, files)
    print(data[-5:])

        

        
        
