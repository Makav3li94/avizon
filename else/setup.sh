#!/usr/bin/env bash

echo 'Install prerequisites (step 1)'
apt update && apt install python3-pip python3-venv redis git cron  -y
if [ $? == 0 ]; then
  echo 'Successfully installed'
else
  echo 'An error occurred while installing the prerequisites'
  exit
fi

echo 'start redis service'
systemctl start redis.service
if [ $? == 0 ]; then
  echo 'redis servie started'
else
  echo 'service starting failed'
  exit
fi

echo "Creating avizon directory (step 2)"
mkdir -p /var/www/avizon && cd /var/www/avizon

echo 'Pulling the repository (step 3)'
git init
git remote add origin https://github.com/Makav3li94/avizon.git
git pull origin master
if [ $? != 0 ]; then
  echo 'could not clone the repository'
  exit
fi

echo 'Create virtual env (step 4)'
python3 -m venv /var/www/avizon/venv
if [ $? != 0 ]; then
  echo "VENV didn't created"
fi

echo 'Installing project dependencies (step 5)'
cd /var/www/avizon && source /var/www/avizon/venv/bin/activate && pip install wheel && pip install avizon_core/ avizon_menu/ && deactivate
if [ $? != 0 ]; then
  echo "Dependencies doesn't installed correctly"
  exit
fi

echo 'Create avizon service (step 6)'
ln -s /var/www/avizon/else/avizon.service /etc/systemd/system/
if [ $? != 0 ]; then
  echo 'Creating service was failed'
  exit
fi

echo 'Reload services and start avizon.service (step 7)'
systemctl daemon-reload
sudo systemctl enable avizon.service
sudo systemctl start avizon.service
if [ $? != 0 ]; then
  echo "avizon service didn't started"
  exit
fi

echo "make avizon as a command (step 8)"
ln -s /var/www/avizon/else/avizon /usr/local/bin/ && chmod +x /usr/local/bin/avizon
if [ $? != 0 ]; then
  echo "failed to add avizon to PATH environment variables"
  exit
fi