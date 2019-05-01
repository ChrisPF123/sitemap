/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"


brew install python3

brew install git

cd ~/Documents

git clone https://github.com/ChrisPF123/sitemap.git

sudo vi ~/.bash_profile

alias sitemap='~/Documents/sitemap/sitemap.sh'

source .bash_profile

cd ~/Documents/sitemap

sudo chmod 777 sitemap.sh
sudo chmod 777 url.py
