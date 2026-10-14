import os, sqlite3
from pathlib import Path
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from flask import Flask, request, redirect, render_template_string, flash
base=Path(os.environ.get("LOCALAPPDATA",str(Path.home())))/"AdwaaERP"
base.mkdir(parents=True,exist_ok=True)
db=base/"data.sqlite3"
app=Flask(__name__)
app.secret_key=os.environ.get("SECRET_KEY","local-prototype")
def connect():
 c=sqlite3.connect(str(db));c.row_factory=sqlite3.Row;return c
with connect() as c:
 c.executescript("""CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY,sku TEXT UNIQUE NOT NULL,name TEXT NOT NULL,price INTEGER NOT NULL,stock INTEGER NOT NULL DEFAULT 0);
 CREATE TABLE IF NOT EXISTS invoices(id INTEGER PRIMARY KEY,customer TEXT NOT NULL,created TEXT NOT NULL,total INTEGER NOT NULL);""")
def page(title,body,**ctx):
 html="""<!doctype html><html lang="ar" dir="rtl"><meta charset="utf-8"><title>أضواء قوة المحرك</title><style>body{font:18px Tahoma,Arial;background:#f3f5f9;color:#172944;margin:0}header{background:#122642;color:white;padding:24px}nav a{color:#fff;margin-left:25px}main{max-width:1100px;margin:32px auto;background:white;padding:32px;border-radius:14px}input,button{padding:12px;margin:7px;border:1px solid #ccd2da;border-radius:6px}button{background:#bd9546;color:white;cursor:pointer}table{width:100%;border-collapse:collapse}td,th{border-bottom:1px solid #ddd;padding:12px;text-align:right}</style><header><h2>شركة أضواء قوة المحرك</h2><nav><a href="/">الرئيسية</a><a href="/products">الأصناف</a><a href="/invoices">الفواتير التجريبية</a></nav></header><main><h2>"""+title+"""</h2>"""+body+"""</main></html>"""
 return render_template_string(html,**ctx)
@app.route("/")
def home():
 with connect() as c:
  p=c.execute("SELECT count(*) FROM products").fetchone()[0]
  i=c.execute("SELECT count(*) FROM invoices").fetchone()[0]
 return page("لوحة التحكم","<p>عدد الأصناف: {{p}} | عدد الفواتير التجريبية: {{i}}</p><p>هذه نسخة أولية محلية وليست نظام فوترة إلكترونية معتمدًا.</p>",p=p,i=i)
@app.route("/products",methods=["GET","POST"])
def products():
 if request.method=="POST":
  try:
   price=int((Decimal(request.form["price"])*100).quantize(Decimal("1"),rounding=ROUND_HALF_UP))
   stock=int(request.form["stock"])
   if price<0 or stock<0: raise ValueError()
   with connect() as c:c.execute("INSERT INTO products(sku,name,price,stock) VALUES(?,?,?,?)",(request.form["sku"].strip(),request.form["name"].strip(),price,stock))
  except Exception:
   return page("خطأ","<p>تعذر إضافة الصنف. تحقق من البيانات ورمز الصنف الفريد.</p><a href='/products'>العودة</a>")
  return redirect("/products")
 with connect() as c:rows=[dict(x) for x in c.execute("SELECT * FROM products ORDER BY id DESC")]
 return page("إدارة الأصناف","""<form method="post"><input name="sku" placeholder="رمز الصنف" required><input name="name" placeholder="اسم الصنف" required><input name="price" type="number" step=".01" min="0" placeholder="السعر بالريال" required><input name="stock" type="number" min="0" placeholder="المخزون" required><button>إضافة الصنف</button></form><table><tr><th>الرمز</th><th>الصنف</th><th>السعر</th><th>المخزون</th></tr>{% for r in rows %}<tr><td>{{r.sku}}</td><td>{{r.name}}</td><td>{{'%.2f'|format(r.price/100)}}</td><td>{{r.stock}}</td></tr>{% endfor %}</table>""",rows=rows)
@app.route("/invoices",methods=["GET","POST"])
def invoices():
 if request.method=="POST":
  try:
   total=int((Decimal(request.form["total"])*100).quantize(Decimal("1"),rounding=ROUND_HALF_UP))
   if total<0:raise ValueError()
   with connect() as c:c.execute("INSERT INTO invoices(customer,created,total) VALUES(?,?,?)",(request.form["customer"],datetime.now().isoformat(timespec="seconds"),total))
  except Exception:return page("خطأ","<p>تعذر تسجيل الفاتورة التجريبية.</p>")
  return redirect("/invoices")
 with connect() as c:rows=[dict(x) for x in c.execute("SELECT * FROM invoices ORDER BY id DESC")]
 return page("سجل فواتير تجريبي","""<p>تنبيه: لا تصدر هذه الشاشة فواتير ضريبية رسمية.</p><form method="post"><input name="customer" placeholder="العميل" required><input name="total" type="number" step=".01" min="0" placeholder="الإجمالي بالريال" required><button>تسجيل تجريبي</button></form><table><tr><th>العميل</th><th>التاريخ</th><th>الإجمالي</th></tr>{% for r in rows %}<tr><td>{{r.customer}}</td><td>{{r.created}}</td><td>{{'%.2f'|format(r.total/100)}}</td></tr>{% endfor %}</table>""",rows=rows)
@app.route("/health")
def health():return {"status":"ok","mode":"prototype"}
