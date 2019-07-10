import sys
import time
import socket

def process_packet(ue_id,stamp,msg):
  decoded = msg.decode('utf-8').rstrip('\n').rstrip('\x00')
  if decoded.startswith("EXIT"):
    return True
  else:
    print (ue_id,stamp, decoded, len(msg))
    return False

if len(sys.argv) < 4:
  print ("Usage: server.py <interface> <ip> <port> tcp|udp")
  print(time.time_ns())
  print(time.time_ns())
  exit(1)

interface = sys.argv[1]
ip = sys.argv[2]
port = int(sys.argv[3])
l4type = sys.argv[4]
ue_id = "".join(filter(type(interface).isdigit,interface))

s = None

if l4type == "tcp":
  s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_TCP,socket.TCP_MAXSEG,1000)
elif l4type =="udp":
  s = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
else:
  print ("INVALID L4 TYPE.")
  exit(1)

s.bind((ip,port))
s.setsockopt(socket.SOL_SOCKET, 25, str(interface+'\0').encode('utf-8'))

conn =None

if l4type == "tcp":
  s.listen(1)
  conn, addr = s.accept()
  msg = bytearray(0)


while True:
  addr = None
  incomplete = False
  exit = False
  
  if l4type == "tcp":
    new_msg = conn.recv(1024)
    msg += new_msg
    if len(new_msg) == 0:
      break
  elif l4type =="udp":
    msg,addr = s.recvfrom(1024)

  stamp = time.time_ns()

  if l4type == "tcp" and not msg:
    break

  next_msg = bytearray()

  if l4type == "tcp":
    incomplete = True
    pointer = 0
    next_msg = msg
    for i in range(0,len(msg)):
      if msg[i] == b"\n"[0]:
        incomplete = False
        if i != len(msg) -1:
          next_msg = msg[i+1:]
          proc_msg = msg[pointer:i+1]
          exit = process_packet(ue_id,stamp,proc_msg)
          pointer = i + 1
          incomplete = True
          assert exit == False
    msg = msg[pointer:]

  if not incomplete:
    exit = process_packet(ue_id,stamp,msg)
    next_msg = bytearray()

  if exit:
    break

  msg = next_msg
  assert len(msg)==0 or msg[-1] != b"\n"[0]

s.close()

