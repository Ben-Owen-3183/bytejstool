HEADER = '\033[95m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
INFOBLUE = '\033[94m'
DANGER = '\033[31m'
ENDC = '\033[0m'

def print_w(text):
  print(f"{WARNING}{text}{ENDC}")

def print_e(text):
  print(f"{FAIL}{text}{ENDC}")

def print_s(text):
  print(f"{OKGREEN}{text}{ENDC}")

def print_h(text):
  print(f"{HEADER}{text}{ENDC}")

def print_i(text):
  print(f"{INFOBLUE}{text}{ENDC}")

def print_d(text):
  print(f"{DANGER}{text}{ENDC}")