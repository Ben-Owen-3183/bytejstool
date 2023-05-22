import os

# home folder relative to user
HOME_PATH = os.path.expanduser('~')
# directors where projects can be found
PROJECT_PATHS = [
  f"{HOME_PATH}/superbyte/projects",
]
# directory where byte is stored
BYTE_PATH = f"{HOME_PATH}/superbyte/projects/byte"











LOGGING = True
# debooger
DEBUG = False
# leave false unless you know what you're doing
DANGEROUS_DEBUG_DELETE = False
# stacks of traces
PRINT_STACK_TRACE = False
# path from project to components
COMPONENT_PATH = 'app/javascript/components'
# relative path to helpers folder
HELPER_DIR_PATH = 'app/helpers'
# relative path to views folder
VIEW_DIR_PATH = 'app/views'
# regex to target the '../' parts in import statements
PREPENDED_IMPORT_PATH_REGEX = r"(\.\.\/)+"
# regex to match import statements that need pointing to byte
IMPORT_REGEX = fr"^\b(import)\b.*\b(from)\b.*{PREPENDED_IMPORT_PATH_REGEX}[A-Z].*$"
# what to replace the import path with
IMPORT_REPLACE = "@cogitorteam/byte/dist/"
# js file extensions to look for when editing files
JS_FILE_EXTENSIONS = ['js', 'jsx', 'ts', 'tsx']
# Prefix for component name for new folder and varaiable/function/class names 
COMPONENT_SUFFIX = 'ByteClone'
# regex to target the react_component('<ComponentName>', ..., ...)
REACT_CALL_SINGLE_QUOTE_REGEX = r".*react_component.*\'$$$COMPONENT_NAME$$$\'.*"
REACT_CALL_DOUBLE_QUOTE_REGEX = r".*react_component.*\'$$$COMPONENT_NAME$$$\'.*"
# local regex to target gem code in gemfile in project
LOCAL_BYTE_GEM_REGEX = r"gem.*byte.*,.*path:.*\.\./byte"
# remote regex to target gem code in gemfile in project
REMOTE_BYTE_GEM_REGEX = r"source.*https://rubygems.pkg.github.com/cogitorteam.*do"
# if true it will print logs when trying to bundle project
SHOW_BUNDLE_LOGS = False

if DEBUG: 
  HOME_PATH = 'testing'
  PROJECT_PATHS = ['testing/working_code']
  BYTE_PATH = 'testing/working_code/byte'
elif DANGEROUS_DEBUG_DELETE:
  DANGEROUS_DEBUG_DELETE = False