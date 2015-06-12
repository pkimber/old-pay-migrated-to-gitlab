import os
from distutils.core import setup


def read_file_into_string(filename):
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


def get_readme():
    for name in ('README', 'README.rst', 'README.md'):
        if os.path.exists(name):
            return read_file_into_string(name)
    return ''


setup(
    name='kb-pay',
    packages=['pay', 'pay.management', 'pay.management.commands', 'pay.migrations', 'pay.tests'],
    package_data={
        'pay': [
            'templates/*.*',
            'templates/pay/*.*',
        ],
    },
    version='0.1.28',
    description='pay',
    author='Malcolm Dinsmore',
    author_email='m.dinsmore@talk21.com',
    url='git@github.com:pkimber/pay.git',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Office/Business :: Scheduling',
    ],
    long_description=get_readme(),
)
