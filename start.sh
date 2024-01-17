bif [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/Dineshv52/Filter-pro-Bot.git /Filter-pro-Bot
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /Filter-pro-Bot
fi
cd /Filter-pro-Bot
pip3 install -U -r requirements.txt
echo "Starting...."
python3 bot.py
