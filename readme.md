## Explanation
TBC

## View the blockchain

Go to [here](http://f-stack.com/LedgerBoard-Blockchain-Information.html) to view information about 








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
10. If Linux/Mac: Run: `sudo gunicorn -b "0.0.0.0:4848" LedgerBoard.wsgi` otherwise run `python3 manage.py runserver 0.0.0.0:4848`
11. Open another terminal window and change your directory to this repository.
12. Find the IP of whatever machine you are on.
13. Run: `sudo python3 manage.py StartUp your.ip:4848` Run this 3-4 times for good measure. 

Now you can leave your node to run in peace. It will update itself to the current chain and will then function normally.

## Mining
1. Run `sudo python3 manage.py mine your.ip:4848`

If you wish to mine on multiple cores then open additional windows and run the above command.
`

## Commands

Run `python3 manage,py addNewHost command your.ip:4848 ip.to.connect.to:4848` to manually connect to a node. 
 