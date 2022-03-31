import argparse

def main():
  # request broker -s s_port -p p_port
  # example broker -s 9000 -p 9000
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

  print(arguments)

if __name__ == "__main__":
  main()