from setuptools import setup, find_packages

setup(
        name='gcalendar',
        version='0.1',
        description='TODO',
        url='http://github.com/pylipp/gcalendar',
        author='navjot12, Philipp Metzner',
        author_email='beth.aleph@yahoo.de',
        license='GPLv3',
        #classifiers=[],
        packages=find_packages(exclude=['test', 'doc']),
        entry_points = {
            'console_scripts': ['gcalendar = gcalendar.main:main']
            },
        install_requires=[]
        )
