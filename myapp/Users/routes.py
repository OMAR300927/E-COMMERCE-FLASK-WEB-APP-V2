from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies
from ..modules.model import Users, Products, ShoppingCart, Payment
from ..modules.services import save, delete
from ..extension import cache, oauth

import stripe



users_bp = Blueprint('users_bp', __name__, url_prefix='/users')

# User Registration
@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if not username or not password or not email:
            flash('All fields are required!', 'error')
            return redirect(url_for('users_bp.register'))
        
        existing_user = Users.query.filter((Users.username == username) | (Users.email == email)).first()
        if existing_user:
            flash('Username or email already exists!', 'error')
            return redirect(url_for('users_bp.register'))

        new_user = Users(username=username, email=email)
        new_user.set_password(password)
        save(new_user)

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('users_bp.login'))

    return render_template('register.html')


# google login
@users_bp.route('/google-login')
def google_login():
    try:
        redirect_uri = url_for('users_bp.google_authorized', _external=True)
        return oauth.google.authorize_redirect(redirect_uri, prompt='select_account')
    except Exception as e:
        flash('Google login failed. Please try again.', 'error')
        return redirect(url_for('users_bp.login'))
    

# google authorized
@users_bp.route('/google-authorized')
def google_authorized():
    token = oauth.google.authorize_access_token()

    userinfo_endpoint = oauth.google.server_metadata.get('userinfo_endpoint')
    res = oauth.google.get(userinfo_endpoint)
    user_info = res.json()

    email = user_info.get('email')
    username = user_info.get('name')

    user = Users.query.filter_by(email=email).first()
    if not user:
        user = Users(
            email=email,
            username=username,
            auth_provider='google'
        )
        save(user)

    access_token = create_access_token(identity=str(user.id))
    response = make_response(redirect(url_for('users_bp.home')))
    set_access_cookies(response, access_token)
    return response


# User Login
@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if not username or not password or not email:
            flash('All fields are required!', 'error')
            return redirect(url_for('users_bp.login'))
        
        user = Users.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=str(user.id))

            res = make_response(redirect(url_for('users_bp.home')))
            set_access_cookies(res, access_token)

            return res
        else:
            flash('Invalid username or password!', 'error')
            return redirect(url_for('users_bp.login'))


    return render_template('login.html')


# User Logout
@users_bp.route('/logout', methods=['GET'])
def logout():
    flash('You have been logged out.', 'success')
    return redirect(url_for('users_bp.login'))


# Home Page
@users_bp.route('/home', methods=['GET'])
@jwt_required()
@cache.cached(timeout=3600)
def home():
    user_id = get_jwt_identity()

    products = Products.query.all()
    return render_template('products.html', products=products)


# cart page
@users_bp.route('/my-cart', methods=['GET', 'POST'])
@jwt_required()
def my_cart():
    user_id = get_jwt_identity()

    items = ShoppingCart.query.filter_by(user_id=user_id).all()
    return render_template('cart.html', items=items)


# add to cart page
@users_bp.route('/add-to-cart/<int:product_id>', methods=['GET'])
@jwt_required()
def add_to_cart_page(product_id):
    user_id = get_jwt_identity()

    product = Products.query.get_or_404(product_id)

    return render_template('add_to_cart.html', product=product)


@users_bp.route('/add-to-cart/<int:product_id>', methods=['POST'])
@jwt_required()
def add_to_cart(product_id):
    user_id = get_jwt_identity()

    product = Products.query.get_or_404(product_id)

    quantity = request.form.get('quantity')

    if not quantity:
        flash('Quantity is required', 'error')
        return redirect(url_for('users_bp.add_to_cart_page', product_id=product_id))

    quantity = int(quantity)
    if quantity <= 0:
        flash('Quantity must be greater than zero.', 'error')
        return redirect(url_for('users_bp.add_to_cart', product_id=product_id))

    if quantity > product.amount:
        flash('Not enough stock available.', 'error')
        return redirect(url_for('users_bp.add_to_cart', product_id=product_id))
    
    existing_item = ShoppingCart.query.filter_by(user_id=user_id, product_id=product.id).first()

    if existing_item:
        existing_item.quantity += quantity
        save(existing_item)

    else:
        cart_item = ShoppingCart(
            user_id=user_id,
            product_id=product.id,
            quantity=quantity
        )
        save(cart_item)

    flash(f'Added {quantity} of {product.name} to cart.', 'success')
    return redirect(url_for('users_bp.my_cart'))
    

# delete from cart
@users_bp.route('/remove-from-cart/<int:item_id>', methods=['POST'])
@jwt_required()
def remove_from_cart(item_id):
    user_id = get_jwt_identity()

    item = ShoppingCart.query.get_or_404(item_id)

    if item.user_id != int(user_id):
        flash('Unauthorized action.', 'error')
        return redirect(url_for('users_bp.my_cart'))

    delete(item)

    flash('Item removed from cart.', 'success')
    return redirect(url_for('users_bp.my_cart'))


# checkout page
@users_bp.route("/create-checkout-session", methods=["POST"])
@jwt_required()
def create_checkout_session():
    user_id = get_jwt_identity()

    try:
        # هنا المفروض تجيب cart من الداتابيز
        cart_items = ShoppingCart.query.filter_by(user_id=user_id).all()

        if not cart_items:
            return jsonify({"error": "Cart is empty"}), 400

        line_items = []

        for item in cart_items:
            product = item.product

            line_items.append({
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": product.name,
                    },
                    "unit_amount": int(product.price * 100),  # Stripe uses cents
                },
                "quantity": item.quantity,
            })

        new_payment = Payment(
            user_id=user_id,
            amount=sum(item.product.price * item.quantity for item in cart_items),
            status='pending'
        )
        save(new_payment)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=url_for("users_bp.payment_success", _external=True),
            cancel_url=url_for("users_bp.payment_cancel", _external=True),
        )

        return redirect(checkout_session.url)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# payment success page
@users_bp.route("/payment-success", methods=["GET"])
@jwt_required()
def payment_success():
    user_id = get_jwt_identity()

    # هنا المفروض تمسح cart من الداتابيز
    cart_items = ShoppingCart.query.filter_by(user_id=user_id).all()

    for item in cart_items:
        delete(item)

    payment = Payment.query.filter_by(user_id=user_id, status='pending').order_by(Payment.id.desc()).first()

    if payment:
        payment.status = 'successful'
        save(payment)

    flash('Payment successful! Your cart has been cleared.', 'success')
    return redirect(url_for('users_bp.home'))


# payment cancel page
@users_bp.route("/payment-cancel", methods=["GET"])
@jwt_required()
def payment_cancel():
    user_id = get_jwt_identity()

    payment = Payment.query.filter_by(user_id=user_id, status='pending').order_by(Payment.id.desc()).first()

    if payment:
        payment.status = 'cancelled'
        save(payment)

    flash('Payment cancelled. Please try again.', 'error')
    return redirect(url_for('users_bp.my_cart'))