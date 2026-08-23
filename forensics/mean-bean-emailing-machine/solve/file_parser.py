import subprocess
import json

with open("../bean_co_email_logs.json", "r") as f:
    data = json.load(f)

for message in data:
    if message["attachment"] is None:
        continue

    # there is an attachment of some kind

    subprocess.run(f"echo {message["data"]} | base64 -d > temp.txt", shell=True)
    filetype = subprocess.check_output("file temp.txt", shell=True)

    # check for junk data
    if filetype == b"temp.txt: data\n":
        subprocess.run("rm temp.txt", shell=True)
        continue

    subprocess.run("mv temp.txt $(md5sum temp.txt | cut -d' ' -f1)", shell=True)