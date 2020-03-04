from subprocess import Popen
import sys

filename = 'main.py'

while True:
    print("STIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIL")
    print(f'\nSTARTING {filename}')
    p = Popen('python3 ' + filename, shell=True)
    p.wait()