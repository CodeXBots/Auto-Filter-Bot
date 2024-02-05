if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone hhttps://github.com/NobiDeveloper/Nobita-Filter-Bot/tree/main.git /Nobita-Filter-Bot
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /Nobita-Filter-Bot
fi
cd /Nobita-Filter-Bot
pip3 install -U -r requirements.txt
echo "Starting...."
python3 bot.py