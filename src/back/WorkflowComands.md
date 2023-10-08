First step when working on project is to activate the virtual environment if dont have one
```
python -m venv <venv>
```
last venv is the name of the virtual environment

then activate the virtual environment on windows or linux
```
linux (bash/zsh):
source <venv>/bin/activate

windows (cmd):
<venv>/Scripts/activate.bat

windows (powershell):
<venv>/Scripts/Activate.ps1
```
Difference between Powershell and cmd is that powershell starts with PS

Now install the packages you need
```
pip install -r requirements.txt
```

Now you can start working on your project

After installing new packages, run the following command to update the requirements.txt file
```
pip freeze > requirements.txt
```
