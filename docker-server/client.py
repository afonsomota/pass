import sys
import os
import getopt
import socket
import time
import random
import fcntl

ue_ip = "10.0.2.20"
port = 4444
l4type="udp"
ue_id = 1
idt = 40
size = 1000
sim_time = 20
jitter = 3
config= None
fconfig=None

try:
  opts,args = getopt.getopt(sys.argv[1:],"a:p:l:u:i:s:t:j:c:",["ip=","port=","l4proto=","ue=","idt=","size=","timeout=","jitter=","config="])
except getopt.GetoptError as err:
  print(err)
  sys.exit(2)

for o,a in opts:
  if o in ("-a","--ip"):
    ue_ip=a
  elif o in ("-p","--port"):
    port = int(a)
  elif o in ("-l","--l4proto"):
    l4type = a
  elif o in ("-u","--ue"):
    ue_id = int(a)
  elif o in ("-i","--idt"):
    idt = int(a)
  elif o in ("-s","--size"):
    size = int(a)
  elif o in ("-t","--timeout"):
    sim_time = int(a)
  elif o in ("-j","--jitter"):
    jitter = int(a)
  elif o in ("-c","--config"):
    config = a
  else:
    print("Uknown option")
    sys.exit(2)
  
output = open("/app/analitics/client_"+str(ue_id)+".log","w")

curr_stamp = time.time_ns()
old_stamp = curr_stamp

fd = open("/tmp/client.lock","w")
fcntl.lockf(fd,fcntl.LOCK_EX)
try:
  ts_file = open("/tmp/client.ts","r")
  curr_stamp = int(ts_file.readline().strip())
  ts_file.close()
except FileNotFoundError:
  ts_file = open("/tmp/client.ts","w")
  print(curr_stamp, file=ts_file)
  ts_file.close()
fcntl.lockf(fd,fcntl.LOCK_UN)


print("Starting client",ue_id,(old_stamp - curr_stamp)/1000000, file=sys.stderr)
start_stamp = curr_stamp + 20*1000000000

#inital jitter
time.sleep(20)

if ue_id == 1:
  fts = open("/app/cell-client/first_ts","w")
  print(start_stamp, file=fts)
  fts.close()

try:
  os.remove("/tmp/client.ts")
except:
  pass


s = None

if config != None:
  fconfig = open(config,"r")
  l4type = fconfig.readline().strip()

if l4type =="udp":
  s = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
elif l4type == "tcp":
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((ue_ip,port))
else:
  print("INVALID L4 TYPE")
  sys.exit(2)

pid = 0

stop_stamp = start_stamp

while True:

  burst = -1
  burst_idt = 0
  burst_max = 0
  burst_cnt = 0
  first_burst = True

  curr_stamp = stop_stamp

  if config != None:
    cline = fconfig.readline().split()
    if cline == []:
      break
    if cline[0].startswith("#"):
      continue
    idt      = int(cline[0])
    size     = int(cline[1])
    jitter   = int(cline[2])
    sim_time = int(cline[3])
    if len(cline) > 4:
      burst = float(cline[4])
      burst_idt = int(cline[5])
      burst_max = int(cline[6])
      burst_cnt = 0
  
  
  stop_stamp = curr_stamp + sim_time*1000000000
  time.sleep(random.random()*idt/1000)#sleep from 0 to idt
  
  while True:
    curr_stamp = time.time_ns()
  
    if curr_stamp > stop_stamp:
      break
  
    pid += 1
  
    msg = bytearray(size)
    msg[0:len(str(pid))] = str(pid).encode('utf-8')
    msg[-1:]=b'\n'
  
    stamp = time.time_ns()
    if l4type=="udp":
      s.sendto(msg,(ue_ip,port))
    elif l4type=="tcp":
      s.sendall(msg)
  
    print(ue_id,stamp,str(pid),len(msg), file=output)
  
    curr_jitter = random.randint(-jitter,jitter)
  
    #curr_jitter and idt in ms(10-3) stamps in ns(10-9)
    
    if burst > 0:
      if burst_cnt > 0:
        next_stamp = curr_stamp + burst_idt*1000000 + curr_jitter*1000000
        burst_cnt+=1
        if burst_cnt == burst_max:
          burst_cnt = 0
      else:
        if burst >= random.random() or first_burst:
          next_stamp = curr_stamp + burst_idt*1000000 + curr_jitter*1000000
          burst_cnt=1
          first_burst = False
        else:
          next_stamp = curr_stamp + idt*1000000 + curr_jitter*1000000
       
    else:
      next_stamp = curr_stamp + idt*1000000 + curr_jitter*1000000
    #sleep time in seconds

    next_stamp = stop_stamp if next_stamp > stop_stamp else next_stamp
    sleep_time = (next_stamp - curr_stamp)/1000000000
  
    time.sleep(sleep_time)

  if config == None:
    break
  
msg=b"EXIT"

if l4type=="udp":
  s.sendto(msg,(ue_ip,port))
elif l4type=="tcp":
  s.sendall(msg)

if ue_id == 1:
  lts = open("/app/cell-client/last_ts","w")
  print(stop_stamp, file=lts)
  fts.close()

s.close()
