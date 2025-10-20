import requests
import re
import os
import datetime
from bs4 import BeautifulSoup

URL = "https://simplicity.kiwi/simplicity-first-home-loans"
regexPattern = r"\d+\.\d{2}\%"
rateSaved = ""
rateCurrent = ""

#Get Saved Rate from file
with open('Simplicity-Rates.md', 'rb') as f:
    try:  # catch OSError in case of a one line file 
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
    except OSError:
        f.seek(0)
    rateSaved = f.readline().decode().split()[3]
f.close()

print(rateSaved)

#Get Current Rate from simplicity website and parse output
r = requests.get(URL, verify=False)
soup = BeautifulSoup(r.text, 'html.parser')
h2 = soup.find_all('h2')
for h in h2:
    if re.match(regexPattern, h.text):
        rateCurrent = h.text
        print(h.text)

#Compare Saved and Current rates to see if they have changed.
if(rateCurrent != rateSaved):
    with open('Simplicity-Rates.md', 'a') as f:
        f.writelines("| " + datetime.date.today().isoformat() + " | " + rateCurrent + ' |\n')
    f.close()
