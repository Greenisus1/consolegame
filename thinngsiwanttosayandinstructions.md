# consolegame
enjoy full version coming soon also i am back 
NOTES:
only works on linux and raspberry pi so far






how to RUN!









// STEP 1

first check if you have it
run in term 

python3 --version

version should say "Python 3.11.2" or higher
If it’s outdated or missing, update your system and install Python 3:
first run in a new term
sudo apt update
in the same term run this now
sudo apt upgrade
and then run this
sudo apt install python3 -y

Want the latest version (e.g., Python 3.12+)?     ______________________________________________________LATEST VERSION___________________________________________________
run this LOOOOOOOOOOOOONG script in a new term

sudo apt install -y build-essential libssl-dev zlib1g-dev \
libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev \
libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev tk-dev

then now 
wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz     
// run this
tar -xvf Python-3.12.0.tgz
// run this next
cd Python-3.12.0
// verify it worked
if it failed go to where it says latest version in big text and go and repeat the prosess

**if that fails try this**
**do-not-run-this-line-this-is-assistance-they-are-my-comments** run each line in the same term 

ls /usr/local/bin/python3.12

**do-not-run-this-line-this-is-assistance-they-are-my-comments** If that file exists, try running it directly:
/usr/local/bin/python3.12 --version
**do-not-run-this-line-this-is-assistance-they-are-my-comments** 🔁 If It Doesn’t Exist...
**BLANK LINE THERE WAS AN ERROR DO NOT RUN THIS**
**do-not-run-this-line-this-is-assistance-they-are-my-comments** The install step may have failed. You can try re-running the final install commands:

cd Python-3.12.0

sudo make altinstall

NOW CLOSE THE TERM AND STOP RUNNING EACH SCRIPT
Now step 2 ---------------------------------------------------------------------------------**STEP 2 IF YOU HAVE PYTHON COME HERE**-------------------------------------------------------------------------------



now download consolegame.py from this repo

open up a new term 

**on raspberry pi**

//first run

stty -ixon   # (to disable flow-control if needed)

//then run

python3 /home/USERNAMEHERE/Downloads/consolegame.py    ------------- //**note:replace USERNAMEHERE with your username go to my repo finding your pi username for info (i am posting it below soon)**

piusernamefinder link -------------------------------------------------------------------------> [[CONTENT_LOCKED]] _****if it says content locked then it will be fixed report it please****_

**ON LINUX**
COMING SOON


 







