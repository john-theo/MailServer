from abc import ABC
from dataclasses import dataclass
import os


@dataclass
class ServiceProvider(ABC):
    name: str
    domain: str
    port: str


class Gmail(ServiceProvider):
    name = 'gmail'
    domain = 'smtp.gmail.com'
    port = 465


class NetEase(ServiceProvider):
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


PROVIDER_MAP = { x.name: x for x in (Gmail, NetEase, Yandex, QQ) }


def get_provider_args():
    provider = PROVIDER_MAP.get(
    os.environ.get('PROVIDER', 'gmail').lower())
    if provider:
        domain = provider.domain
        port = provider.port
    domain = os.environ.get('SMTP_DOMAIN', domain)
    port = os.environ.get('SMTP_SSL_PORT', port)
    return domain, port
