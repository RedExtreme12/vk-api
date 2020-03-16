import vk_api


def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """

    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)


def set_vk_session(login: str, password: str, token: str) -> 'vk_api.VkApi':
    """Устанавливаем сессию vk, а также пробуем аутентифицироваться,
    если возникает проблема, кидаем исключение AuthError."""

    vk_session = vk_api.VkApi(login=login,
                              password=password,
                              token=token,
                              captcha_handler=captcha_handler, )
    #  BAD PASSWORD
    try:
        vk_session.auth()
    except vk_api.AuthError as err_msg:
        print(f'Ooops... Something went wrong! {err_msg}')
    else:
        print('Authentication was successful')

    return vk_session


def get_api(vk_session: 'vk_api.VkApi') -> 'vk_api.vk_api.VkApiMethod':
    """Получаем API для установленной сессии."""

    api = vk_session.get_api()

    return api


def set_api(login: str, password: str, token: str) -> 'vk_api.vk_api.VkApiMethod':
    """Композиция функций get_api, set_vk_session."""

    vk_session = set_vk_session(login=login,
                                password=password,
                                token=token, )

    api = get_api(vk_session=vk_session)

    return api
