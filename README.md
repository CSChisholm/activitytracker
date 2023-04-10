# Activity Tracker

Local only, manual entry activity logging program. The puprose of this program is to cater to thos who would like to track some sort of metric (distance run each day, number of hours of piano practice, number of cheeseburgers consumed, etc.) but would trade the convenience of automated entry and cloud connectivity for complete control of local files in an application which doesn't know how to access the internet.

Data is saved as text in `.json` format.

# To do
* Produce stand alone excutables for different operating systems (This feature will correspond to first release)
* Write usage documentation

# Usage

# Development
Clone repository:
`git clone https://github.com/CSChisholm/activitytracker`

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
