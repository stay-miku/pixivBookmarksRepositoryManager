from setuptools import setup, find_packages

setup(
    name='pbrm',
    version='0.0.5',
    description='A pixiv bookmarks local backup tool',
    author='stay_miku',
    author_email='miku@miku.pics',
    url='',
    packages=find_packages(),
    install_requires=[
        "requests",
        "lxml",
        "docopt"
    ],
    entry_points={
        'console_scripts': [
            'pbrm=pbrm.main:main',
        ],
    }
)
