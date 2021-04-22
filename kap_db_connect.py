import pyodbc
from sqlalchemy import create_engine, MetaData, Table, select

import numpy as np
import pandas as pd
from datetime import datetime, timedelta, date

with open("../kap_db_info.txt") as f:
    lines = f.readlines()
    server = lines[0].strip()
    db = lines[1].strip()
    user = lines[2].strip()
    pwd = lines[3].strip()
    dns = lines[4].strip()

class Kapodbc:

    def __init__(self, server=server, db=db, user=user, pwd=pwd):
        self.server = server
        self.db = db
        self.user = user
        self.pwd = pwd

    def connect(self):

        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=' + self.server + ';DATABASE=' + self.db + ';UID=' + self.user + ';PWD=' + self.pwd)
        cursor = conn.cursor()

        return conn, cursor


class Kapsqlalchemy:
    def __init__(self, user=user, pwd=pwd, dns = dns):
        self.user = user
        self.pwd = pwd
        self.dns = dns

    def create_engine(self):
        conn = create_engine('mssql+pyodbc://' + self.user + ':' + self.pwd + '@' + self.dns)
        return conn