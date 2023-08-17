from setuptools import find_packages, setup

setup(
    name = 'conversational-ai',
    version = '0.1',
    description = 'microservices for conversational agents',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    author = 'Cesar Flres',
    author_email = 'cfloressuazo@gmail.com',
    maintainer = 'Cesar Flores',
    maintainer_email = 'cfloressuazo@gmail.com',
)
