echo -n "Enter in URL: "
read URL
python3 url.py --wordlist sitemap.txt --targeturl $URL 
