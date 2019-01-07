from setuptools import setup, find_packages


setup(
    name='basket-client',
    version='1.0.0',
    description="A Python client for Mozilla's basket service.",
    long_description=open('README.rst').read(),
    author='Michael Kelly and contributors',
    author_email='dev-mozilla-org@lists.mozilla.org',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    install_requires=['requests', 'six'],
    url='https://github.com/mozilla/basket-client',
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "License :: OSI Approved :: BSD License",
        "Topic :: Communications",
        'Topic :: Software Development :: Libraries',
    ],
    keywords=['mozilla', 'basket'],
    test_suite="basket.tests.TestBasketClient",
    tests_require=['mock==2.0.0'],
)
