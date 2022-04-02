 #!/usr/bin/python3

import argparse
from ast import arg
from pydoc_data.topics import topics
import socket
import threading
import sys

HOST = "localhost"

def main():
  # request broker -s s_port -p p_port
  # example broker -s 9001 -p 9000
  arguments = {}

  # declare the desire arguments
  parser =  argparse.ArgumentParser(description='Publisher arguments', add_help=False, usage='broker.py -s subscribers_port -p publishers_port')
  parser.add_argument('-s', nargs=1, required=True) # subscribers port
  parser.add_argument('-p', nargs=1, required=True) # publishers port
  
  # get the arguments
  args = parser.parse_args()
  
  # save arguments to a dictionary 
  arguments['subscribers_port'] = args.s[0]
  arguments['publishers_port'] = args.p[0]

  try:
    threading.Thread(target=pubthread, args=(arguments['publishers_port'],)).start()
    threading.Thread(target=subthread, args=(arguments['subscribers_port'],)).start()
  except KeyboardInterrupt as msg:
    sys.exit(0)


# thread for publisher
def pubthread(P_PORT):
  # set up for publisher
  pub_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  pub_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
  pub_sock.bind((HOST, int(P_PORT)))
  pub_sock.listen(10)
  print("Broker listening Pubs on %s %d" %(HOST, int(P_PORT)))

  conn, addr = pub_sock.accept()
  print("Pub Connected : " + addr[0] + ":" + str(addr[1]))

  while True:
    try:
      data = conn.recv(1024).strip().decode()
      topic = data.rpartition(':')[0]
      msg = data.rpartition(':')[2]

      if len(msg) != 0:
        print("Received from Pub-> topic: " + topic + " , message: " + msg)
        conn.sendall(bytes("OK", "utf-8"))
    except:
      print("Pub Disconnected")
      break

# thread for subscriber
def subthread(S_PORT):
  # set up for subscriber
  sub_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sub_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
  sub_sock.bind((HOST, int(S_PORT)))
  sub_sock.listen(10)
  print("Broker listening Subs on %s %d" %(HOST, int(S_PORT)))

  conn, addr = sub_sock.accept()
  print("Sub Connected : " + addr[0] + ":" + str(addr[1]))

  while True:
    try:
      data = conn.recv(1024).strip().decode()
      sub_id = data.rpartition(':')[0]
      action = data.rpartition(':')[2].rpartition(',')[0]
      topic = data.rpartition(':')[2].rpartition(',')[2]

      if len(str(data)) == 0:
        print("No message")
      print("Received from Sub: " + str(data))

      file = open("brokerDb.txt", "r")
      fileLines = [line.rstrip() for line in file.readlines()]
      file.close()

      line = sub_id + " " + topic
      
      if line not in fileLines:
        if action == 'sub':
          file1 = open("brokerDb.txt", "a")
          file1.write(line + "\n")
          file1.close()
          conn.sendall(bytes("Subscribed successfully", "utf-8"))
        elif action == 'unsub':
          conn.sendall(bytes("Not subscribes yet to this topic", "utf-8"))
      else:
        if action == 'sub':
          conn.sendall(bytes("Already in this topic", "utf-8"))
        elif action == 'unsub':
          file1 = open("brokerDb.txt", "w")
          fileLines.remove(line)
          newLines = ("\n".join(fileLines))
          print(newLines)
          file1.write(newLines)
          file1.close()
          conn.sendall(bytes("Unsubscribed successfully", "utf-8"))

      # send the sub some data
      # conn.sendall(bytes("\nsome data for you", "utf-8"))
    except:
      print("Sub Disconnected")
      break

if __name__ == "__main__":
  main()