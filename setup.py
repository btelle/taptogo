from setuptools import setup

setup(
    name='taptogo',
    packages=['taptogo'],
    version = "0.1",
    include_package_data=True,
    install_requires=[
        'selenium',
        'BeautifulSoup4'
    ],
)
