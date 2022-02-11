import subprocess
import glob
images = 'imgs/'
subprocess.run(['ls'])
subprocess.run(['sudo', 'python3', 'segment.py', '%s'%images]) 
