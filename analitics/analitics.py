import statistics
import datetime
import time
import math
import glob
import numpy
import sys
from scipy.stats import norm



servers = glob.glob("server_*")

sli_data=[]

sli_data.append(open("uRLLC.dat","w"))
sli_data.append(open("eMBB.dat","w"))
sli_data.append(open("mMTC.dat","w"))

sli_data_io=[]

sli_data_io.append(open("uRLLC-io.dat","w"))
sli_data_io.append(open("eMBB-io.dat","w"))
sli_data_io.append(open("mMTC-io.dat","w"))

f_tracer = open("pass.trace")

fts = open("../cell-client/first_ts")
first_ts = int(fts.readline().strip())
lts = open("../cell-client/last_ts")
last_ts = int(lts.readline().strip())

print(first_ts,last_ts)

sched_in = {}
sched_out = {}
sched_res = {}
sched_resp = {}
sched_p12 = {}
ttis = []

sli_delays= {0:[],1:[],2:[]}
sli_tps= {0:[],1:[],2:[]}

for line in f_tracer.readlines():
  if line.startswith("connecting") or line.startswith("turning"):
    continue
  arr_line = line.split()
  seconds = arr_line[1].strip("[]:")
  nano = arr_line[0].split(".")[1]
  stamp = int(seconds + nano)
  arr_line = arr_line[2:]
  logt = arr_line[0]

  if stamp < first_ts:
    continue

  if stamp > last_ts:
    print(line)
    print(first_ts,stamp,last_ts)
    break
  
  if logt == "SCHEDULER_IN" :
    if len(arr_line) < 7:
      continue
    ue_id = int(arr_line[2])
    sli =   int(arr_line[4])
    size =  int(arr_line[6])
    if sli not  in sched_in: sched_in[sli] = {}
    assert stamp not in sched_in
    sched_in[sli][stamp]={'size': size, 'slice': sli, 'stamp': stamp}
  elif logt == "SCHEDULER_OUT" :
    if len(arr_line) < 9:
      continue
    ue_id = int(arr_line[2])
    sli =   int(arr_line[4])
    size =  int(arr_line[6])
    rbs =   int(arr_line[8])
    if sli not in sched_out: sched_out[sli] = {}
    assert stamp not in sched_out
    sched_out[sli][stamp]={'size': size, 'slice': sli, 'stamp': stamp}
  elif logt == "RESOURCES_SCHEDULED":
    if len(arr_line) < 11:
      continue
    sli = int(arr_line[2])
    frame    = int(arr_line[4])
    subframe = int(arr_line[6])
    phase12  = int(arr_line[8])
    phase3   = int(arr_line[10])
    sched = phase12 + phase3
    keyp = stamp//1000000000*100000 +frame*10 + subframe
    sched_resp[keyp]['sched'][sli] = sched
    sched_p12[keyp]['sched'][sli] = phase12
    sched_p12[keyp]['sched']['out'] += phase3

    key = sched_resp[keyp]['stamp']
    if sli not in sched_res: sched_res[sli] = {}
    assert key not in sched_res
    sched_res[sli][key]={'sched': sched, 'slice': sli, 'stamp': key, 'p12': phase12, 'p3': phase3}

  elif logt == "SCHEDULING":
    if len(arr_line) < 5:
      continue
    frame    = int(arr_line[2])
    subframe = int(arr_line[4])
    ttis.append(stamp)
    keyp = stamp//1000000000*100000 +frame*10 + subframe
    if keyp not in sched_resp:
      sched_resp[keyp] = {'sched': {0:0, 1:0, 2:0},'stamp': stamp}
      sched_p12[keyp] = {'sched': {0:0, 1:0, 2:0, 'out':0},'stamp': stamp}
  else:
    print(arr_line)
    print("Invalid trace log")
sli_packets = {}
for i in range (0,3):
  sli_packets[i] = {}

