from setuptools import setup

description = ''
with open('README.md', 'r') as f:
    description = f.read()

setup(
    name='easy_tbot',
    version='1.0',
    packages=['easy_tbot', 'easy_tbot.db', 'easy_tbot.bot', 'easy_tbot.shell', 'easy_tbot.handlers',
              'easy_tbot.handlers.setup'],
    url='',
    license='GNU LESSER GENERAL PUBLIC LICENSE',
    author='Jesús Enrique Fuentes González',
    author_email='jesusefg12@gmail.com',
    description='Framework  for data base and other usefull stuff integration with Telegram bot api',
    long_description=description,
    long_description_content_type="text/markdown",
)
