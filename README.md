# easy_tbot
Mini framework  for data base and other usefull stuff integration with Telegram bot api
## Instalation
````commandline
pip install easy-tbot
````
## Project structure
- Project
  - Sections (a set of sections folders)
  - settings.py
  - botmanager.py
### The settings.py file
Here we hold all framework configuration stuff.

| varibale name | Wath they do |
| ------------- | ------------- |
| BASEDIR  | Store the project direction  |
| SECTIONS | Store wath sections must be loaded  |
| DB | sqlalchemy connection string |
| TOKEN | The token provided by Telegram botfather for your bot |
| PROXY | The proxy for connect with Telegram (MTPROTO not allowed ...!!yet!!) |
| DEBUG | Control if framework can display debug information |
### The botmanager.py file 
A file that store a entry point for our full bot. Three commands base are allowed and others can be added.

1. To create a section
   - ```commandline  
     python botmanager.py createsection <name> 
     ```
2. To setup the data base
   - ```commandline  
     python botmanager.py migrate
     ```
3. To run the bot
   - ```commandline  
     python botmanager.py run
     ```

### Sections
Sections are logic separed part of our bot. They are formed by handler, inlines, middlewares, models, and shells explained below.

- Section
  _ __init__.py
  - handlers.py
  - inlines.py
  - middlewares.py
  - models.py
  - shells.py
  
#### Handlers
Represented by handlers.py file. Store a set of handlers that inherit from All, Command, Regex, Function classes stored in
easy_tbot.handlers.handler
A example for reply the /start command
```python

from easy_tbot.handlers.handler import Command,Message

class StartCommand(Command):
    commands = ['start']

    def handle(self, msg: Message):
        self.bot.reply_to(msg, 'Hello world!!!')
```
#### Inlines
Represented by inlines.py file. Store a set of handlers that inherit from InlineHandler class stored in
easy_tbot.handlers.inline
A example for reply the 'hello' inline
```python
from easy_tbot.handlers.inline import InlineHandler,InlineQuery

class HelloInline(InlineHandler):
    def filter(self, query: InlineQuery):
        return query.query == 'hello'
    
    def inline(self, query: InlineQuery):
            self.bot.send_message(query.id, 'Hello to you')
```
#### Middlewares
Represented by middlewares.py file. Store a set of handlers that inherit from Middlware class stored in
easy_tbot.handlers.middleware
A example for edit message info
```python
from easy_tbot.handlers.middleware import Middleware,Message,TeleBot
from .models import User

class HelloMiddleware(Middleware):

    def middleware(self, bot: TeleBot, msg: Message):
        
        msg.register = User.get_user_from_db(msg.from_user.id) is not None
```
#### Models
Represented by models.py file. Store a set of ORM models that inherit from Model class stored in
easy_tbot.db.models
A example for user model
```python
from easy_tbot.db.models import Model, session_scope
from sqlalchemy import Column, String, Integer, Boolean
class User(Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)

    def __repr__(self):
        return self.username

    @staticmethod
    def get_user_from_db(_id):
        with session_scope() as s:
            return s.query(User).filter(User.id==_id).first()

```
#### Shells
Represented by shells.py file. Store a set of commands that inherit from ShellCommand class stored in
easy_tbot.shell.shell
A example for edit message info
```python
from easy_tbot.shell.shell import  ShellCommand

class HelloCommand(ShellCommand):
    name = 'hello'
    def do(self, *args, **kwargs):
        print('Hello from terminal!')
```
This command can be invoqued now with botmanager.py
```commandline
python botmanager.py hello
```
## To do stuff
They are the most demanded stuff for our mini framework, we want do all  this.

- [ ] Not only pyTelegramBotAPI as backend , telethon to
- [x] Support for commobly used data bases
- [ ] Support for mtproto proxy protocol
- [ ] A session system
- [ ] A user system
- [ ] A permission  system
- [ ] A markup on the fly system
- [ ] Support for webhooks