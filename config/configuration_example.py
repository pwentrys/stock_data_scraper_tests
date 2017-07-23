from os.path import join
import sys


NAME = 'App'
IP = 'QUARTET'
PORT = 9001
PROJECT = sys.path[0]
RESOURCES = join(PROJECT, 'resources')
STATIC = join(RESOURCES, 'static')
TEMPLATES = join(RESOURCES, 'templates')
DEBUG = True
SESSION_LIFETIME = 1
THREADED = True
