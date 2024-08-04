import json
import pandas as pd
from datetime import datetime
from datetime import timedelta

try:
    openfile = open('data.json', 'r')
    tobejson = json.load(openfile)
    openfile.close()
except FileNotFoundError:
    tobejson = {'currentctr': 0}


demoTB = pd.read_csv('TB final.csv', header= 0)
dct = demoTB[['Trans. Time','Entry Time','Strike Price','Option Type',
              'Buy/Sell','Average Price','Total Qty','Trade Qty']].to_dict()
current_ctr = len(dct['Trans. Time'])

timelst = ['09:15:59', '09:29:59', '09:59:59', '10:14:59', '10:29:59',
           '10:44:59', '11:59:59', '13:14:59']

checkpt = []

for tim in timelst:
    timchg = datetime.strptime(str(datetime.today()).split(' ')[0] + ' ' + tim, '%Y-%m-%d %H:%M:%S')
    checkpt.append([timchg - timedelta(seconds=i) for i in range(-5,6)])

# print(checkpt)

current_ctr = current_ctr - tobejson['currentctr']

# print(checkpt)

print(current_ctr)

for i in range(current_ctr-1, -1, -1):
    day = datetime.strptime(str(datetime.today()).split(' ')[0] + ' ' + dct['Entry Time'][i], '%Y-%m-%d %H:%M:%S')
    ind = [index for index, row in enumerate(checkpt) if day in row]
    if ind:
        key = timelst[ind[0]] + ' ' + dct['Option Type'][i]
        if key not in tobejson:
            tobejson[key] = {'Trans. Time': dct['Trans. Time'][i],
                             'Entry Time': dct['Entry Time'][i],
                             'Strike Price': dct['Strike Price'][i],
                             'Option Type': dct['Option Type'][i],
                             'Buy/Sell': dct['Buy/Sell'][i],
                             'Total Qty': dct['Total Qty'][i],
                             'Average Price Buy' : [],
                             'Average Price Sell' : [],
                             'Trade Qty Buy' : [],
                             'Trade Qty Sell' : []}
            tobejson[key]['Average Price'+ ' ' +dct['Buy/Sell'][i]].append(dct['Average Price'][i])
            tobejson[key]['Trade Qty'+ ' ' +dct['Buy/Sell'][i]].append(dct['Trade Qty'][i])

        elif tobejson[key]['Buy/Sell'] == dct['Buy/Sell'][i]:
            tobejson[key]['Average Price'+ ' ' +dct['Buy/Sell'][i]].append(dct['Average Price'][i])
            tobejson[key]['Trade Qty'+ ' ' +dct['Buy/Sell'][i]].append(dct['Trade Qty'][i])
        elif tobejson[key]['Buy/Sell'] != dct['Buy/Sell'][i]:
            tobejson[key]['Exit time'] = dct['Trans. Time'][i]
            tobejson[key]['Average Price'+ ' ' +dct['Buy/Sell'][i]].append(dct['Average Price'][i])
            tobejson[key]['Trade Qty'+ ' ' +dct['Buy/Sell'][i]].append(dct['Trade Qty'][i])


for k, v in tobejson.items():
    print(k)
    if k != 'currentctr':
        for key, val in v.items():
            print('\t',key,'\t',val)

tobejson['currentctr'] = len(dct['Trans. Time'])

with open("data.json", "w") as outfile:
    json.dump(tobejson, outfile)