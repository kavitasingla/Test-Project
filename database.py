import sqlalchemy
import pymysql
from sqlalchemy import create_engine,text

connection_string = 'mysql+pymysql://gp8dkxwezyz4dekrmy4f:pscale_pw_KXvpP15c1YdPphnEgEqIO2E1uY0JiSskCiaziRD2PPw@ap-southeast.connect.psdb.cloud/project'
ssltext={"ssl":
        { "ssl_ca": "/etc/ssl/cert.pem"}}

engine=create_engine(connection_string, connect_args=ssltext)

def load_articles():
    with engine.connect() as conn1:
        result=conn1.execute(text("select * from articles"))
        list=result.all()
        articles=[]
        for row in list:
            articles.append(row._asdict())
    return articles

def load_users(id):
    with engine.connect() as conn2:
        result=conn2.execute(text("select * from users where customer_id= :userid"), {"userid":id})
        list=result.all()
        users=[]
        for row in list:
            users.append(row._asdict())
        
        if len(users)==0:
            return None
        else:
            return users[0]
        

def load_orders(id):
    with engine.connect() as conn2:
        result=conn2.execute(text("select articles.product,orders.quantity,articles.price from orders,articles where orders.customer_id= :userid and orders.product=articles.product"), {"userid":id})
        list=result.all()
        orders=[]
        for row in list:
            orders.append(row._asdict())
        return orders
        
def add_orders(id,product):
    with engine.connect() as conn2:
        result=conn2.execute(text("insert into orders values(:userid,:product,1)"), {"userid":id,"product":product})

        
        
def if_present(id,product):
    with engine.connect() as conn2:
        result=conn2.execute(text("select * from orders where customer_id= :id AND product= :products"),{"id":id,"products":product})
        list=result.all()
        if (len(list)>0):
            result1=conn2.execute(text("UPDATE orders set quantity=quantity+1"))
        else:
            add_orders(id,product)


def quantity_added(id,product):
    with engine.connect() as conn2:
        result=conn2.execute(text("update orders  set quantity=quantity+1 where customer_id= :id AND product= :products"),{"id":id,"products":product})

def quantity_removed(id,product):
    with engine.connect() as conn2:
        result=conn2.execute(text("update orders  set quantity=quantity-1 where customer_id= :id AND product= :products"),{"id":id,"products":product})
        result1=conn2.execute(text(" select quantity from orders where customer_id= :id AND product= :products"),{"id":id,"products":product})
        result2=result1.all()
        x=result2[0]
        if (x[0]<1):
            conn2.execute(text(" delete from orders where customer_id= :id AND product= :products"),{"id":id,"products":product})

def deleted(id,product):
    with engine.connect() as conn2:
        conn2.execute(text(" delete from orders where customer_id= :id AND product= :products"),{"id":id,"products":product})

def order_settled(cid):
    with engine.connect() as conn2:
        conn2.execute(text(" delete from orders where customer_id= :id "),{"id":cid})