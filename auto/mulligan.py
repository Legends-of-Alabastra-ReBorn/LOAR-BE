from subprocess import Popen
import sys

filename = 'main.py'

while run:
    print("STIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIL")
    print(f'\nSTARTING {filename}')
    p = Popen('python3 ' + filename, shell=True)
    p.wait()