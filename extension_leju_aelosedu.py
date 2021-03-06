import serial
import subprocess
import time
from codelab_adapter.core_extension import Extension

import logging
logger = logging.getLogger(__name__)

SERIAL_DEVICE = '/dev/tty.wchusbserial14110'
CHANNEL = 0x42


def say(word):
    subprocess.call("say {}".format(word), shell=True)


class Dongle2401:
    def __init__(self, port, channel):
        self.port = port
        self.channel = channel
        self.dongle = self.open_port(self.port)
        # self.set_channel(channel)

    def open_port(self, port):
        return serial.Serial(port, 9600)

    def send(self, data):
        self.dongle.write(bytes(data))

    def set_channel(self, channel):
        self.send([0x29, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, channel])


def is_positive_int(s):
    try:
        num = int(s)
        return True if num > 0 else False
    except ValueError:
        return False


def parse_cmd(payload):
    cmd = 0
    if payload.startswith('leju_aelos_cmd_'):
        msg = payload.split('_')
        if is_positive_int(msg[-1]):
            cmd = int(msg[-1])
    return cmd


dongle = Dongle2401(SERIAL_DEVICE, CHANNEL)


class LejuAelosRobotExtention(Extension):
    def __init__(self):
        name = type(self).__name__
        super().__init__(name)

    def run(self):
        while True:
            message = self.read()
            if message["topic"] == "eim":
                action_num = parse_cmd(message.get('payload'))
                logger.info(action_num)
                dongle.send([action_num])


export = LejuAelosRobotExtention
