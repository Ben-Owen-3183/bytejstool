import settings
from print_helpers import *
import re
import subprocess
from validation import *
from custom_exceptions import *
from file_manager import *

def find_target_project_path(target_project):
  for path in filter_invalid_project_path(target_project):
    if directory_exists(path):
      return path
  raise BMJException(f"Could not find target project {target_project} ")

def filter_invalid_project_path(target_project):
  project_paths = []
  for path in settings.PROJECT_PATHS:
    project_path = f"{path}/{target_project}"
    if directory_exists(project_path):
      project_paths.append(project_path)
  return project_paths

class ByteMeJS:
  def __init__(self, target_component, target_project, component_path):
    self.target_component = target_component
    self.target_project = target_project
    self.target_project_path = find_target_project_path(target_project)
    self.target_component_path = component_path
    self.new_component_name = f"{self.target_component}{settings.COMPONENT_SUFFIX}"
    self.new_component_path = f"{self.target_project_path}/{settings.COMPONENT_PATH}/{self.new_component_name}"
    self.react_call_paths = [
      f"{self.target_project_path}/{settings.HELPER_DIR_PATH}",
      f"{self.target_project_path}/{settings.VIEW_DIR_PATH}", 
      f"{settings.BYTE_PATH}/{settings.HELPER_DIR_PATH}",
      f"{settings.BYTE_PATH}/{settings.VIEW_DIR_PATH}"
    ]
    self.single_quote_react_call_regex = settings.REACT_CALL_SINGLE_QUOTE_REGEX.replace('$$$COMPONENT_NAME$$$', self.target_component)
    self.single_quote_react_call_verify_regex = settings.REACT_CALL_SINGLE_QUOTE_REGEX.replace('$$$COMPONENT_NAME$$$', self.new_component_name)
    self.double_quote_react_call_regex = settings.REACT_CALL_DOUBLE_QUOTE_REGEX.replace('$$$COMPONENT_NAME$$$', self.target_component)
    self.double_quote_react_call_verify_regex = settings.REACT_CALL_DOUBLE_QUOTE_REGEX.replace('$$$COMPONENT_NAME$$$', self.new_component_name)
    container_id_command = f"docker ps | grep \"app\" | grep \"{self.target_project}\""
    self.project_docker_container_id = subprocess.getoutput(container_id_command).split(" ")[0]

  def pull(self):
    # self.__build_new_component_folder_structure()
    # self.__clone_component()
    self.__replace_all_react_calls()
    # self.__enable_local_byte_gem()
    # self.__bundle_project()
    
  def push(self):
    if not directory_exists(self.new_component_path):
      raise BMJException(f"The {self.new_component_name} component clone was not found in {self.target_project}")
    paths = find_all_child_files(self.new_component_path)
    self.__add_new_directories()
    for path in paths:
      self.__push_cloned_component_to_byte(path)
    
  def __paths_to_file_names(self, paths):
    names = []
    for path in paths:
      names.append(path.split("/")[-1].split(".")[0])
    return names

  def __add_new_directories(self):
    directories = find_all_child_directories(self.new_component_path)
    directories = sorted(directories, key=lambda path: len(path.split("/")))
    for directory in directories:
      byte_directory_path = self.__project_to_byte_path(directory)
      if not directory_exists(byte_directory_path):
        print_i(f"New directory added {byte_directory_path}")
        make_directory(byte_directory_path)

  def __push_cloned_component_to_byte(self, path):
    depth = len(path.split(self.new_component_path)[-1].split("/")) - 1
    print_i(f"Copying Contents of {path}")
    with open(path, 'r') as cloned_file:
      original_file_path = self.__project_to_byte_path(path)
      original_file = None
      if not file_exists(original_file_path):
        print_s(f"- Adding new file {original_file_path}")
        original_file = create_empty_file(original_file_path)
      else:
        original_file = get_file(original_file_path)
      lines = cloned_file.read().splitlines()
      lines = self.__replace_component_name(lines, self.new_component_name, self.target_component)
      lines = self.__revert_import_paths(lines, depth)
      overwrite_file(original_file, lines)

  def __revert_import_paths(self, lines, depth):
    for i, line in enumerate(lines):
      if re.search(settings.IMPORT_REPLACE, line):
        lines[i] = line.replace(settings.IMPORT_REPLACE, ("../" * depth))
        print_s(f" - line {i} import reverted to {lines[i]}")
    return lines

  def __byte_to_project_path(self, path):
    path = path.replace(settings.BYTE_PATH, self.target_project_path)
    return path.replace(self.target_component, self.new_component_name)

  def __project_to_byte_path(self, path):
    path = path.replace(self.target_project_path, settings.BYTE_PATH)
    return path.replace(self.new_component_name, self.target_component)

  def __build_new_component_folder_structure(self):
    print_i(f"\nBuilding new component folder structure...")  
    try:
      make_directory(self.new_component_path)
    except FileExistsError:
      if settings.DANGEROUS_DEBUG_DELETE:
        dangerous_delete_directory(self.new_component_path)
        make_directory(self.new_component_path)
      else:
        raise BMJException(f"New Component Folder already exists in {self.target_component}: {self.new_component_path}")

    directories = find_all_child_directories(self.target_component_path)
    directories = sorted(directories, key=lambda path: len(path.split("/")))

    for directory in directories:
      make_directory(self.__byte_to_project_path(directory))

  def __clone_component(self):
    print_i(f"\nCloning component to target project...")
    byte_file_paths = find_all_child_files(self.target_component_path)
    local_component_names = self.__paths_to_file_names(byte_file_paths)
    for bf_path in byte_file_paths:
      with open(bf_path, 'r') as f:
        print_i(f"Cloning file: {bf_path}")
        lines = f.read().splitlines()
        lines = self.__replace_imports(lines, local_component_names)
        lines = self.__replace_component_name(lines, self.target_component, self.new_component_name)
        create_file(self.__byte_to_project_path(bf_path), lines)

  def __replace_component_name(self, lines, target, replace):
    for i, line in enumerate(lines):
      if re.search(target, line):
        lines[i] = line.replace(target, replace)
        print_s(f" - line {i} changed to \"{lines[i]}\"")
    return lines

  def __replace_imports(self, lines, local_component_names):
    for i, line in enumerate(lines):
      if re.match(settings.IMPORT_REGEX, line):
        import_component = line.split("\'")[1].split("/")[-1]
        if import_component not in local_component_names:
          lines[i] = re.sub(settings.PREPENDED_IMPORT_PATH_REGEX, settings.IMPORT_REPLACE, line)
          print_s(f" - line {i} changed to \"{lines[i]}\"")
    return lines

  def __replace_all_react_calls(self):
    file_paths = []
    for ruby_file_path in self.react_call_paths:
      file_paths = file_paths + find_all_child_files(ruby_file_path)

    print_i(f"\nSearching for `react_component(...)` calls in {len(file_paths)} files")
    for path in file_paths:
      self.__search_file_for_react_calls(path)

  def __search_file_for_react_calls(self, path):
    file = get_file(path)
    lines = file.read().splitlines()
    for i, line in enumerate(lines):
      
      single_quote_match = re.match(fr"{self.single_quote_react_call_regex}", line) 
      single_quote_verify_match = not re.match(fr"{self.single_quote_react_call_verify_regex}", line)
      double_quote_match = re.match(fr"{self.double_quote_react_call_regex}", line)
      double_quote_verify_match = not re.match(fr"{self.double_quote_react_call_verify_regex}", line)

      if (single_quote_match and single_quote_verify_match) or (double_quote_match and double_quote_verify_match):
        lines[i] = line.replace(self.target_component, self.new_component_name)
        print_i(f"React call found in {path}")
        print_s(f" - line {i} will be changed to \"{lines[i]}\"")
    overwrite_file(file, lines)

  def __enable_local_byte_gem(self):
    print_i(f"\nEnabling local byte gem...")
    gemfile_path = f"{self.target_project_path}/gemfile"
    file = get_file(gemfile_path)
    lines = file.read().splitlines()
    for i, line in enumerate(lines):
      if re.search(settings.LOCAL_BYTE_GEM_REGEX, line):
        lines[i] = lines[i].replace("#", "").strip()
      if re.search(settings.REMOTE_BYTE_GEM_REGEX, line) and not re.match(r"#", line):
        lines[i] = '#' + lines[i]
        lines[i + 1] = '#' + lines[i + 1]
        lines[i + 2] = '#' + lines[i + 2]
    overwrite_file(file, lines)

  def __bundle_project(self):
    print_i(f"\nAttempting to bundle project...")
    command = f"docker exec -it -w /workspaces/{self.target_project} {self.project_docker_container_id} bundle"
    if settings.DEBUG:
      print_w(f"Pretending to run bundle command: {command}")
    else:
      print_i(f"Running bundle command: {command}")
      bundle_logs = subprocess.getoutput(command)
      if settings.SHOW_BUNDLE_LOGS:
        print_i(bundle_logs)

