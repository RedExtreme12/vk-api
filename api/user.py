import vk_api
import time

from api import API

CURRENT_VERSION_API = 5.103
NUMBER_RECEIVED_PHOTO = 1000  # Max value


class User:

    def __init__(self, login: str, password: str, token: str, link=None):
        self.api = API.set_api(login=login,
                               password=password,
                               token=token, )

        self.user_id = self.get_user_id(link)

    def get_user_id(self, link: 'str') -> (int, None):
        if link:
            user_id = link

            if 'vk.com/' in link:
                user_id = link.split('/')[-1]
            if not user_id.replace('id', '').isdigit():
                user_id = self.api.users.get(user_ids=user_id)
                user_dict = user_id[0]
                return user_dict['id']
            else:
                user_id = user_id.replace('id', '')

            return int(user_id)

        return None

    def get_photo_albums(self, type_of_album: str) -> (dict, None):
        if self.api:
            try:
                albums = self.api.photos.get(owner_id=self.user_id,
                                             album_id=type_of_album,
                                             count=NUMBER_RECEIVED_PHOTO,
                                             rev=1)
            except vk_api.VkApiError as err_msg:
                print(f'Ooops... Something went wrong, Error message: {err_msg}')
            else:
                return albums['items']

        return None

    def get_wall(self, _count):
        if self.api:
            try:
                wall = self.api.wall.get(owner_id=self.user_id,
                                         count=_count)
            except vk_api.VkApiError as err_msg:
                print(f'Ooops... Something went wrong, Error message: {err_msg}')
            else:
                return wall['items']

        return None

    def add_obj_like(self, _type: str, item_id: int, count_of_liked: int) -> int:
        if self.api:
            if not self.obj_is_liked(_type=_type,
                                     item_id=item_id, ):
                try:
                    self.api.likes.add(type=_type,
                                       item_id=item_id,
                                       owner_id=self.user_id,
                                       captcha_handler=self.captcha_handler)
                except vk_api.VkApiError as msg:
                    print(f'Error! The {_type.title()} with id: {item_id} was not like because of {msg}, oh...')
                else:
                    count_of_liked += 1
                    print(f'The {_type.title()} {item_id} was successfully put like! Total count: {count_of_liked}')
                    time.sleep(1)
                    return count_of_liked
            else:
                print(f'On the {_type.title()} with id: {item_id} like has already been set.')
                time.sleep(1)

        return count_of_liked

    def add_like_photo(self, type_of_album: str, cnt: int) -> int:
        count_of_liked = 0
        _type = 'photo'

        album = self.get_photo_albums(type_of_album=type_of_album)

        if cnt != 1:
            for c in range(cnt - 1):
                if album:
                    for photo in album:
                        count_of_liked = self.add_obj_like(_type=_type,
                                                           item_id=photo['id'],
                                                           count_of_liked=count_of_liked, )

        return count_of_liked

    def add_comment(self, comment: list, count: int):
        import random

        if self.api:
            try:
                wall = self.get_wall(10)

                for post in wall:
                    for _ in range(count):
                        msg = comment[random.randrange(0, len(comment))]

                        self.api.wall.createComment(owner_id=self.user_id,
                                                    post_id=post['id'],
                                                    message=comment)
                        print('Comment added!')

            except vk_api.VkApiError as msg:
                print(f'Something went wrong: {msg}')

    def remove_obj_like(self, _type: str, item_id: int, count_of_disliked: int):
        if self.api:
            if self.obj_is_liked(_type=_type,
                                 item_id=item_id):
                try:
                    self.api.likes.delete(type=_type,
                                          item_id=item_id,
                                          owner_id=self.user_id,
                                          captcha_handler=self.captcha_handler)
                except vk_api.VkApiError as msg:
                    print(f'Error! The {_type.title()} with id: {item_id} was not disliked because of {msg}, oh...')
                else:
                    count_of_disliked += 1
                    print(f'Like was successfully deleted from {_type.title()} with id'
                          f'{item_id} ! Total count: {count_of_disliked}')
                    time.sleep(1)

        return count_of_disliked

    def remove_like_photo(self, type_of_album: str) -> int:
        count_of_disliked = 0
        _type = 'photo'

        album = self.get_photo_albums(type_of_album=type_of_album)

        if album:
            for photo in album:
                count_of_disliked = self.remove_obj_like(_type=_type,
                                                         item_id=photo['id'],
                                                         count_of_disliked=count_of_disliked)

        return count_of_disliked

    def obj_is_liked(self, _type: 'str', item_id: int) -> bool:
        if self.api:
            try:
                isLiked = self.api.likes.isLiked(type=_type,
                                                 item_id=item_id,
                                                 owner_id=self.user_id, )

                return isLiked['liked']

            except ValueError:
                print('Hm, maybe You forgot to provide a link to the human...')

            return False

    def captcha_handler(self, captcha):
        """ При возникновении капчи вызывается эта функция и ей передается объект
            капчи. Через метод get_url можно получить ссылку на изображение.
            Через метод try_again можно попытаться отправить запрос с кодом капчи
        """

        key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

        # Пробуем снова отправить запрос с капчей
        return captcha.try_again(key)
