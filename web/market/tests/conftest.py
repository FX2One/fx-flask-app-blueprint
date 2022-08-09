from market.config import TestingConfig
from market import db as _db
from market import create_app
import pytest
import sys
import os
from sqlalchemy import event
from flask.testing import FlaskClient
from market.models import Item, User, Post, Review, Note
basedir = os.path.abspath(os.path.dirname(__file__))


"""Session wide-test Flask application"""
@pytest.fixture(scope='function')
def app():
    app = create_app(TestingConfig)

    # Establish an application context before running the tests.
    with app.app_context():
        yield app


"""Flask test client"""
@pytest.fixture(scope='function')
def client(app):
    ap = app
    ctx = ap.test_request_context()
    ctx.push()
    ap.test_client_class = FlaskClient
    with ap.test_client() as client:
        yield client


"""Flask test database scope"""
@pytest.fixture(scope='function')
def db(app):
    _db.app = app
    _db.create_all()
    yield _db
    _db.drop_all()


"""Function scoped session"""
@pytest.fixture(scope="function", autouse=True)
def session(app, db):
    with app.app_context():
        conn = _db.engine.connect()
        txn = conn.begin()

        options = dict(bind=conn, binds={})
        sess = _db.create_scoped_session(options=options)

        # establish  a SAVEPOINT just before beginning the test
        # (http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#using-savepoint)
        sess.begin_nested()

        _db.session = sess
        yield sess

        @event.listens_for(sess(), "after_transaction_end")
        def restart_savepoint(sess2, trans):
            # Detecting whether this is indeed the nested transaction of the test
            if trans.nested and not trans._parent.nested:
                # The test should have called session.commit(),
                # but to be safe we expire the session
                sess2.expire_all()
                sess.begin_nested()

        # Cleanup
        sess.remove()

        # This instruction rollback any commit that were executed in the tests.
        txn.rollback()
        conn.close()


# create default user
@pytest.fixture(scope='function')
def new_user(session):
    user = User(username='testname',
                email_address='test@test.com', password='testpass')
    session.add(user)
    session.commit()
    return user


# create default user2
@pytest.fixture(scope='function')
def new_user2(session):
    user = User(username='testname2',
                email_address='test2@test.com', password='testpass')
    session.add(user)
    session.commit()
    return user


# gather token generator
@pytest.fixture(scope='function')
def the_token(new_user):
    token = new_user.generate_auth_token()
    return token


# create new item in 'budget'
@pytest.fixture(scope='function')
def new_item(session):
    item = Item(name='testitem', price=100,
                barcode=1212121, description='testitem')
    session.add(item)
    session.commit()
    return item


# create new_item over 'budget'
@pytest.fixture(scope='function')
def new_item_over(session):
    item = Item(name='testitem2', price=6000,
                barcode=1212122, description='testitem2')
    session.add(item)
    session.commit()
    return item


# buys new item in 'budget'
@pytest.fixture(scope='function')
def buy_item_in_budget(session, new_user, new_item):
    new_item.buy(new_user)
    return new_item


# buys item which is over the 'budget'
@pytest.fixture(scope='function')
def buy_item_over_budget(session, new_user, new_item_over):
    new_item_over.buy(new_user)
    return new_item_over


# takes fixture of already bought item
# returns item back to market
@pytest.fixture(scope='function')
def new_item_sold(session, buy_item_in_budget, new_user):
    buy_item_in_budget.sell(new_user)
    return buy_item_in_budget


# check new post addition
@pytest.fixture(scope='function')
def new_post(session, new_user):
    post = Post(title='testtitletest',
                post='somepostsomepost', author_id=new_user.id)
    session.add(post)
    session.commit()
    return post


# check new note addition
@pytest.fixture(scope='function')
def new_note(session, new_user):
    note = Note(title='testtitletest',
                notation='somenote_somenote', notation_id=new_user.id)
    session.add(note)
    session.commit()
    return note


# user1 ,post1 = review1
# check new review added to post1 by user1
@pytest.fixture(scope='function')
def new_review(session, new_post, new_user):
    review = Review(review='testreviewonpost',
                    reviewer_id=new_user.id, post_id=new_post.id)
    session.add(review)
    session.commit()
    return review


# user1, post1 = review2
# check another review being added to the post1 by user1
@pytest.fixture(scope='function')
def new_review2(session, new_post, new_user):
    review = Review(review='testreviewonpost2',
                    reviewer_id=new_user.id, post_id=new_post.id)
    session.add(review)
    session.commit()
    return review


# user2 ,post1 = review3
# check user2 adding 3rd review to post1
@pytest.fixture(scope='function')
def new_review_all(session, new_post, new_user2):
    review = Review(review='testreviewonpost3',
                    reviewer_id=new_user2.id, post_id=new_post.id)
    session.add(review)
    session.commit()
    return review


# check login and logout
@pytest.fixture(scope='function')
def login_default_user(client):
    client.post('/login',
                data=dict(username='testuser', password='testpass'),
                follow_redirects=True)

    yield
    client.get('/logout', follow_redirects=True)
