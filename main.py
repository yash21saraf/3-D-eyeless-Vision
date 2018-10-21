import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import matplotlib
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
import cv2
import urllib
import urllib.request
import time
import os
import tkinter as tk
from tkinter import ttk
import abcdabcd
from datetime import datetime
import subprocess

from utils import label_map_util

from utils import visualization_utils as vis_util


procs = []
while True:
    if(os.stat("Iplist.txt").st_size !=0):
        f = open("Iplist.txt",'r+')
        a=f.read()
        f.truncate(0)
        f.close()
        a=a.encode()
        print(a)
        proc = subprocess.Popen([sys.executable, "objectt.py"],stdin=subprocess.PIPE)
        proc.stdin.write(a)
        proc.stdin.close()
        procs.append(proc)
