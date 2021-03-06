import socket
import argparse
import time
import sys
import threading

def main():
  # request subscriber -i ID -r sub_port -h broker_IP -p port [-f command_file]
  # example python3 subscriber.py -i s1 -r 8000 -h localhost -p 9001 -f subscriber1.txt
  arguments = {}
  file = ''

  # declare the desire arguments
  parser =  argparse.ArgumentParser(description='Subscriber arguments', add_help=False, usage='subscriber.py -i subscriber_ID -r subscriber_port -h broker_IP -p broker_port -f command_file')
  parser.add_argument('-i', nargs=1, required=True) # subscriber id
  parser.add_argument('-r', nargs=1, required=True) # port of the subscriber
  parser.add_argument('-h', nargs=1, required=True) # IP address of the broker
  parser.add_argument('-p', nargs=1, required=True) # port of the broker
  parser.add_argument('-f', nargs=1) # command_file
  
  # get the arguments
  args = parser.parse_args()
  
  # save arguments to a dictionary 
  arguments['id'] = args.i[0]
  arguments['sub_port'] = args.r[0]
  arguments['broker_IP'] = args.h[0]
  arguments['port'] = args.p[0]

  if args.f == None :
    arguments['command_file'] = args.f
  else:
    arguments['command_file'] = args.f[0]
    fh = open(args.f[0])
    file = [line.rstrip() for line in fh.readlines()]
    fh.close()

  # connect to server and send and receive the data twice
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((arguments['broker_IP'], int(arguments['port'])))

  # https://stackoverflow.com/questions/54621028/send-receive-messages-at-the-same-time-socket-python
  background_thread = threading.Thread(target=receive_and_print, args=(sock,))
  background_thread.daemon = True
  background_thread.start()

  # send subscriber id so as to save the information
  sock.sendall(bytes(arguments['id'], "utf-8"))

  # if file exists
  if file != '':
    # for each line of the file, execute the appropriate action
    for line in file:
      """""
      Split each line where: 
      item[0] -> number of seconds that the subscriber should wait after connecting in order to execute that command
      item[1] -> command to be executed : sub for subscribe and unsub for unsubscribe
      item[2] -> topic that the subscriber is interested in subscribing or unsubscribing from
      """""
      item = line.split() # split the each line where 

      # based on the declared action, call the pertinent function
      if item[1] == 'sub' or item[1] == 'unsub':
        subscriberAction(sock, arguments['id'], item[0], item[1], item[2])
      else :
        print("Wrong action in the " + arguments['command_file'])
  
  # when finishing with the file - if user sent it - then wait from publisher for more commands from the keyboard ex. s1 sub #hello
  while True:
    try:
      # read from command line the next action
      str = input().split()

      # check if user typed 3 arguments
      if len(str) != 3:
        print("Please type all the neccessary info ex. SUB_ID COMMAND TOPIC")
      else:
        if str[1] == 'sub' or str[1] == 'unsub' and str[0] == arguments['id']:
            subscriberAction(sock, str[0], 0, str[1], str[2])
        elif str[0] != arguments['id']:
          print("You cannot subscribe/unsubscribe another user")
        else :
          print("Wrong action in the " + arguments['command_file'])
    except KeyboardInterrupt:
      sock.close()
      sys.exit(0)



def subscriberAction(sock, sub_id, waitTime, action, topic):
  # number of seconds that the user will wait until the command execution
  print("Sending the action: " + action +" to topic " + topic + "... Please wait!" )
  time.sleep(int(waitTime))
  
  while True:
    # send action to broker
    sock.sendall(bytes(sub_id + ":" + action + "," + topic +  "\n", "utf-8"))

    # receive the data
    received = str(sock.recv(1024), "utf-8")
    print("Received: " + received)
    break

def receive_and_print(sock):
  for message in iter(lambda: sock.recv(1024).decode(), ''):
    print(message)

if __name__ == "__main__":
  main()