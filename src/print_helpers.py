import settings

HEADER = '\033[95m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
INFOBLUE = '\033[94m'
DANGER = '\033[31m'
ENDC = '\033[0m'

def print_w(text):
  custom_print(f"{WARNING}{text}{ENDC}")

def print_e(text):
  custom_print(f"{FAIL}{text}{ENDC}")

def print_s(text):
  custom_print(f"{OKGREEN}{text}{ENDC}")

def print_h(text):
  custom_print(f"{HEADER}{text}{ENDC}")

def print_i(text):
  custom_print(f"{INFOBLUE}{text}{ENDC}")

def print_d(text):
  custom_print(f"{DANGER}{text}{ENDC}")
  
def custom_print(text):
  if settings.LOGGING:
    print(text)