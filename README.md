# easy_tbot
Mini framework for database and other useful stuff integration with Telegram bot api
## Motivation
The biggest motivation was when I wanted to make my first bot on Telegram using python. I had many modules like telethon or pyTelegramBotApi but it did not solve the idea of how to structure the project, how to make it join a database and other integrations. The most important thing if I wanted to do another project, would I have to repeat all the code? Thus was born easy_tbot. Another motivation that came as a divine sign was to try to copy (test purpose) a friend's bot, a .py of more than 3000 lines of code -_-
## Installation
````commandline
pip install easy-tbot
````
## How create a project?
Once installed run the command.
```commandline
create-tbot bot_name
```
The command will create the structure for the projects explained below.
## Project structure
- Project
  - Sections (a set of sections folders)
  - settings.py
  - botmanager.py
### The settings.py file
Here we hold all framework configuration stuff.

| Variable name | Wat they do |
| ------------- | ------------- |
| BASEDIR  | Stores the project direction  |
| SECTIONS | Stores what sections must be loaded with |
| DB.NAME | Sqlalchemy connection string |
| DB.EXTRA | Others args for sqlalchemy connection in dict form |
| TOKEN | The token provided by Telegram botfather's bot for using your own bot |
| TEMPLATES.DIR | Save the directory where the template engine should look |
| TEMPLATES.AUTO_ESCAPE | Defines which file extensions it should read |
| PROXY | The proxy for connect with Telegram (MTPROTO not allowed ...!!yet!!) |
| DEBUG | Controls if the framework can display debug's information |
### The botmanager.py file 
A file that stores an entry point for our full bot. There are 3 basic commands allowed and others can be added.

1. Create a section
   - ```commandline  
     python botmanager.py createsection <name> 
     ```
2. Set up the data base
   - ```commandline  
     python botmanager.py migrate
     ```
3. Run the bot
   - ```commandline  
     python botmanager.py run
     ```

### Sections
Sections are logicall-separated parts of our bot. They are formed by handler, inlines, middlewares, models, and shells explained below.

- Section
  - handlers.py
  - inlines.py
  - middlewares.py
  - models.py
  - shells.py
  
#### Handlers
Represented by handlers.py file. Stores a set of handlers that inherit from All, Command, Regex, Function classes.
An example of a reply to the /start command
```python

from easy_tbot import Command, types

class StartCommand(Command):
    commands = ['start']

    def handle(self, msg: types.Message):
        self.bot.reply_to(msg, 'Hello world!!!')
```
#### Inlines
Represented by inlines.py file. Stores a set of handlers that inherit from InlineHandler.
An example of a reply made to the 'hello' inline button
```python
from easy_tbot import  InlineHandler, types

class HelloInline(InlineHandler):
    def inline_filter(self, query: types.InlineQuery):
        return query.query == 'hello'
    
    def inline(self, query: types.InlineQuery):
        answer = types.InlineQueryResultArticle(1,'hola',types.InputTextMessageContent('hola'))
        try:
            self.bot.answer_inline_query(query.id,[answer])
        except:
            pass
        
```
#### Middlewares
Represented by middlewares.py file. Stores a set of handlers that inherit from Middlware class.
An example of how to edit a message's info
```python
from easy_tbot.handlers.middleware import Middleware,types,Bot
from .models import User

class HelloMiddleware(Middleware):

    def middleware(self, bot: Bot, msg: types.Message):
        
        msg.register = User.get_user_from_db(msg.from_user.id) is not None
```
#### Models
Represented by models.py file. Stores a set of ORM models that inherit from Model.
An example off a user model
```python
from easy_tbot.db import Model, session_scope, Column, Integer, String, Boolean


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
Represented by shells.py file. Stores a set of commands that inherit from ShellCommand class.
```python
from easy_tbot import  ShellCommand

class HelloCommand(ShellCommand):
    name = 'hello'
    def do(self, *args, **kwargs):
        print('Hello from terminal!')
```
This command can be used now with botmanager.py
```commandline
python botmanager.py hello
```
## Class Mixing
Some times we make a bot with same logic for a set of user input, since easy_tbot use class systme for user logic representation.
Mixing class functionality is in part easy.
```python
from easy_tbot import Mixing, Command, Regex, types

class Hello(Mixing,Command,Regex):
    commands = ['hello']
    regex = r'hello'
    def handle(self, msg: types.Message):
        self.bot.reply_to(msg, 'Hello to you')
```

## Release Notes
If you migrate from version previous to v1.0.2b5, you must fixed import problems
class like 'Model' and methods like 'session_scope' where movo from 'easy_tbot' to 'easy_tbot.db'
## Thanks
My thanks to [GowterZil](https://github.com/GowtherZil) a newborn of zen.

