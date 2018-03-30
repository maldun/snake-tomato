# snake_tomato
Simple Python app for Pomodoro Method

## Version
1.1

## Requirements
Python 2.7+ (3.6 tested)

## License
GPL V3

## Install
Just copy the folder or use git in a shell with
```bash
git clone https://github.com/maldun/snake_tomato.git snake_tomato
```

## Start
Change to directory of install.
Call either
```bash
python /path/to/snake_tomato/snake_tomato.py
```
or as module
```bash
cd /path/to/snake_tomato
python -m snake_tomato
```
On Linux one can also make it executable
```bash
cd /path/to/snake_tomato
chmod +x snake_tomato.py
./snake_tomato.py
```
At the first run an empty scratch.txt and a new snake_tomato.cfg will be created.
The scratch file can be changed in snake_tomato.cfg if you don't want to loose it,
or want a different file.

## Usage

### Timer

Default time unit is minutes.
The Field Working time contains
your desired work time interval.
The pause field contains the length 
of your pause.
 
When you press start the work timer
will count down till it reaches 00:00.
then a message window will inform you
that you should take a break.
after clicking OK the break counter 
starts to remind you of your remaining time.
When you are ready for a new work run hit 
start anew.

If you want to stop you can hit reset any time.
It will set back the timer to 00:00.

### ToDo List

Enter anything in the empty input line and hit the
"+"-Button. This item will be added to the list.
When you have finished the specific task mark it
and hit the "-"-button. It will be deleted.

Your todo list will be saved in your scratch file
after closing the app.

### Preferences

#### Scratch
File type: desired file type of the scratch (default .txt)
scratch file: File to write and read your scratch.

#### Defaults

unit: The used time unit in seconds. Default is 60 (min) for 
e.g. hours you would use 3600.
default work time: default timer setting for work interval.
default pause time: default pause timer setting.

## Notes
* TKinter can be sometimes be painful to work with when threads are involved.
If you observe lags this may be occouring because of some timing operation. 
Don't think to much about it.
* The app is VERY minimalistic by design, but it can be called everywhere 
when at least Python is available.
* Found a bug? Have some ideas? Just put it on the github page.
