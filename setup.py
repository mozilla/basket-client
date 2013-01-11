from setuptools import setup, find_packages

import basket as distmeta


setup(
    name='basket-client',
    version=distmeta.__version__,
    description=distmeta.__doc__,
    long_description=open('README.rst').read(),
    author=distmeta.__author__,
    author_email=distmeta.__contact__,
    license=distmeta.__license__,
    packages=find_packages(exclude=['ez_setup']),
    install_requires=['requests'],
    url=distmeta.__homepage__,
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "License :: OSI Approved :: BSD License",
        "Topic :: Communications",
        'Topic :: Software Development :: Libraries',
    ],
    keywords=['mozilla', 'basket']
)
