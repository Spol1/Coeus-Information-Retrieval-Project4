from flask import Flask, render_template, request
import urllib.request
import plotly
import plotly.graph_objects as go
import pandas as pd
import pymongo
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import json

app = Flask(__name__,template_folder='templates')

client = MongoClient("mongodb://localhost:27017/")
db = client["tweetsDB"]

from app import views

