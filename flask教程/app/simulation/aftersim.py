import datetime
import csv
import sys

print('aftersim的参数：',sys.argv[1])

fout='result2.csv'

def once(fout):
    with open(fout, 'a') as wf:
        writer = csv.writer(wf)
        nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow(['run', nowtime])


once(fout)
print('调用 aftersim')