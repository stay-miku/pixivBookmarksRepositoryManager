from setuptools import setup, find_packages

setup(
    name='pbrm',
    version='0.0.1',
    description='A pixiv bookmarks local backup tool',
    author='stay_miku',
    author_email='none',
    url='https://github.com/yourusername/myproject',
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
