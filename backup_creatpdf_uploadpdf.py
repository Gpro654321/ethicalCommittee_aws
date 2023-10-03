import subprocess

subprocess.run("python3 ./iec_certbot.py", shell=True)
subprocess.run("python3 ./iec_fileuploader.py", shell=True)
