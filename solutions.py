#!/usr/bin/env python3

from authentication import get_admin_session
from browser import solve_browser_challenges
from feedback import solve_feedback_challenges
from filehandling import solve_file_handling_challenges
from misc import solve_misc_challenges
from products import solve_product_challenges
from users import solve_user_challenges
import sys

try:
  hostname = sys.argv[1]
except:
  hostname = 'http://localhost:8080'
  print('Using default hostname for solving...')
  
server = hostname
session = get_admin_session(server)
solve_browser_challenges(server)
solve_file_handling_challenges(server)
solve_user_challenges(server)
solve_feedback_challenges(server)
solve_product_challenges(server)
solve_misc_challenges(server)
