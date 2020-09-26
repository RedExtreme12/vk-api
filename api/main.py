from api.user import User
from pprint import pprint


if __name__ == '__main__':
    # Enter your login and password.
    login = ''
    password = ''

    # You should get a token.
    token = '30fb3f5f75a96fbe146aa679e9f87c5763e4cdf981220488e74df174f70c75c140b5659783b587440edb2'

    _user = User(login,
                 password,
                 token,
                 'https://vk.com/paramime', )

    print(_user.add_like_photo('saved', cnt=100))
    # print(_user.add_comment('Динак идёт пить пиво', 2))
