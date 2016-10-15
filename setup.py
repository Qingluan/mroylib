

from setuptools import setup, find_packages


setup(name='Mroylib',
    version='1.1.4',
    description='add duckduck go  module based on',
    url='https://git.oschina.net/dark.h/Mroylib.git',
    author='Qing luan',
    author_email='darkhackdevil@gmail.com',
    license='MIT',
    zip_safe=False,
    packages=find_packages(),
    install_requires=['Qtornado','redis', 'psycopg2','pymysql','fabric3','requests','lxml','bs4','termcolor','bson','simplejson'],

)


