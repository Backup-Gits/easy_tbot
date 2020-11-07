from setuptools import setup

with open('README.md', 'r') as f:
    description = f.read()

setup(
    name='easy_tbot',
    version='1.0',
    packages=['easy_tbot', 'easy_tbot.db', 'easy_tbot.bot', 'easy_tbot.shell', 'easy_tbot.handlers',
              'easy_tbot.handlers.setup'],
    install_requires=['pyTelegramBotAPI~=3.7.3', 'SQLAlchemy~=1.3.19'],
    entry_points={'console_scripts': ['tbot-admin=easy_tbot.tbot_admin:main'], },
    url='',
    license='GNU LESSER GENERAL PUBLIC LICENSE',
    author='Jesús Enrique Fuentes González',
    author_email='jesusefg12@gmail.com',
    description='Framework  for data base and other usefull stuff integration with Telegram bot api',
    long_description=description,
    long_description_content_type="text/markdown",
    python_requires='>=3.6',

)
