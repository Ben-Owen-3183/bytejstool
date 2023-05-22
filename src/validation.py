import settings
import sys
from custom_exceptions import *
from file_manager import directory_exists


def validate_user_args():
  if len(sys.argv) < 2:
    raise BMJException("You must provide an action")
  if sys.argv[1] != 'push' and sys.argv[1] != 'pull':
    raise BMJException(f"{sys.argv[1]} is not a valid action. Either push or pull.")
  if len(sys.argv) < 3:
    raise BMJException("You must provide a component name")
  if len(sys.argv) < 4:
    raise BMJException("You must provide a target project")  

def validate_settings():
  if not settings.HOME_PATH:
    raise BMJException("You must set a home path")
  if not settings.PROJECT_PATHS:
    raise BMJException("You must set project paths")
  if not settings.BYTE_PATH:
    raise BMJException("You must set a byte path")
  if not directory_exists(settings.BYTE_PATH):
    raise BMJException(f"Byte folder was not found at: {settings.BYTE_PATH}")
  if not settings.COMPONENT_PATH:
    raise BMJException("You must set a component path")
  if not settings.HELPER_DIR_PATH:
    raise BMJException("You must set a helper dir path")
  if not settings.VIEW_DIR_PATH:
    raise BMJException("You must set a view dir path")
  if not settings.PREPENDED_IMPORT_PATH_REGEX:
    raise BMJException("You must set a prepended import path regex")
  if not settings.IMPORT_REGEX:
    raise BMJException("You must set an import regex")
  if not settings.IMPORT_REPLACE:
    raise BMJException("You must set an import replace")
  if not settings.JS_FILE_EXTENSIONS:
    raise BMJException("You must set js file extensions")
  if not settings.COMPONENT_SUFFIX:
    raise BMJException("You must set a component suffix")
  if not settings.REACT_CALL_SINGLE_QUOTE_REGEX or not settings.REACT_CALL_DOUBLE_QUOTE_REGEX:
    raise BMJException("You must set a react call regex")
  if not settings.LOCAL_BYTE_GEM_REGEX:
    raise BMJException("You must set a local byte gem regex")
  if not settings.REMOTE_BYTE_GEM_REGEX:
    raise BMJException("You must set a remote byte gem regex")