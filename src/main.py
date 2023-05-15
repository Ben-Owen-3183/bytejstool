#!/usr/bin/env python3

import settings
from file_manager import directory_exists
import traceback
from print_helpers import *
from validation import validate_settings, validate_user_args
from bytemejs import ByteMeJS 
from custom_exceptions import *
import sys

if settings.DANGEROUS_DEBUG_DELETE:
  print_d("!!! DANGEROUS DEBUG DELETE ENABLED !!!")

if settings.DEBUG:
  print_w("DEBUG MODE ENABLED")

def main():
  validate_settings()
  validate_user_args()

  action = sys.argv[1]
  target_component = sys.argv[2]
  target_project = sys.argv[3]
  component_path = f"{settings.BYTE_PATH}/{settings.COMPONENT_PATH}/{target_component}"

  if not directory_exists(component_path):
    raise BMJException(f"Could not find \"{target_component}\" in byte")

  if action == "pull":
    bytemejs = ByteMeJS(target_component, target_project, component_path)
    bytemejs.pull()
  elif action == "push":
    bytemejs = ByteMeJS(target_component, target_project, component_path)
    bytemejs.push()

  print_s("\njob's a good'un")

try:
  main()
except Exception as e:
  print_h("\nOh dear...\nSomething went wrong...\nMost likely it is your fault!")
  print_h("\nexample: command <component name> <target project name>\n")
  print_e(e)
  if settings.PRINT_STACK_TRACE:
    print_e(traceback.format_exc())
  exit(1)


