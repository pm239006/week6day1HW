from flask import Blueprint, render_template, request, flash, redirect

#internal imports
from dealership_shop.models import Product, Customer, ProdOrder, Order, db, product_schema, products_schema
from dealership_shop.forms import ProductForm

site = Blueprint('site', __name__, template_folder='site_templates') #telling your blueprint where to load the html files 


#create our CREATE route
@site.route('/shop/create', methods = ['GET', 'POST'])
def create():

    createform = ProductForm()

    if request.method == 'POST' and createform.validate_on_submit():

        # try: 
        car_make = createform.car_make.data
        car_model = createform.car_model.data
        car_year = createform.car_year.data
        desc = createform.description.data
        image = createform.image.data
        price = createform.price.data
        quantity = createform.quantity.data 

        shop = Product(price, quantity, image, desc,car_year="",car_model="",car_make="")

        db.session.add(shop)
        db.session.commit()

        flash(f"You have successfully added a vechicle", category='success')
        return redirect('/')

        # except:
        #     flash("We were unable to process your request. Please try again", category='warning')
        #     return redirect('/shop/create')
        
    return render_template('create.html', form=createform)

#create our first route
@site.route('/')
def shop():

    shop = Product.query.all()
    customers = Customer.query.all()
    orders = Order.query.all()

    shop_stats = {
        'cars': len(shop),
        'sales': sum([order.order_total for order in orders]), #order totals was total cost of that specific order
        'customers' : len(customers)
    }

    return render_template('shop.html', shop=shop) #stats=shop_stats) #basically displaying our shop.html page 



# create our CREATE route
@site.route('/shop/update/<id>', methods = ['GET', 'POST'])
def update(id):

    updateform = ProductForm()
    product = Product.query.get(id) #WHERE clause WHERE product.prod_id == id 

    if request.method == 'POST' and updateform.validate_on_submit():

        try: 
            product.car_make = updateform.car_make.data
            product.car_model = updateform.car_model.data
            product.car_year = updateform.car_year.data
            product.description = updateform.description.data
            product.set_image(updateform.image.data, updateform.name.data) #calling upon that set_image method to set our image!
            product.price = updateform.price.data
            product.quantity = updateform.quantity.data 

            

            db.session.commit() #commits the changes to our objects 

            flash(f"You have successfully updated your list", category='success')
            return redirect('/')

        except:
            flash("We were unable to process your request. Please try again", category='warning')
            return redirect('/shop/update')
        
    return render_template('update.html', form=updateform, product=product)


@site.route('/shop/delete/<id>')
def delete(id):

    product = Product.query.get(id)

    db.session.delete(product)
    db.session.commit()

    return redirect('/')

