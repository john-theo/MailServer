from abc import ABC
from dataclasses import dataclass
from typing import List
import os


@dataclass
class ServiceProvider(ABC):
    domains: List[str]
    server: str
    port: str


class Gmail(ServiceProvider):
    domains = ['gmail.com']
    server = 'smtp.gmail.com'
    port = 465


class NetEase(ServiceProvider):
    domains = ['163.com']
    server = 'smtp.163.com'
    port = 465


class NetEase2(ServiceProvider):
    domains = ['126.com']
    server = 'smtp.126.com'
    port = 465


class Yandex(ServiceProvider):
    domains = ['yandex.com']
    server = 'smtp.yandex.com'
    port = 465


class QQ(ServiceProvider):
    domains = ['qq.com', 'foxmail.com']
    server = 'smtp.qq.com'
    port = 465


PROVIDER_MAP = {}
for provider in (Gmail, NetEase, NetEase2, Yandex, QQ):
    for domain in provider.domains:
        PROVIDER_MAP[domain] = provider


def get_provider_args():
    username = os.environ.get('EMAIL')
    assert username, 'Missing environment variable EMAIL'
    if username.endswith('.com'):
        domain = username.split('@', 1)[-1].lower()
        if domain in PROVIDER_MAP:
            provider = PROVIDER_MAP[domain]
            return provider.server, provider.port
    server = os.environ.get('SMTP_DOMAIN')
    port = os.environ.get('SMTP_SSL_PORT')
    assert server and port, 'Missing environment variable SMTP_DOMAIN or SMTP_SSL_PORT'
    return server, port
