

## setup

create

Fill in settings for your workspace
```python
# home folder relative to user
HOME_PATH = os.path.expanduser('~')
# directors where projects can be found
PROJECT_PATHS = [
  f"{HOME_PATH}/path/to/projects",
]
# directory where byte is stored
BYTE_PATH = f"{HOME_PATH}/path/to/byte/dir"
```

```bash
# to run
python3 main.py <action> <ComponentName> <working_project>
```

