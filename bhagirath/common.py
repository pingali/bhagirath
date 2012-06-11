'''
Created on Jun 11, 2012

@author: 254910
'''

from bhagirath import settings
 
def get_prod_server_flag():
    if settings.is_production_server():
        return True
    else:
        return False