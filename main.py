import sqlite3
import datetime
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
@app.route("/<path:path>")
def ipaddress(path=None):
    try:
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            ip_addr = request.environ['REMOTE_ADDR']
        else:
            ip_addr = request.environ['HTTP_X_FORWARDED_FOR'].split(",")[0]
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("INSERT INTO logs (ip, datetime, useragent) VALUES(?, ?, ?);", (ip_addr, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') ,request.headers['User-Agent']))
        con.commit()
        con.close()
        print(f"Host: {request.headers['Host']}\nURL: {request.url}\nClient IP: {ip_addr}\nUser-Agent: {request.headers['User-Agent']}")
        return ip_addr
    except Exception as err:
        print(f"Error getting ipaddress : {err}")
        return "Error"
    
app.run(host="0.0.0.0", port="3124", use_reloader=True)