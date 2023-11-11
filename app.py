from flask import Flask,render_template,request,redirect,url_for,session

app = Flask(__name__, template_folder="templates")

from models import *
li=[]
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    li.clear()
    return redirect(url_for('index'))
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('landing.html')

@app.route('/userLogin',methods=['GET','POST'])
def userLogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        signin=Usersignin(email, password)
        if signin is not None:
            li.append(email)
            return redirect(url_for('user_dashboard', userid=signin.id))
        else:
            return render_template('userLogin.html', error="Invalid user credentials entered.")

    msg = request.args.get('msg')
    return render_template('userLogin.html')
@app.route('/userSignup',methods=['GET','POST'])
def userSignup():
    if request.method=='POST':
        fname= request.form['fname']
        lname = request.form['lname']
        mobile = request.form['mobile']
        email = request.form['email']
        password = request.form['password']
        if validateSignup(email): #Used to check if user exists or not
            signup(fname=fname,lname=lname, mobile = mobile, email=email, password=password)
            return render_template('userLogin.html', msg='User added Successfully')
        else:
            return render_template('userSignup.html', error='User already exists')

    return render_template('userSignup.html')

@app.route('/adminLogin',methods=['GET','POST'])
def adminLogin():
    if request.method == 'POST':
        email = request.form['email']

        password = request.form['password']

        if Adminsignin(email, password):
            li.append(email)
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('adminLogin.html', error="Invalid user credentials entered.")


    return render_template('adminLogin.html')

@app.route('/admin_dashboard', methods=['GET',"POST"])
def admin_dashboard():
    category_items=fetch_category()
    product_items=fetch_all_products()
    if len(li)!=0:
        return render_template('admin_dashboard.html',category_items=category_items, product_items=product_items)
    else:
        return redirect(url_for('adminLogin'))
@app.route('/admin_dashboard/Create_Category', methods=['GET',"POST"])
def createCat():
    if request.method == 'POST':
        name = request.form['name']
        print(name)
        if validateCategory(name):
            print(True)
            AddCategory(name)
            return render_template('add_category.html', msg="Added Succesfully")
        else:
            return render_template('add_category.html', error='Category already exists')
    return render_template('add_category.html')

@app.route('/admin_dashboard/Delete_Category', methods=['GET',"POST"])

def deleteCat():
    category_items=fetch_category()
    if len(category_items) !=0:
        if request.method == 'POST':
            name = request.form['category']
            msg=DeleteCategory(name)
            category_items = fetch_category()
            product_items = fetch_all_products()
            return render_template('admin_dashboard.html', msg=msg,  category_items=category_items, product_items=product_items)
        return render_template('deleteCat.html', dropdown_items=category_items)
    else:
        return render_template('admin_dashboard.html', error="No categories are available!!")

@app.route('/admin_dashboard/Edit_Category', methods=['GET',"POST"])

def editCat():
    category_items=fetch_category()
    if len(category_items) != 0:
        if request.method == 'POST':
            newName = request.form['name']
            oldName= request.form['category']
            msg=EditCategory(newName, oldName)
            category_items = fetch_category()
            product_items = fetch_all_products()
            return render_template('admin_dashboard.html', msg=msg, category_items=category_items,product_items=product_items)


        return render_template('editCat.html', dropdown_items=category_items)
    else:
        return render_template('admin_dashboard.html', error="No categories are available!!")


@app.route('/admin_dashboard/Edit_Product', methods=['GET', 'POST'])
def edit_product():
    product_items = fetch_all_products()
    if len(product_items) != 0:
        if request.method == 'POST':
            try:
                old_product_name=request.form['old_name']
                new_product_name = request.form['new_name']
                manufacture_date = request.form['manufacture_date']
                expiry_date = request.form['expiry_date']
                rate_per_unit = request.form['rate_per_unit']
                quantity = request.form['quantity']
                print(old_product_name, new_product_name, manufacture_date, expiry_date, rate_per_unit, quantity)
                if ProductUpdate(old_product_name, new_product_name, manufacture_date, expiry_date, rate_per_unit, quantity):
                    product_items = fetch_all_products()
                    return render_template('editProd.html', dropdown_items=product_items,
                                           msg="Product updated successfully", error=False)

            except Exception as e:
                session.rollback()
                return render_template('editProd.html', dropdown_items=product_items, msg="An error occurred", error=True)

        return render_template('editProd.html', dropdown_items=product_items, msg=None, error=False)
    return render_template('editProd.html', error="No categories are available!!")


@app.route('/admin_dashboard/Create_Product', methods=['GET',"POST"])
def createProduct():
    dropdown_items = fetch_category()
    if len(dropdown_items) != 0:
        if request.method == 'POST':
            name = request.form['name']
            manufacture_date=request.form['manufacture_date']
            expiry_date = request.form['expiry_date']
            rate_per_unit = request.form['rate_per_unit']
            category_id= request.form['category']
            quantity= request.form['quantity']
            if validateProduct(name, category_id):
                AddProduct(name, manufacture_date, expiry_date, rate_per_unit, category_id, quantity)
                return render_template('add_product.html',msg="Added Succesfully",dropdown_items=dropdown_items )
            else:
                return render_template('add_product.html', error='Product already exists', dropdown_items=dropdown_items)
        return render_template('add_product.html',dropdown_items=dropdown_items)
    return render_template('admin_dashboard.html', error="No categories are available!!")

