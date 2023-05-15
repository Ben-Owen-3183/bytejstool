import os
import shutil

def directory_exists(path):
  return os.path.isdir(path)

def is_directory(path):
  return os.path.isdir(path)

def file_exists(path):
  return os.path.isfile(path)

def list_dir(path):
  return os.listdir(path)

def dangerous_delete_directory(path):
  return shutil.rmtree(path)

def create_empty_file(path):
  return open(path, 'x')

def create_file(path, file_contents):
  with open(path, 'x') as f:
    f.writelines("\n".join(file_contents))
    
def make_directory(path):
  if not directory_exists(path):
    return os.mkdir(path)
  raise FileExistsError(f"Directory already exists. {path}")
  
def get_file(path):
  if file_exists(path):
    return open(path, 'r+')
  raise FileExistsError(f"File does not exist. {path}")

def overwrite_file(file, lines):
  file.seek(0)
  file.writelines("\n".join(lines))
  file.close()
  
def find_all_child_files(path):
  file_list = []
  for item in list_dir(path):
    next_path = f"{path}/{item}"
    if is_directory(next_path):
      file_list = file_list + find_all_child_files(next_path)
    else:
      file_list.append(next_path)
  return file_list

def find_all_child_directories(path):
  dir_list = []
  for item in list_dir(path):
    next_path = f"{path}/{item}"
    if is_directory(next_path):
      dir_list.append(next_path)
      dir_list = dir_list + find_all_child_directories(next_path)
  return dir_list
