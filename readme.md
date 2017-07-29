##Installation

1. Install Python 3.
2. Open a terminal window.
2. Run: `sudo pip3 install django`
3. Run: `sudo pip3 install requests`
4. Run: `sudo pip3 install ecdsa`
5. Run: `sudo pip3 install bcrypt`
6. Run `sudo pip3 install gunicorn`
7. If, forwhatever reason, pip is not installed refer to [here.](https://pip.pypa.io/en/stable/installing/)
8. Clone/download this repository.

##Starting your node


9. Change your directory to this repository.
10. Run: `sudo gunicorn -b "0.0.0.0:4848" LedgerBoard.wsgi`
11. Open another terminal window and change your directory to this repository.
12. Find the IP of whatever machine you are on.
13. Run: `sudo python3 manage.py startup your.ip:4848`

Now you can leave your node to run in peace. It will update itself to the current chain and will then function normally.

##Mining
1. Run `sudo python3 manage.py mine your.ip:4848`

If you wish to mine on multiple cores then open additional windows and run the above command.
`

 
 