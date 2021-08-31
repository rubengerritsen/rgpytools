from setuptools import find_packages, setup


setup(
  name="rgpytools", 
  packages=find_packages(include=['crystal']), 
  version='0.1.0', 
  description='personal python tools', 
  author='Ruben Gerritsen', 
  license='MIT',
  install_requires=['numpy', 'vpython'],
  setup_requires=['pytest-runner'],
  tests_require=['pytest'],
  test_suite='tests',)