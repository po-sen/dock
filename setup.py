from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as fp:
    long_description = fp.read()

setup(
    name='dock-cli',
    version='0.3.1',
    author='Posen',
    author_email='posen2101024@gmail.com',
    description='CLI for manage container applications',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=[
        'click==8.1.7',
    ],
    entry_points='''
        [console_scripts]
        dock=dock_cli.main:cli
    ''',
)
