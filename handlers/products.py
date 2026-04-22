from models import query
# from security import SECRET_KEY
# import jwt



def tshirts_list(handler):
    parse = handler.path.split('?')

    filter = {}
    if len(parse) > 1:
        for i in parse[1].split('&'):
            if '=' in i:
                key, val = i.split('=')
                filter[key] = val
    request = '''SELECT * FROM tshirts WHERE 1=1'''

    pass

