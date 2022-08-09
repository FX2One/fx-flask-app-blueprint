# test confirmation token
def test_the_token(new_user, the_token):
    assert new_user.confirm(the_token)

# testing if two users added to the database have initially assigned id numbers


def test_2_users(new_user, new_user2):
    assert new_user.id == 1
    assert new_user2.id == 2

# testing if bought item belong to new_user we committed it too


def test_buy_item(new_user, buy_item_in_budget):
    can_purchase = new_user.can_purchase(buy_item_in_budget)
    assert can_purchase is True
    assert buy_item_in_budget.user_id == new_user.id
    assert new_user.budget == 4900

# testing if your user can buy item which is over his budget


def test_buy_item_over_budget(new_user, buy_item_over_budget):
    can_purchase = new_user.can_purchase(buy_item_over_budget)
    assert can_purchase is False
    assert buy_item_over_budget.user_id == new_user.id
    assert new_user.budget == -1000

# testing if sold item is not attached to any user


def test_sell_item(new_item_sold):
    assert new_item_sold.user_id is None

# test buy/sell functionality in Item model along with can_purchase/can_sell based in User model


def test_user_can_buysell(new_user, new_item, buy_item_in_budget):
    buy_it = new_user.can_purchase(new_item)
    biib = buy_item_in_budget
    assert biib.user_id == new_user.id
    assert new_user.budget == 4900
    assert new_item.user_id == new_user.id
    assert buy_it is True
    sell_it = new_user.can_sell(new_item)
    assert sell_it is True
    biib.sell(new_user)
    assert new_user.budget == 5000
    assert new_item.user_id is None

# checks is the password is added and created correctly


def test_set_password(new_user):
    assert new_user.password_hash != 'testpass'
    assert new_user.check_password('testpass')

# testing item creation


def test_item(new_item):
    assert new_item.name == 'testitem'
    assert new_item.price == 100
    assert new_item.barcode == 1212121
    assert new_item.description == 'testitem'

# testing new post


def test_new_post(new_post):
    assert new_post.title == 'testtitletest'
    assert new_post.post == 'somepostsomepost'
    assert new_post.author_id == 1

# testing new note


def test_new_note(new_note):
    assert new_note.title == 'testtitletest'
    assert new_note.notation == 'somenote_somenote'
    assert new_note.notation_id == 1

# one review added by one new_user


def test_new_review(new_review, new_review2):
    assert new_review.review == 'testreviewonpost'
    assert new_review2.review == 'testreviewonpost2'
    assert new_review.reviewer_id == 1
    assert new_review.post_id == 1
    assert new_review2.post_id == 1

# two reviews added by one new_user ,which should result in id == 1
# one review added to the same post by new_user2 which should result as id == 2
# all reviews have to have the same post_id as they belong to the same post


def test_new_review2(new_review, new_review2, new_review_all):
    assert new_review.review == 'testreviewonpost'
    assert new_review2.review == 'testreviewonpost2'
    assert new_review_all.review == 'testreviewonpost3'
    assert new_review.reviewer_id == 1
    assert new_review.post_id == 1
    assert new_review2.post_id == 1
    assert new_review_all.post_id == 1
    assert new_review_all.reviewer_id == 2

# test item being purchased and sold


def test_can_purchase_sell(new_user, new_item):
    buy = new_user.can_purchase(new_item)
    assert buy is True
    new_item.buy(new_user)
    assert new_user.budget < 5000
    assert new_user.id == new_item.user_id
    sell = new_user.can_sell(new_item)
    assert sell is True
    new_item.sell(new_user)
    assert new_user.id != new_item.user_id
    assert new_item.user_id is None
    assert new_user.budget == 5000
