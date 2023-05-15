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
    self.react_call_regex = settings.REACT_CALL_REGEX.replace('$$$COMPONENT_NAME$$$', self.target_component)
    self.react_call_verify_regex = settings.REACT_CALL_REGEX.replace('$$$COMPONENT_NAME$$$', self.new_component_name)
    container_id_command = f"docker ps | grep \"app\" | grep \"{self.target_project}\""
    self.project_docker_container_id = subprocess.getoutput(container_id_command).split(" ")[0]

  def pull(self):
    self.build_new_component_folder_structure()
    self.clone_component()
    self.replace_all_react_calls()
    self.enable_local_byte_gem()
    self.bundle_project()
    
  def push(self):
    paths = find_all_child_files(self.new_component_path)
    for path in paths:
      self.add_new_directories()
      self.push_cloned_component_to_byte(path)

  def add_new_directories(self):
    directories = find_all_child_directories(self.new_component_path)
    directories = sorted(directories, key=lambda path: len(path.split("/")))
    for directory in directories:
      byte_directory_path = self.project_to_byte_path(directory)
      if not directory_exists(byte_directory_path):
        print_i(f"New directory added {byte_directory_path}")
        make_directory(byte_directory_path)

  def push_cloned_component_to_byte(self, path):
    depth = len(path.split(self.new_component_path)[-1].split("/")) - 1
    print_i(f"Copying Contents of {path}")
    with open(path, 'r') as cloned_file:
      original_file_path = self.project_to_byte_path(path)
      original_file = None
      if not file_exists(original_file_path):
        print_s(f"- Adding new file {original_file_path}")
        original_file = create_empty_file(original_file_path)
      else:
        original_file = get_file(original_file_path)
      lines = cloned_file.read().splitlines()
      lines = self.replace_component_name(lines, self.new_component_name, self.target_component)
      lines = self.revert_import_paths(lines, depth)
      overwrite_file(original_file, lines)

  def revert_import_paths(self, lines, depth):
    for i, line in enumerate(lines):
      if re.search(settings.IMPORT_REPLACE, line):
        lines[i] = line.replace(settings.IMPORT_REPLACE, ("../" * depth))
        print_s(f" - line {i} import reverted to {lines[i]}")
    return lines

  def byte_to_project_path(self, path):
    path = path.replace(settings.BYTE_PATH, self.target_project_path)
    path = path.replace(self.target_component, self.new_component_name)
    return path

  def project_to_byte_path(self, path):
    path = path.replace(self.target_project_path, settings.BYTE_PATH)
    path = path.replace(self.new_component_name, self.target_component)
    return path

  def build_new_component_folder_structure(self):
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
      make_directory(self.byte_to_project_path(directory))

  def is_js_file(self, path):
    if path.split('.')[-1] in settings.JS_FILE_EXTENSIONS:
      return True
    return False

  def clone_component(self):
    print_i(f"\nCloning component to target project...")
    
    byte_file_paths = find_all_child_files(self.target_component_path)
    for bf_path in byte_file_paths:
      with open(bf_path, 'r') as f:
        print_i(f"Cloning file: {bf_path}")
        lines = f.read().splitlines()
        lines = self.replace_imports(lines)
        lines = self.replace_component_name(lines, self.target_component, self.new_component_name)
        create_file(self.byte_to_project_path(bf_path), lines)

  def replace_component_name(self, lines, target, replace):
    for i, line in enumerate(lines):
      if re.search(target, line):
        lines[i] = line.replace(target, replace)
        print_s(f" - line {i} changed to \"{lines[i]}\"")
    return lines

  def replace_imports(self, lines):
    for i, line in enumerate(lines):
      if re.match(settings.IMPORT_REGEX, line):
        lines[i] = re.sub(settings.PREPENDED_IMPORT_PATH_REGEX, settings.IMPORT_REPLACE, line)
        print_s(f" - line {i} changed to \"{lines[i]}\"")
    return lines

  def replace_all_react_calls(self):
    file_paths = []
    for ruby_file_path in self.react_call_paths:
      file_paths = file_paths + find_all_child_files(ruby_file_path)
    
    print_i(f"\nSearching for `react_component(...)` calls in {len(file_paths)} files")
    for path in file_paths:
      self.search_file_for_react_calls(path)

  def search_file_for_react_calls(self, path):
    file = get_file(path)
    lines = file.read().splitlines()
    for i, line in enumerate(lines):
      if re.match(self.react_call_regex, line) and not re.match(self.react_call_verify_regex, line):
        lines[i] = line.replace(self.target_component, self.new_component_name)
        print_i(f"React call found in {path}")
        print_s(f" - line {i} will be changed to \"{lines[i]}\"")
    overwrite_file(file, lines)

  def enable_local_byte_gem(self):
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

  def bundle_project(self):
    print_i(f"\nAttempting to bundle project...")
    command = f"docker exec -it -w /workspaces/{self.target_project} {self.project_docker_container_id} bundle"
    if settings.DEBUG:
      print_w(f"Pretending to run bundle command: {command}")
    else:
      print_i(f"Running bundle command: {command}")
      bundle_logs = subprocess.getoutput(command)
      if settings.SHOW_BUNDLE_LOGS:
        print_i(bundle_logs)

