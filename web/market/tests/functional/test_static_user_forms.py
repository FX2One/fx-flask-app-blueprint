from market.notes.forms import NoteForm, EditNoteForm
from market.posts.forms import AddPostForm, EditPostForm
from market.posts_review.forms import AddReviewForm, EditReviewForm
from market.models import User, Note, Review, Note, Post
from urllib.parse import urlparse



"""
mocking static user.id while turning off @login_required
change .env LOGIN_DISABLED=TRUE
locate current_user.id in views and replace with 1
to mock statically created user
"""

def test_add_note_page_redirect(client):
    form = NoteForm(title='test_2title', notation='test_2note')
    response = client.post('/add_note', data=form.data, follow_redirects=False)
    assert response.status_code == 302
    expectedPath = '/all_owned_notes'
    assert urlparse(response.location).path == expectedPath


def test_edit_post_form(client,new_post):
    form = EditPostForm(title='testtitle1', post='testpost1')
    response = client.post(f'/post/edit/{new_post.id}', data=form.data)
    assert response.status_code == 200
    assert b'Title' in response.data
    assert b'Post Section' in response.data


def test_edit_review_form(client,new_post, new_user, session):
    reviews = Review(review='reviewtest', reviewer_id=new_user.id, post_id=new_post.id)
    session.add(reviews)
    session.commit()
    form = EditReviewForm(review='changed')
    response = client.post(f'/review/edit/{new_post.id}', data=form.data)
    assert response.status_code == 200
    assert b'Edit Review' in response.data
    assert b'Edit the comment' in response.data


def test_edit_note_form(client,new_user,session):
    note = Note(title='notetitle',notation='testnote',notation_id=new_user.id)
    session.add(note)
    session.commit()
    form = EditNoteForm(title='editedtitle', notation='editednote')
    response = client.post(f'/edit_note/{new_user.id}', data=form.data)
    assert response.status_code == 200
    assert b'Title' in response.data
    assert b'Note' in response.data
