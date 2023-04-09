# Activity Tracker

Local only, manual entry activity logging program

# To do
* Load and save data (format: JSON? HDF5?)
* Detect unsaved changes before closing or loading new file
* Select different days
* Add radio button to plot selected field in avaliable time ranges
* Produce stand alone excutables for different operating systems (This feature will correspond to first release)
* Enable custom time range for plotting

# Development
Set up virtual environment:

## Linux + macOS
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Windows
```
python3 -m venv venv
venv\Scripts\activate
python3 -m pip install -r requirements.txt
```
