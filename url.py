#HTTP URL Brute Forcer
import threading
import urllib.request
import queue
import sys

arguments = sys.argv
successful_attempts = []
extensions = [".xml", ".html", ".php"]
threads = 20
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko; Google Page Speed Insights) Chrome/27.0.1453 Safari/537.36"

#Script Usage Instructions
def usage():
    print(f"""
    HTTP Brute Forcer Script Usage:
    python3 {arguments[0]} --wordlist </path/to/file> --targeturl <http://url>
    python3 {arguments[0]} --wordlist </path/to/file> --resumefrom <some_word> --targeturl <http://url>
    Optional: Use --resumefrom flag to resume from a word in the wordlist file.
    This is useful for any interruptions.
    """)
    sys.exit(0)

#Takes a word file and builds a word queue object. You can resume a word in the file
#by using the --resumefrom flag in the script
def build_word_list(word_list_file, resume_word):
    fd = open(word_list_file, "rb")
    word_list = fd.readlines()
    fd.close()

    if len(word_list):
        word_queue = queue.Queue()
        if not resume_word:
            for word in word_list:
                word = word.rstrip().decode("utf8")
                word_queue.put(word)
        else:
            resume_found = False
            for word in word_list:
                word = word.rstrip().decode("utf8")
                if resume_found:
                    word_queue.put(word)
                if word == resume_word:
                    resume_found = True
        return word_queue
    return None

#Takes the word queue and builds an attempt list for each attempt. Then, each entry
#in the attempt list (brute) is tried against the target URL/path. If the response
#is successful, we print the output and add to our successful attempts list.
def brute_forcer(word_queue, target_url, extensions):
    while not word_queue.empty():
        attempt_list = []
        attempt = word_queue.get()

        if "." in attempt:
            attempt_list.append("/" + attempt)
            if extensions:
                for extension in extensions:
                    attempt_no_extension = attempt.split(".")[0]
                    attempt_extension = attempt_no_extension + extension
                    if attempt != attempt_extension:
                        attempt_list.append("/" + attempt_extension)
            else:
                attempt_list.append("/" + attempt)
        else:
            attempt_list.append("/" + attempt + "/")

        for brute in attempt_list:
            url = target_url + brute
            headers = {}
            headers["User-Agent"] = user_agent
            request = urllib.request.Request(url, headers=headers)
            try:
                response = urllib.request.urlopen(request)
                if len(response.read()):
                    if response.url not in successful_attempts:
                        successful_attempts.append(response.url)
                        print(f"[{response.code}] => {response.url}")
            except urllib.request.URLError as err:
                #if hasattr(err, "code") and err.code == 404:
                #    print(f"[{err.code}] => {url}")
                pass
try:
    if "--wordlist" == arguments[1]:
        word_list_file = arguments[2]
    if "--resumefrom" == arguments[3]:
        resume_word = arguments[4]
        if "--targeturl" ==  arguments[5]:
            target_url = arguments[6]
    else:
        resume_word = None
        if "--targeturl" ==  arguments[3]:
            target_url = arguments[4]

    if word_list_file and target_url:
        word_queue = build_word_list(word_list_file, resume_word)
        if word_queue:
            print(f"[*] Word Queue Created")
            print(f"[*] HTTP Brute Force Started")
            #Since we are bruteforcing, we have multiple threads to speed it up
            #These threads will have access to the same word queue
            for i in range(threads):
                brute_force_thread = threading.Thread(target=brute_forcer, args=(word_queue, target_url, extensions))
                brute_force_thread.start()
except:
    usage()
