import argparse
import time

def main():
  # request publisher -i ID -r sub_port -h broker_IP -p port [-f command_file]
  # example publisher -i p1 -r 8200 -h 127.0.0.1 -p 9000 -f publisher1.cmd
  arguments = {}

  # declare the desire arguments
  parser =  argparse.ArgumentParser(description='Publisher arguments', add_help=False, usage='publisher.py -i publisher_ID -r publisher_port -h broker_IP -p broker_port -f command_file')
  parser.add_argument('-i', nargs=1, required=True) # publisher id
  parser.add_argument('-r', nargs=1, required=True) # port of the publisher
  parser.add_argument('-h', nargs=1, required=True) # IP address of the broker
  parser.add_argument('-p', nargs=1, required=True) # port of the broker
  parser.add_argument('-f', nargs=1) # command_file
  
  # get the arguments
  args = parser.parse_args()
  file = ''
  
  # save arguments to a dictionary 
  arguments['id'] = args.i[0]
  arguments['pub_port'] = args.r[0]
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
      item[0] -> number of seconds that the publisher should wait after connecting in order to execute that command
      item[1] -> command to be executed : pub for publishing
      item[2] -> topic that the publisher wants to publish
      item[3:] -> message (each item after position 3 is a word of the message) 
      """""
      item = line.split() # split the each line where 
      
      # number of seconds that the user will wait until the command execution
      time.sleep(int(item[0]))

      # based on the declared action, call the pertinent function
      if item[1] == 'pub':
        publish(item[2], item[3:])
      else :
        print("Wrong action in the " + arguments['command_file'])

def publish(topic, msg_list):
  print(topic)
  msg = ' '.join([str(item) for item in msg_list]) # list comprehension into a string
  print(msg)

if __name__ == "__main__":
  main()