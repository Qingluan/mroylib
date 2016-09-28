

from setuptools import setup, find_packages


setup(name='Mroylib',
    version='0.2',
    description='some lib',
    url='https://github.com/Qingluan/Q.git',
    author='Qing luan',
    author_email='darkhackdevil@gmail.com',
    license='MIT',
    zip_safe=False,
    packages=find_packages(),
    install_requires=['Qtornado','redis','pymysql','fabric3','requests','lxml','bs4','termcolor','bson','simplejson'],

)


