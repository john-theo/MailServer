from abc import ABC
from dataclasses import dataclass


@dataclass
class ServiceProvider(ABC):
    name: str
    domain: str
    port: str


class Gmail(ServiceProvider):
    name = 'gmail'
    domain = 'smtp.gmail.com'
    port = 465


class NetEase163(ServiceProvider):
    name = '163'
    domain = 'smtp.163.com'
    port = 465


class Yandex(ServiceProvider):
    name = 'yandex'
    domain = 'smtp.163.com'
    port = 465


class QQ(ServiceProvider):
    name = 'qq'
    domain = 'smtp.qq.com'
    port = 465
