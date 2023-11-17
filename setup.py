from setuptools import setup, find_packages

setup(
    name='pbrm',
    version='0.2.1',
    description='A pixiv bookmarks local backup tool',
    author='stay_miku',
    author_email='miku@miku.pics',
    url='https://github.com/stay-miku/pixivBookmarksRepositoryManager',
    packages=find_packages(),
    install_requires=[
        "requests",
        "lxml",
        "docopt",
        "bottle"
    ],
    entry_points={
        'console_scripts': [
            'pbrm=pbrm.main:main',
        ],
    },
    package_data={"pbrm.web_server": ["template/*"]}
)
