

## quick setup

```bash
mkdir ~/.scripts
cd ~/.scripts
git clone git@github.com:Ben-Owen-3183/bytejstool.git
cd bytejstool
# you might need to give execute permissions to scripts
chmod +x bcpull.sh
chmod +x bcpush.sh
```


Add .scripts to your path
```bash
# Don't forget to restart terminal for this change to take effect
echo 'export PATH="$HOME/.scripts:$PATH"' > ~/.zshrc
```

Open the tools settings
```
vim ~/.scripts/bytejstool/src/settings.py
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

You now be able to run the following commands
```bash
# to pull a component to a project run
bcpull ComponentName working_project
# to push from the project to byte run
bcpush ComponentName working_project
```

