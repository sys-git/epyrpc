#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages
    
setup(
    name="epyrpc",
    version="0.1",
    url='https://github.com/sys-git/epyrpc',
    packages=find_packages(),
    package_dir={'epyrpc': 'epyrpc'},
    include_package_data=True,
    author="Francis Horsman",
    author_email="francis.horsman@gmail.com",
    description="Object based pure Python RPC.",
    license="GNU General Public License",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Communications',
    ]
)
