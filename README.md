/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"


brew install python3

brew install git

git clone https://github.com/ChrisPF123/sitemap.git

cd ~/Documents

sudo vi ~/.bash_profile

source .bash_profile

alias sitemap='~/Documents/sitemap/sitemap.sh'

sudo chmod 777 sitemap.sh
sudo chmod 777 url.py
