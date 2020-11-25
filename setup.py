from setuptools import setup

with open('README.md', 'r') as f:
    description = f.read()

setup(
    name='easy_tbot',
    version='1.0.2b5',
    packages=['easy_tbot', 'easy_tbot.db', 'easy_tbot.bot', 'easy_tbot.shell', 'easy_tbot.handlers',
              'easy_tbot.handlers.setup', 'easy_tbot.render'],
    install_requires=['pyTelegramBotAPI~=3.7.3', 'SQLAlchemy~=1.3.19'],
    entry_points={'console_scripts': ['create-tbot=easy_tbot.tbot_admin:main'], },
    url='https://github.com/Gaspect/easy_tbot',
    license='GNU LESSER GENERAL PUBLIC LICENSE',
    author='Jesús Enrique Fuentes González',
    author_email='jesusefg12@gmail.com',
    description='Mini framework  for data base and other usefull stuff integration with Telegram bot api',
    long_description=description,
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
    classifiers=[
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)"
    ]
)