for i in range(0,len(servers)-1):

  f_client = open("client_"+str(i+1)+".log","r")
  f_server = open("server_"+str(i+1)+".log","r")
  
  packets = {}
  delays=[]
  tps = []
  sent = 0
  recv = 0
  ue_id = i+1
  interval = 1
  
  for line in f_client.readlines():
    if line.startswith("#"):
      continue
    data = line.split()
  
    sli = (ue_id-1) % 3
    stamp = int(data[1])
    pid = int(data[2])
    size = int(data[3])
    key = str(ue_id) + "." + str(pid)
 
    if first_ts == -1 or stamp < first_ts:
      print(stamp)
      first_ts=stamp
  
    packets[key]={}
    packets[key]['ue_id'] = ue_id
    packets[key]['sent'] = stamp
    packets[key]['pid'] = pid
    packets[key]['size'] = size
  
    sent += 1
    
  for line in f_server.readlines():
    if line.startswith("#"):
      continue
    data = line.split()
    sli = (ue_id-1) % 3
    stamp = int(data[1])
    pid = int(data[2].rstrip('\x00'))
    size = int(data[3])

    recv += 1
  
    key = str(ue_id) + "." + str(pid)
    sent_stamp = packets[key]['sent']

    period = ((sent_stamp-first_ts)//1000000000//interval)*interval
    if period not in sli_packets[sli]:
      sli_packets[sli][period] = {}
      sli_packets[sli][period]["delay"] = []
      sli_packets[sli][period]["tp"] = []


    assert key in packets
    assert packets[key]['size'] == size
    
    packets[key]['recv'] = stamp
  
  
    assert stamp > sent_stamp

    delay = (stamp - sent_stamp)/1000000 #ms
    tp = size/delay #Kbps
  
    sli_delays[sli].append(delay)
    sli_tps[sli].append(tp)
    delays.append(delay)
    tps.append(tp)
    sli_packets[sli][period]["delay"].append(delay)
    sli_packets[sli][period]["tp"].append(tp)
  
  if len(delays) > 0:
    print("UE =",ue_id,", Delay avg =",statistics.mean(delays),", tp =",statistics.mean(tps),", Delivery =",recv/sent)
  else:
    print("UE",ue_id," DID NOT RECEIVE TRAFFIC!", file = sys.stderr)

sli_data_res = open("scheduler.dat","w")
for k in sorted(sched_resp):
  v = sched_resp[k]
  print((v['stamp']-first_ts)//1000000,v['sched'][0],v['sched'][1],v['sched'][2], file = sli_data_res)
sli_data_res.close()
  
sli_data_res = open("profiled.dat","w")
for k in sorted(sched_p12):
  v = sched_p12[k]
  print((v['stamp']-first_ts)//1000000,v['sched'][0],v['sched'][1],v['sched'][2],v['sched']['out'], file = sli_data_res)
sli_data_res.close()
  

for sli in range(0,3):
  print("stamp in out res", file=sli_data_io[sli])
  in_sorted = sorted(sched_in[sli].keys(), reverse=True)
  out_sorted = sorted(sched_out[sli].keys(), reverse=True)
  res_sorted = sorted(sched_res[sli].keys(), reverse=True)
  prev_ts = 0
  for i in range(0,len(ttis)-1):
    ts = ttis[i]
    next_ts = ttis[i+1]
    
    ins = []
    outs = []

    if len(in_sorted) == 0 or len(out_sorted) == 0:
      break

    assert in_sorted[-1] > prev_ts

    while in_sorted[-1] < ts:
      ins.append(sched_in[sli][in_sorted.pop()]['size'])
      if len(in_sorted) == 0:
        break

    while out_sorted[-1] > ts and out_sorted[-1] < next_ts:
      outs.append(sched_out[sli][out_sorted.pop()]['size'])
      if len(out_sorted) == 0:
        break

    scheduled = sched_res[sli][ts]['sched'] if ts in sched_res[sli] else 0

    print((ts-first_ts)//1000000,sum(ins),sum(outs),scheduled, file=sli_data_io[sli])

    prev_ts = ts


for s in range(0,3):
  print("#stamp delay(avg) delay(CI) tp(avg) tp(CI)",file=sli_data[s])
  for p in sorted(sli_packets[s]):
    samples = len(sli_packets[s][p]["delay"])
    if samples == 1:
      continue
    delay_avg = statistics.mean(sli_packets[s][p]["delay"])
    delay_ci = 1.96*statistics.stdev(sli_packets[s][p]["delay"])/math.sqrt(samples)
    tp_avg = statistics.mean(sli_packets[s][p]["tp"])
    tp_ci = 1.96*statistics.stdev(sli_packets[s][p]["tp"])/math.sqrt(samples)
    print(p,delay_avg,delay_ci,tp_avg,tp_ci,file=sli_data[s])
    print(p,delay_avg,delay_ci,tp_avg,tp_ci)



for s in range(0,3):
  cdfdf = open("cdf-delays-"+str(s)+".dat","w")
  cdftf = open("cdf-tps-"+str(s)+".dat","w")
  for d in sorted(sli_delays[s]):
    print(d,len(sli_delays[s]),file=cdfdf)
  for t in sorted(sli_tps[s]):
    print(t,len(sli_tps[s]),file=cdftf)
  cdfdf.close()
  cdftf.close()
