from flask import Flask, render_template,request
from database import load_articles, load_users,load_orders, if_present, quantity_added,quantity_removed,deleted, order_settled


myapp= Flask(__name__)

@myapp.route("/")
def login():
    return render_template("login.html")

@myapp.route("/home/<int:id>")
def home_page(id):
    id=id
    user=load_users(id)
    products=load_articles()
    print (user)
    return render_template("test.html",items=products,users=user)

@myapp.route("/home/<int:id>/cart", methods=["post","get"])
def cart_page(id):
    if request.method=="POST":
        product=request.form.get("product",False)
        if (product!=False):
            if_present(id,product)

        product_added=request.form.get("added",False)
        if(product_added!=False):
            quantity_added(id,product_added)
     
        product_removed=request.form.get("removed",False)
        if(product_removed!=False):
            quantity_removed(id,product_removed)
        product_deleted=request.form.get("deleted",False)
        if(product_deleted!=False):
            deleted(id,product_deleted)

    user=load_users(id)
    order=load_orders(id)
    sum=0
    for x in order:
        sum=sum+(x['price']*x['quantity'])  
    return render_template("cart.html",users=user, orders=order,subtotal=sum)

@myapp.route("/home/checkout", methods=["post","get"])
def checkout():
    if (request.method=="POST"):
         cid=request.form.get("cid",False)
    if (cid!=False):
        order_settled(cid)
        return render_template("checkout.html",cid=cid)



if __name__ == "__main__":
    myapp.run(debug=True)