@app.route('/admin_dashboard/Delete_Product/', methods=['GET', 'POST'])
def deleteProduct():
    category_items = fetch_category()
    if len(category_items) != 0:
        if request.method == 'POST':
            catId = request.form['category']
            print(catId)
            return redirect(url_for('deleteProduct2', catId=catId))

        return render_template('delete_product.html', dropdown_items=category_items)
    return render_template('admin_dashboard.html', error="No categories are available!!")

@app.route('/admin_dashboard/Delete_Product2/<catId>', methods=['GET', 'POST'])
def deleteProduct2(catId):
    product_items = prodCat(catId)
    category_items = fetch_category()
    prodCheck=session.query(Product).filter(Product.category_id==catId).all()
    if len(prodCheck) !=0:
        if request.method == 'POST':
            product=request.form['product']
            msg = DeleteProduct(product)
            return render_template('delete_product.html', msg=msg, dropdown_items=fetch_category())

        return render_template('delete_product2.html', dropdown_items=product_items, catId=catId)
    return render_template('delete_product.html', error="No products are available!!", dropdown_items=category_items)

@app.route('/user_dashboard/<int:userid>', methods=['GET', 'POST'])
def user_dashboard(userid):
    u1=session.query(User).filter(User.role=='user', User.id==userid).first()
    if u1 is not None:
        user=session.query(User).filter(User.id==userid).first()
        name=user.fname
        print(name)
        category_items = fetch_category()
        product_items = fetch_all_products()
        cart_value= len(session.query(Cart).filter(Cart.user_id==userid).all())

        if request.method=='POST':
            search_query = searchProduct(request.form['query'])
            category_items = session.query(Category).all()
            filtered_category_items = []


            if search_query:
                for item in search_query:
                    filtered_category_items.append(fetch_product_cat(item.category_id))
                filtered_category_items = set(filtered_category_items)
                return render_template('user_dashboard.html', name=name, userid=userid,category_items=filtered_category_items,product_items=search_query, cart_value=cart_value)

            if not search_query:
                    return render_template('user_dashboard.html', name=name, userid=userid, msg="No search found", cart_value=cart_value)

        return render_template('user_dashboard.html',name=name, userid=userid, category_items=category_items,product_items=product_items, cart_value=cart_value)
    else:
        return redirect(url_for('index'))

@app.route("/cart/<userid>", methods=['GET', 'POST'])
def cart(userid):
    cartitem=cartProducts(userid)
    prod=[]
    print(cartitem)
    for cart in cartitem:
       prod.append(cart_prod(cart))
    cartQuantity=session.query(Cart).filter(Cart.user_id==userid).all()
    total_price=cartPrice(prod)

    return render_template('cart.html', product_items=prod, cartQuantity=cartQuantity, userid=userid, total_price=total_price)
@app.route("/buyAll/<int:userid>")
def buy(userid):
    if buyAll(userid):
        return redirect(url_for('user_dashboard', userid=userid, msg="Products purchased Successfully"))
    else:
        return redirect(url_for('cart', userid=userid))

@app.route("/edit_quantity/<int:userid>/<int:product_id>", methods=['GET', 'POST'])
def edit_quantity(userid, product_id):
    if request.method=='POST':
        quantity=request.form['quantity']
        updateQuantity(userid, product_id, quantity)

    return redirect(url_for("cart", userid=userid))
@app.route('/delete_product/<int:userid>/<int:product_id>', methods=['GET', 'POST'])
def delete_product(userid,product_id):
    deleteProductCart(userid, product_id)
    category_items = fetch_category()
    product_items = fetch_all_products()
    cart_value = len(session.query(Cart).filter(Cart.user_id == userid).all())
    if cart_value!=0:
        return redirect(url_for("cart", userid=userid))
    else:
        return render_template('user_dashboard.html', userid=userid, category_items=category_items,
                               product_items=product_items, cart_value=cart_value,)


@app.route('/Add_to_cart/<userid>/<product_id>')
def add_to_cart(userid, product_id):
    prodAdded=addcart(userid, product_id)
    category_items = fetch_category()
    product_items = fetch_all_products()
    cart_value = len(session.query(Cart).filter(Cart.user_id == userid).all())
    return render_template('user_dashboard.html', userid=userid, category_items=category_items,product_items=product_items, cart_value=cart_value,msg=f"Product {prodAdded} Added to Cart")

@app.route("/profile/<int:userid>")
def profile(userid):
    u1=session.query(User).filter(User.id==userid, User.role=='user').first()
    profile_items = profileItems(userid)
    if len(profile_items)!=0:
        return render_template("profile.html",profile_items=profile_items, user=u1, items=True)
    else:
        return render_template("profile.html",user=u1, items=False)

@app.route("/summary")
def summary():
    purchaseItems=purchase_items()
    userItems=user_items()
    if len(purchaseItems)!=0:
        return render_template("summary.html", purchase_items=purchaseItems,user_items=userItems, items=True)
    else:
        return render_template("summary.html",items=False)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)