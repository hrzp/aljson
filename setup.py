
from setuptools import setup


setup(name='aljson',
      version='0.2.0',
      description='Convert a SqlAlchemy query object to a dict(json)',
      long_description=open('README.rst').read(),
      url='https://github.com/hrzp/aljson',
      download_url='https://github.com/hrzp/aljson/archive/0.2.0.tar.gz',
      author='Hamid Reza Zarepour',
      author_email='hamid.zarepour.dev@gmail.com',
      license='MIT',
      packages=['aljson'],
      zip_safe=False,
      install_requires=['sqlalchemy']
      )
