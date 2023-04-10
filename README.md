# Activity Tracker

Local only, manual entry activity logging program. The puprose of this program is to cater to thos who would like to track some sort of metric (distance run each day, number of hours of piano practice, number of cheeseburgers consumed, etc.) but would trade the convenience of automated entry and cloud connectivity for complete control of local files in an application which doesn't know how to access the internet.

Data is saved as text in `.json` format.

# To do
* Produce stand alone excutables for different operating systems (This feature will correspond to first release).
* Enable plotting multiple fields simultaneously (inlcuding multiple fields across multiple items).

# Usage

From command line: `python3 activitytracker.py`

The user will be presented with a blank interface, to get start added an item by clicking `Add item`, the item name can be any nonempty string. The fields for each item are shown by clicking on the item name. Each item can contain a number of fields which are create by clicking `Add field`. Fields have three components, the name which can be any nonempty string, the value which can be any numeric value, and the unit which can be any string (including empty). Once a field is created it cannot be deleted and the only part which can be edited is the value. To commit changes to values, click `Update fields` otherwise the changes will be reverted if the view is changed.

The viewed day can be changed using the calendar at the top left, when opening a file or starting a new project, the view is set to the current day according to the system. When a new field is added to an item, it will only be added on the current day. When a day which has never been used is selected, it is populated with all of the items and fields (initialised to zero) of the most recent nonfuture day which has entries.

On the right, a field of the currently selected item can be slected for plotting from a drop down menu at the bottom. The time range for the plot is also set by a drop down menu. For the `Custom` date range, the two calendars at the top set the start and end dates (there is probably a more elegant way to do this). If two items have fields with matching names, only the field corresponding to the currently selected item is shown.

# Development
This project was hacked together in one weekend for personal use and to learn `PyQt5` and will probably not be developed much (see to do list above) but contributions are welcome.

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

# License

Copyright © 2023 Craig S. Chisholm

Version - 0.1.0

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <a href="https://www.gnu.org/licenses/">https://www.gnu.org/licenses</a>.
