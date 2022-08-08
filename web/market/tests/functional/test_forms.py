from market.notes.forms import NoteForm, EditNoteForm
from market.posts.forms import AddPostForm, EditPostForm
from market.posts_review.forms import AddReviewForm, EditReviewForm
from market.account.forms import LoginForm, RegisterForm
from market.models import User, Note, Review, Note, Post
from market.items.forms import ItemsForm
from urllib.parse import urlparse
from flask import url_for,request


"""
form testing inspired by below
https://stackoverflow.com/questions/37579411/testing-a-post-that-uses-flask-wtf-validate-on-submit
https://stackoverflow.com/questions/56171561/unit-test-validation-for-a-flask-wtf-form
"""


# test redirect after adding item
def test_add_item_form(client):
    rv = client.get('/add_item')
    assert rv.status_code == 200
    assert b'Name' in rv.data
    assert b'Price' in rv.data
    assert b'Barcode' in rv.data
    assert b'Description' in rv.data
    form = ItemsForm(name='item', price=123, barcode=1234567, description='test')
    response = client.post('/add_item', data=form.data, follow_redirects=False)
    assert response.status_code == 302
    expectedPath = '/market'
    assert urlparse(response.location).path == expectedPath



def test_add_note_form(client):
    rv = client.get('/add_note')
    assert rv.status_code == 200
    assert b'Title' in rv.data
    assert b'Note' in rv.data
    form = NoteForm(title='test_title', notation='test_note')
    response = client.post('/add_note', data=form.data, follow_redirects=True)
    assert response.status_code == 200



def test_add_post_form(client):
    form = AddPostForm(title='test2title', post='3testpost')
    response = client.post('/add_post', data=form.data, follow_redirects=False)
    assert response.status_code == 200
    response = client.get(url_for('posts.add_post'), follow_redirects=False)
    assert response.status_code == 200
    assert request.path == url_for('posts.add_post')



def test_add_review_form(client, new_post, new_user, session):
    reviews = Review(review='reviewtest', reviewer_id=new_user.id, post_id=new_post.id)
    form = AddReviewForm(formdata=None, obj=reviews)
    session.add(reviews)
    session.commit()
    response = client.post(f'/add_review/{new_post.id}', data=form.data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Review Post' in response.data
    assert b'Comment the Post' in response.data


def test_login_form(client):
    form = LoginForm(username='testname', password='testpass')
    response = client.post('/login', data=form.data)
    assert response.status_code == 200
    assert b'Username' in response.data
    assert b'Password' in response.data


# test register form and redirect after
def test_register_user_page(client):
    # test register page
    response = client.get('/register')
    assert b'Username' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data
    assert b'Confirm' in response.data
    assert response.status_code == 200
    # test user registration
    form = RegisterForm(username='testuser',email_address='testmail@test.com',password='testpass1',confirm='testpass1')
    response = client.post('/register', data=form.data, follow_redirects=False)
    assert response.status_code == 302
    expectedPath = '/market'
    assert urlparse(response.location).path == expectedPath



