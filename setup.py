#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re
from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-pg-current-timestamp',
    version='0.2.4',
    author='Jay Taylor',
    author_email='jay@jaytaylor.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/threatstream/django-pg-current-timestamp',
    license=open(os.path.join(os.path.dirname(__file__), 'LICENSE'), 'r').read(),
    description='Add true postgresql `CURRENT_TIMESTAMP` support to Django + PostgreSQL',
    long_description='Documentation is available on github: https://github.com/threatstream/django-pg-current-timestamp',
    requires=map(lambda s: re.sub(r'([<>!=].*)$', r'(\1)', s), open(os.path.join(os.path.dirname(__file__), 'requirements.txt'), 'r').read().strip().split('\n')),
    install_requires=map(lambda s: re.sub(r'([<>!=,]+)', r' \1 ', s).strip(), open(os.path.join(os.path.dirname(__file__), 'requirements.txt'), 'r').read().strip().split('\n')),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database',
        'Topic :: Database :: Database Engines/Servers',
    ],
    test_suite='runtests.runtests',
    zip_safe=False,
)

