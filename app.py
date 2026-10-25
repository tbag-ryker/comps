import os, json, sqlite3, secrets, hmac
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from http.cookies import SimpleCookie
from pathlib import Path

ROOT=Path(__file__).parent
HOTELS=['Hotel Don Fernando de Taos','Hampton Inn Taos','Sagebrush Inn','Hotel Willa','El Monte Sagrado','Historic Taos Inn','Taos Valley Lodge','Super 8 Taos']
DB=os.environ.get('RATES_DB',str(ROOT/'rates.sqlite3'))
PASSWORD=os.environ.get('DASHBOARD_PASSWORD')
SESSIONS={}
def connect():
    c=sqlite3.connect(DB)
    c.execute('CREATE TABLE IF NOT EXISTS rates (hotel TEXT, stay TEXT, amount REAL, status TEXT, source TEXT, checked TEXT, PRIMARY KEY(hotel,stay))')
    return c
class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt,*args): pass
    def send(self,status,body,kind='application/json',cookie=None):
        data=body.encode(); self.send_response(status)
        self.send_header('Content-Type',kind); self.send_header('Content-Length',str(len(data)))
        self.send_header('Cache-Control','no-store'); self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Content-Security-Policy',"default-src 'self'; style-src 'self'; script-src 'self'; frame-ancestors 'none'")
        if cookie: self.send_header('Set-Cookie',cookie)
        self.end_headers(); self.wfile.write(data)
    def authorized(self):
        try:
            cookies=SimpleCookie(self.headers.get('Cookie','')); token=cookies.get('session')
            return token and SESSIONS.get(token.value,0)>datetime.now().timestamp()
        except Exception: return False
    def do_GET(self):
        if self.path in ['/', '/style.css','/app.js']:
            name={'/':'index.html','/style.css':'style.css','/app.js':'app.js'}[self.path]
            return self.send(200,(ROOT/'static'/name).read_text(),{'/':'text/html','/style.css':'text/css','/app.js':'text/javascript'}[self.path])
        if not self.authorized(): return self.send(401,'{}')
        if self.path!='/api/rates': return self.send(404,'{}')
        today=datetime.now(ZoneInfo('America/Denver')).date()
        dates=[str(today+timedelta(days=i)) for i in range(8)]
        with connect() as c:
            c.row_factory=sqlite3.Row
            rows=[dict(r) for r in c.execute('SELECT * FROM rates WHERE stay BETWEEN ? AND ?', (dates[0],dates[-1]))]
        self.send(200,json.dumps(dict(hotels=HOTELS,dates=dates,rates=rows)))
    def do_POST(self):
        # Same-origin requests only; reject cross-origin browser writes.
        origin=self.headers.get('Origin')
        if origin and origin.split('://')[-1]!=self.headers.get('Host'): return self.send(403,'{}')
        try:
            length=int(self.headers.get('Content-Length',0))
            if length>16384: return self.send(413,'{}')
            data=json.loads(self.rfile.read(length))
        except Exception: return self.send(400,'{}')
        if self.path=='/api/login':
            if not hmac.compare_digest(str(data.get('password','')),PASSWORD): return self.send(401,'{}')
            token=secrets.token_urlsafe(32); SESSIONS[token]=datetime.now().timestamp()+28800
            secure='; Secure' if os.environ.get('COOKIE_SECURE')=='1' else ''
            return self.send(200,'{}',cookie=f'session={token}; HttpOnly; SameSite=Strict; Path=/; Max-Age=28800'+secure)
        if not self.authorized(): return self.send(401,'{}')
        if self.path=='/api/logout': return self.send(200,'{}',cookie='session=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0')
        if self.path!='/api/rates': return self.send(404,'{}')
        try:
            assert data['hotel'] in HOTELS
            stay=datetime.strptime(data['stay'],'%Y-%m-%d').date().isoformat()
            status=data['status']; assert status in ['available','sold_out','unavailable']
            amount=float(data['amount']) if status=='available' else None
            assert amount is None or 0<amount<100000
            source=str(data['source']).strip(); assert source and len(source)<2000
        except Exception: return self.send(400,json.dumps({'error':'Provide a valid hotel, date, rate/status and source.'}))
        with connect() as c:
            c.execute('INSERT OR REPLACE INTO rates VALUES (?,?,?,?,?,?)',(data['hotel'],stay,amount,status,source,datetime.now(ZoneInfo('America/Denver')).isoformat()))
        self.send(200,'{}')
if __name__=='__main__':
    if not PASSWORD or len(PASSWORD)<16: raise SystemExit('Set DASHBOARD_PASSWORD to at least 16 characters.')
    connect().close()
    ThreadingHTTPServer((os.environ.get('HOST','127.0.0.1'),int(os.environ.get('PORT','8000'))),Handler).serve_forever()
