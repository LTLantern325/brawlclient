from .server import LoginFailedMessage, LoginOkMessage, ServerHelloMessage
MESSAGES = {
    20100: ServerHelloMessage,
    20103: LoginFailedMessage,
    20104: LoginOkMessage
}

def create_message(packet_type):
    if packet_type in MESSAGES:
        return MESSAGES[packet_type]()