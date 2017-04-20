#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: le4f.net

from flask import Flask, request, redirect, url_for, send_file, render_template, g, make_response
from werkzeug.utils import secure_filename
from cStringIO import StringIO
from collections import Counter
from scapy.all import *
import os, sys, time, math, re
import simplejson, sqlite3
import pyshark
import chartkick
from flask.ext.sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = 'server/pcapfile/'
ALLOWED_EXTENSIONS = set(['pcap', 'pcapng', 'cap'])
DATABASE = 'server/db/db.sqlite'

app = Flask(__name__)
app.jinja_env.add_extension("chartkick.ext.charts")
app.config.from_object(__name__)
app.secret_key = '\xac=\x0f\xee\x88\x9f\xb9\xfaF\x04\x93\xc2\x12\xc2\x9fG\t\xa1\xf2t\x80\xe5\x1c['
# print(__name__)
import views
import func
