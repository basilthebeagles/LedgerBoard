## Explanation and Information
Refer to [here](http://f-stack.com/LedgerBoard.html). 







## Installation

1. Install Python 3.5 or above.
2. Open a terminal window.
2. Run: `sudo pip3 install django`
3. Run: `sudo pip3 install requests`
4. Run: `sudo pip3 install ecdsa`
5. Run: `sudo pip3 install bcrypt` If this doesn't work use `sudo apt-get install bcrypt` And if that doesn't work use `sudo apt-get install libffi6 libffi-dev` and then `sudo pip3 install bcrypt` again.
6. Run `sudo pip3 install gunicorn`
7. If, for whatever reason, pip is not installed refer to [here.](https://pip.pypa.io/en/stable/installing/)
8. Clone/download this repository.

## Starting your node


9. Change your directory to this repository.
10. Make sure that port 4848 is forwarded.
10. If Linux/Mac: Run: `sudo gunicorn -b "0.0.0.0:4848" LedgerBoard.wsgi` otherwise run `python3 manage.py runserver 0.0.0.0:4848`
11. Open another terminal window and change your directory to this repository.
12. Find the IP of whatever machine you are on.
13. Run: `sudo python3 manage.py StartUp your.ip:4848` Run this 3-4 times for good measure. 

The following steps are not necessarily necessary but they may be useful. They involve setting up an automated command so that the node regularly updates it's connected nodes and blocks; just incase it missed a few.

Create a file that contains the following text:

`#!/bin/bash`

`cd /path/to/LedgerBoard/`

`sudo python3 manage.py StartUp your.ip:4848`

1. Make it executable with: `chmod +x file`
2. Then use `sudo crontab -e` to write: `*/20 * * * * /path/to/LedgerBoard/file.extension`
3. Save the file.


 Now you can leave your node to run in peace. It will update itself to the current chain and will then function normally.




## Mining
1. Run `sudo python3 manage.py mine your.ip:4848`

If you wish to mine on multiple cores then open additional windows and run the above command.

Ignore the first 'valid block time' console output.

valid block time console output = time for node to receive a valid block, not necessarily mine one. It will specify if it has mined one


## Commands

Run `python3 manage,py addNewHost command your.ip:4848 ip.to.connect.to:4848` to manually connect to a node. 
 