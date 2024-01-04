bif [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/NobiDeveloper/Nobita-Filter-Bot.git /Nobita-Filter-Bot
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /Nobita-Filter-Bot
fi
cd /Nobita-Filter-Bot
pip3 install -U -r requirements.txt
echo "Starting...."
python3 bot.py
