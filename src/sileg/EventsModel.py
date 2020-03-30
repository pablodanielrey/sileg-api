
import os
import pulsar
from pulsar.schema import JsonSchema

from login.model.entities.Login import LoginEvent, LoginEventTypes

PULSAR_URL = os.environ.get('PULSAR_URL', 'pulsar://localhost:6650')
PULSAR_TOPIC = os.environ.get('PULSAR_TOPIC', 'google')
PULSAR_SUBSCRIPTION = os.environ.get('PULSAR_SUBSCRIPTION', 'google')

import logging

class EventsModel:

    def __init__(self):
        self.client = pulsar.Client(PULSAR_URL)
        self.producer = self.client.create_producer(topic=PULSAR_TOPIC, schema=JsonSchema(LoginEvent))
        self.logging = logging.getLogger(self.__class__.__qualname__)

    def __del__(self):
        try:
            self.producer.close()
        except:
            pass
        self.client.close()

    def send(self, username, credentials):
        self.logging.debug(f'enviando el evento de {username} a pulsar')
        try:
            msg = LoginEvent(type_=LoginEventTypes.CHANGE_CREDENTIALS.value, 
                            username=username, 
                            credentials=credentials)
            self.producer.send(msg)
        except Exception as e:
            self.logging.exception(e)
            raise e
