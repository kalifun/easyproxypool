from datetime import datetime
from flask_apscheduler import APScheduler
from flask import current_app,Flask
from Proxy.config.config import Config
from Proxy.model.models import db,Iplist
from Proxy.tools.ipcheck.Verification import CheckIp
scheduler = APScheduler()

def SpiderProxy():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app=app)
    with app.app_context():
        print(current_app.name)
        iplist = CheckIp().AddinfotoIp()
        print(iplist)
        try:
            deletedata = Iplist.query.all()
            [db.session.delete(u) for u in deletedata]
            db.session.commit()
            for newlist in iplist:
                ip = newlist["ip"]
                port = newlist["port"]
                httptype = newlist["httptype"]
                address = newlist["address"]
                isp = newlist["isp"]
                spend = newlist["spend"]
                createtime = datetime.now()
                insertip = Iplist(ip=ip, port=port, httptype=httptype, address=address, isp=isp, spend=spend,createtime=createtime)
                print(insertip)
                db.session.add(insertip)
                db.session.commit()
        except Exception as e:
            print(e)



def registtodos():
    job = {
        'id': 'try spider ip',
        'func': 'SpiderProxy'
    }
    # result = scheduler.add_job(func=__name__ + ':' + job['func'], id=job['id'], trigger='cron', hour= '00',minute = '44')
    result = scheduler.add_job(func=__name__ + ':' + job['func'], id=job['id'], trigger='interval', minute=30)
    print(result)