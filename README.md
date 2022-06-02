<pre><p align="center"><code>
   __  ___     _ __  ____                    
  /  |/  /__ _(_) / / __/__ _____  _____ ____
 / /|_/ / _ `/ / / _\ \/ -_) __/ |/ / -_) __/
/_/  /_/\_,_/_/_/ /___/\__/_/  |___/\__/_/   
                                             
</code></p></pre>

<p align="center">
<a href="https://hub.docker.com/r/johndope/mail-server"><img src="https://img.shields.io/docker/pulls/johndope/mail-server.svg" /></a>
<a href="https://github.com/john-theo/MailServer"><img src="https://img.shields.io/github/stars/john-theo/MailServer?label=github stars" /></a>
<img src="https://img.shields.io/badge/language-python-brightgreen.svg" />
<!-- <img src="https://img.shields.io/docker/v/johndope/mail-server?color=green" />
<img src="https://img.shields.io/github/last-commit/john-theo/MailServer?color=blue" />
<img src="https://img.shields.io/github/repo-size/john-theo/MailServer" /> -->
<img src="https://img.shields.io/badge/license-CC_BY--NC--SA_4.0-lightgrey" />
</p>

---

Completely **FREE and Open Source** like [Mail In A Box](https://github.com/mail-in-a-box/mailinabox), [Docker Mailserver](https://github.com/docker-mailserver/docker-mailserver), [Mailu](https://github.com/Mailu/) and [Maddy Mail Server](https://github.com/foxcpp/maddy), but <strong>DOESN'T REQUIRE</strong> posessing a domain, <strong>DOESN'T REQUIRE</strong> loads of docker compose configurations and <strong>DOESN'T REQUIRE</strong> a HTTPS certificate.

> **Notice: DO NOT** use this project in large-scale production environments.

<p align="center">
<img src="https://github.com/john-theo/MailServer/raw/main/imgs/banner.png" width="600" style="border-radius: 8px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); padding: 5px 10px" />
</p>

## Features

- 🔥 <strong>RESTful API</strong>, basic url request in any coding language;
- 📧 <strong>Authentic</strong>, send actual emails (looking at you, mailhog);
- 🔐 <strong>Secure</strong>, force SSL encryption when sending mails;
- ✨ <strong>Lightweight yet Reliable</strong>, use SMTP under the hood;
- 🚀 <strong>OOTB</strong>, working out-of-the-box with almost zero config;
- 🐳 <strong>Docker Ready</strong>, start your service in less than 1 minute;
- ⚛️ <strong>Heroku Ready</strong>, deploy your service in less than 1 minute.

## Get Started

```bash
read -p "Password: " -s password && \
docker run --rm -it -p <LOCAL_PORT>:8080 \
    -e "NAME=<DISPLAY_SENDER_NAME>" \
    -e "EMAIL=<YOUR@EMAIL.ADDRESS>" \
    -e "PASSWORD=${password}" \
    johndope/mail-server:latest
```

> There will be a prompt for "Password", paste your Email password and hit enter (whatever you paste or input will not be shown on the screen).

## Providers

Email addresses from these 4 SMTP mail service providers can be automatically configured: [Gmail](https://support.google.com/mail/answer/7126229?hl=en#zippy=%2Cstep-change-smtp-other-settings-in-your-email-client), [Yandex](https://yandex.com/support/mail/mail-clients/others.html), [QQ (Tencent)](https://service.mail.qq.com/cgi-bin/help?id=28&no=167&subtype=1) and [163 (NetEase)](http://help.163.com/09/1223/14/5R7P3QI100753VB8.html).

**NOTICE:**
- Use the [APP password](https://myaccount.google.com/apppasswords) for Gmail password;
- Use the [Auth Code](#) (Settings - POP3/SMTP/IMAP - Auth Code Management) for NetEase password.

### Use other providers

[Mail Server](https://github.com/john-theo/MailServer) also supports custom provider configurations, just add the `SMTP_DOMAIN` (eg. smtp.gmail.com) and `SMTP_SSL_PORT` (eg. 465) env variables.

## Basic Usage

Here's a simple example for Python users:

```python
import requests

resp = requests.get(SERVER_INSTANCE, params={
    'subject': 'Please validate your email address',
    'receiver': [RECEIVER_EMAIL, ANOTHER_RECEIVER_EMAIL],
    'html': f'<h1>Hello from {BRAND_NAME}!</h1>',
})
resp.raise_for_status()
print(resp.json())
```

## Templates

[Mail Server](https://github.com/john-theo/MailServer) also supports templates. [Mail Server](https://github.com/john-theo/MailServer) ships with a [default template](https://github.com/john-theo/MailServer/blob/main/templates/activation.jinja) (for new registered account activation), to use this template:

```python
activation_template_args = {
    'username': 'John Theo',
    'activation_link': 'https://github.com/john-theo',
    'brand_name': BRAND_NAME,
    'contact_email': RECEIVER_EMAIL,
}
resp = requests.post(SERVER_INSTANCE, data={
    'subject': 'Please validate your email address',
    'receiver': [RECEIVER_EMAIL],
    'template': 'activation',
    **activation_template_args
}, files=[
    ('attachments', ('activation.jinja', open('templates/activation.jinja', 'rb'))),
    ('attachments', ('server.py', open('src/server.py', 'rb')))
])
resp.raise_for_status()
print(resp.json())
```

You can also mount your own templates into the docker container and use them.

### Template Debugging

To debug your own templates, you can use the `/debug` (backward compatibility) or the `/preview` endpoint with the same request payload, it will response the renderer HTML page with parsed parameters at the bottom.

<p align="center">
<img src="https://github.com/john-theo/MailServer/raw/main/imgs/preview.png" width="300"  style="border-radius: 8px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); padding: 5px 10px" />
</p>

## TOTP

TOTP, or time-based one-time password, is the algorithm commonly used by authenticators for 2FA, it generates a one-time password that uses the current time as a source of uniqueness.

If you deploy [Mail Server](https://github.com/john-theo/MailServer) to a publicly accessible domain (like Heroku), anyone can send emails on your behalf which is highly dangerous. So to enable TOTP to reject requests not send by your trusted backends:

1. add a `TOTP_SECRET` env variable;
2. tell your good backend pal this secret key and ask them to send requests with a query parameter `totp` (eg. `GET /?totp=072813`).

> There are packages in various languages that can generate the TOTP token like [ROTP](https://github.com/mdp/rotp) for Ruby, [PyTOP](https://github.com/pyauth/pyotp) for Python, [OTPlib](https://github.com/yeojz/otplib) for Nodejs and many more.

### How to generate the TOTP secret key

To generate a secret key run:

```bash
docker run --rm -it \
    johndope/mail-server:latest \
    bash generate_totp.sh
```

## Deploy

1. Clone this repository
2. Fill in the blanks in the `.env` file
3. Run `make hinit && make hpush`

## Quick reference

- **Maintained by:** [John Dope](https://github.com/john-theo)
- **Code repository:** https://github.com/john-theo/MailServer
- **Issues:** https://github.com/john-theo/MailServer/issues
- **Docker Hub:** https://hub.docker.com/r/johndope/mail-server

## License

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://avatars.githubusercontent.com/u/36699957">Mail Server</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://github.com/john-theo">John Dope</a> is licensed under <a href="http://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution-NonCommercial-ShareAlike 4.0 International<img style="height:18px;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:18px;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><img style="height:18px;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1"><img style="height:18px;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1"></a></p>