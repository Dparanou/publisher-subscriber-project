import sys
import argparse
import time

def main():
  # request subscriber -i ID -r sub_port -h broker_IP -p port [-f command_file]
  # example subscriber -i s1 -r 8000 -h 127.0.0.1 -p 9000 -f subscriber1.cmd
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

  # if file exists
  if file != '':
    # for each line of the file, execute the appropriate action
    for line in file:
      """""
      Split each line where: 
      item[0] -> number of seconds that the subscriber should wait after connecting in order to execute that command
      item[1] -> command to be executed : sub for subscribe and unsub for unsubscribe
      item[3] -> topic that the subscriber is interested in subscribing or unsubscribing from
      """""
      item = line.split() # split the each line where 
      
      # number of seconds that the user will wait until the command execution
      time.sleep(int(item[0]))

      # based on the declared action, call the pertinent function
      if item[1] == 'sub':
        subscribe(item[2])
      elif item[1] == 'unsub':
        unsubscribe(item[2])
      else :
        print("Wrong action in the " + arguments['command_file'])


def subscribe(topic):
  print(topic)

def unsubscribe(topic):
  print(topic)

if __name__ == "__main__":
  main()