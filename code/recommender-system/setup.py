from setuptools import setup, find_packages

setup(name='recommender-system',
      version='0.1',
      description='Provides movie recommedations for users based on their rating history',
      url='https://github.com/rasmunk/set11521cw2',
      author='Rasmus Munk',
      author_email='40161642@live.napier.ac.uk',
      license='MIT',
      packages=find_packages(),
      install_requires=['SQLAlchemy', 'MySQL-python'],
      scripts=['bin/SetupDatabase', 'bin/RunRecommenderSystem']
      )
