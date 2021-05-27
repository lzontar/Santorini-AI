import os

ALL_MINMAXERS =  [i.split('.')[0] for i in os.listdir('./Minmaxers') if i[0] != '_']
