<div align="center">
    <img alt="Tzedek banner" src="https://github.com/user-attachments/assets/4df3e686-21bb-42e8-99c0-a42248632f32" width="85%" height="85%">
<h1 align="center">
  TZEDEK
</h1>
<p align="center">
  <i>Know your rights</i>
</p>

[![Linters](https://github.com/TabarakoAkula/tzedek/actions/workflows/linters.yml/badge.svg?branch=master)](https://github.com/TabarakoAkula/tzedek/actions/workflows/linters.yml)  
[![python - 3.12](https://img.shields.io/badge/python-3.12-4b4de3)](https://github.com/TabarakoAkula/tzedek)
[![Django - 5.0.6](https://img.shields.io/badge/Django-5.2.1-4b4de3)](https://github.com/TabarakoAkula/tzedek)

</div>

Tzedek is an AI-driven platform that helps people to understand their legal and civil rights. 
It collects and structures data from [Kol-Zchut](https://www.kolzchut.org.il/) and uses AI 
([Onyx](https://github.com/onyx-dot-app/onyx) + GPT) to provide clear answers in multiple languages.
The project include open API and a [Telegram bot](https://t.me/tzedek_israel_bot) for easy and accessible legal help.

The project currently provides answers in **English**, **Hebrew**(_עברית_) and **Russian**(_Русский_)

## 🔧 Prerequisites

This project integrates with the [Onyx](https://github.com/onyx-dot-app/onyx), a critical part of the 
website's infrastructure. Follow [Documentation](https://docs.onyx.app/quickstart) to set it up.  

Onyx launch checkpoints:
- [Clone](https://github.com/onyx-dot-app/onyx) repository
- [Configure](https://docs.onyx.app/configuration_guide) settings
- [Launch](https://docs.onyx.app/quickstart) by docker compose

> A web version will be available at [localhost:3000](http://localhost:3000)
>

- Open [connectors page](http://localhost:3000/admin/indexing/status) at admin panel
- [Create](http://localhost:3000/admin/connectors/file?step=1) new "File" connector
- Add your files (Our version use 6000+ files with pages data)

Wait theirs indexing (Progress is displaying at [connectors page](http://localhost:3000/admin/indexing/status)) 
and [create your own Assistant](http://localhost:3000/admin/assistants). 
Do not forget to provide a prompt (``You are a professional lawyer...``). 

> **Important: Tzedek will use the first custom assistant wich u added**
>

Now u can proceed to the setup of Tzedek🐦‍🔥
## 🤖 Tzedek setup
### 🐋 Fast start
Clone Tzedek git repository: 
```bash
git clone https://github.com/TabarakoAkula/tzedek.git
  ```
Configure it:
+ Fill in ``.env.template`` file
+ Rename file to ``.env``

Build and launch docker compose by: 
```bash
docker compose up --build
```

> It will be launched at [localhost:8181](http://localhost:8181)
>

**Enjoy it😊**

### ⚒️ Launching without docker

Install requirements using poetry:
  ```bash
poetry install --without dev linters
```

Launch Web, Bot, Celery:
  - Web:
    ```bash
    cd web
    python manage.py.migrate
    python manage.py runserver
    ```
    > Site will be launched at [localhost:8000](http://localhost:8000)
    >

- Telegram bot
  ```bash
    python telegram_bot
    ```
- Celery
  ```bash
    cd web
    celery -A core worker -P threads -E
    ```

## ⚙️ Additional options 
### 🕹️Admin panel
Tzedek provides a web admin panel, to use it:
- Create superuser:
  ```bash
    cd web
    python manage.py createsuperuser
    ```
- Fill required fields
- Open ``/admin`` endpoint and enter your data

### 📂 Logs
While using gunicorn (Docker compose version) it will save logs to 
``/web/logs/`` folder. U can view ``access_log`` and ``errors_log``.
Other logs would be in terminal / docker logs

# Explanation of work

## User flow
<div align="center">
<img src="https://github.com/user-attachments/assets/d87f9e3e-07a6-41a0-b3b0-29256d9f0229" alt="userflow explanation">
</div>

## Interaction between Tzedek and Onyx
<div align="center">
<img src="https://github.com/user-attachments/assets/590f6b6a-b72a-4efd-b2c6-dfa55fd989be" alt="interaction explanation" width="70%" align="center">
</div>
