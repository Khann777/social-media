import json
import urllib.parse

from django.contrib.auth import get_user_model
from django.utils.timezone import now

from asgiref.sync import sync_to_async

from channels.generic.websocket import AsyncWebsocketConsumer

from knox.models import AuthToken
from knox.settings import CONSTANTS

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Установка соединения. Извлечение токена из query параметров.
        """
        print('CONNECTING...')
        query_string = self.scope['query_string'].decode('utf-8') #? Извлекаем query параметры из соединения
        query_params = urllib.parse.parse_qs(query_string) #? Парсим query параметры
        token = query_params.get('token', [None])[0] #? Получаем токен


        #* Проверка токена
        if not token or not await self.authenticate_user(token):
            #* Закрываем соединение, если токен отсутствует или недействителен
            await self.close()
            return

        #* Присоединяемся к группе (логика подключения)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        #* Получаем пользователя
        self.user = self.user

        #* Уведомление о подключении
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_connected',  # Новый тип события
                'username': self.user.username,
            }
        )

        #* Подключаем к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print('CONNECTED!!!!!!!!!!')


    async def disconnect(self, close_code):
        """
        Метод вызывается при разрыве соединения.
        """
        #* Уведомление об отключении
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_disconnected',  # Новый тип события
                'username': self.user.username,
            }
        )

        #* Удаляем пользователя из группы
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print('DISCONNECTED!!!!!!!!')


    async def receive(self, text_data):
        """
        Метод вызывается при получении сообщения через WebSocket.
        """
        #* Парсим полученные данные
        data = json.loads(text_data)
        message = data.get('message')

        #* Отправляем сообщение всем в группе
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',  # Указываем метод для вызова
                'message': message
            }
        )


    async def chat_message(self, event):
        """
        Метод для отправки сообщений через WebSocket.
        """
        #* Получаем сообщение из события
        message = event['message']

        #* Отправляем сообщение через WebSocket клиенту
        await self.send(text_data=json.dumps({
            'message': message
        }))


    async def user_connected(self, event):
        """
        Метод для уведомления всех участников чата о подключении пользователя.
        """
        username = User.get_username(self.user)


        #* Отправляем уведомление через WebSocket
        await self.send(text_data=json.dumps({
            'system_message': f'{username} connected to chat room {self.room_name}.'
        }))


    async def user_disconnected(self, event):
        """
        Метод для уведомления всех участников чата об отключении пользователя.
        """
        username = User.get_username(self.user)


        #* Отправляем уведомление через WebSocket
        await self.send(text_data=json.dumps({
            'system_message': f'{username} disconnected from chat room {self.room_name}.'
        }))


    @sync_to_async
    def authenticate_user(self, token):
        """
        Проверка токена Knox.
        """
        try:
            #* Ищем токен в базе данных по значению token_key
            auth_token = AuthToken.objects.filter(token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH], expiry__gt=now()).first()

            if auth_token:
                self.user = auth_token.user  #? Привязываем пользователя
                print(f'Authenticated user: {self.user}')
                return True
            else:
                print("Invalid or expired token")
                return False
        except Exception as e:
            print(f"Authentication failed: {e}")
        return False