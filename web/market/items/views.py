from flask import render_template, redirect, url_for, flash, request, Blueprint
from market.items.forms import ItemsForm, EditItemsForm, PurchaseItemForm, SellItemForm
from flask_login import current_user, login_user, logout_user, login_required
from market.models import User, Item, Post, Review
from market import db

item_bp = Blueprint('items', __name__, template_folder='templates')


@item_bp.route('/add_item', methods=['GET', 'POST'])
@login_required
def add_item():
    form = ItemsForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_item = Item(
            form.name.data,
            form.price.data,
            form.barcode.data,
            form.description.data)
        db.session.add(new_item)
        db.session.commit()
        flash(f"item {new_item.name} has been added successfully!", category="success")
        return redirect(url_for('items.market_page'))
    return render_template('add_item.html', form=form)


@item_bp.route('/all_owned_items', methods=['GET', 'POST'])
@login_required
def all_owned_items():
    sell_form = SellItemForm()
    sold_item = request.form.get('sold_item')
    s_item_object = Item.query.filter_by(name=sold_item).first()
    if s_item_object:
        if current_user.can_sell(s_item_object):
            s_item_object.sell(current_user)
            flash(f"Congratulations! You sold {s_item_object.name} back to market!", category='success')
        else:
            flash(f"Something went wrong with selling {s_item_object.name}", category='danger')
    all_user_items = Item.query.filter_by(user_id=current_user.id)
    return render_template('all_owned_items.html', items=all_user_items, sell_form=sell_form)


@item_bp.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    if request.method == "POST":
        # Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$",
                      category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!",
                      category='danger')
        return redirect(url_for('items.market_page'))

    if request.method == "GET":
        items = Item.query.filter_by(user_id=None)
        return render_template('market.html', items=items, purchase_form=purchase_form)