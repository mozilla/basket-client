from setuptools import setup, find_packages


setup(
    name='basket',
    version='0.2.0',
    description="A Python client for Mozilla's basket service",
    long_description=open('README.rst').read(),
    author='Michael Kelly',
    author_email='mkelly@mozilla.com',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    install_requires=['requests'],
    url='https://github.com/Osmose/basket-client',
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Software Development :: Libraries',
        ],
    keywords=['mozilla', 'basket'],
    **extra_setup
)
