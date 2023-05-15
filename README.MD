
## NOTE: i've not ran through this install process, so take it with a pinch of salt.

## quick setup

```bash
mkdir ~/scripts
cd ~/scripts
git clone git@github.com:Ben-Owen-3183/bytejstool.git
cd bytejstool
# you might need to give execute permissions to scripts
chmod +x bcpull
chmod +x bcpush
```


Add scripts/bytejstool to your path
```bash
# open zshrc
vim ~/.zshrc
# the following
export PATH="$HOME/scripts/bytejstool:$PATH"
# save file then run the following to reload zshrc (or restart terminal)
source ~/.zshrc 
```

Open the tools settings
```
vim ~/scripts/bytejstool/src/settings.py
```
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

You should now be able to run the following commands
```bash
# to pull a component to a project run
bcpull ComponentName working_project
# to push from the project to byte run
bcpush ComponentName working_project
```

