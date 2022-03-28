from setuptools import setup, find_packages

setup(
	name='project1',
	version='1.0',
	author='Rachana Vellampalli',
	authour_email='rachana@ou.edu',
	packages=find_packages(exclude=('tests', 'docs')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
)
