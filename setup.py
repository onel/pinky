from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


# tutorial: 
# https://python-packaging.readthedocs.io/en/latest/index.html
setup(name='pinky',
        version='0.1',
        description='Create easy email templates with python',
        long_description=readme(),
        keywords='html email templates inky',
        url='https://github.com/onel/pinky',
        author='Andrei Onel',
        author_email='andrei@edumo.org',
        license='MIT',
        packages=['pinky'],
        # https://pypi.org/pypi?%3Aaction=list_classifiers
        classifiers=[
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Topic :: Text Processing :: Markup :: HTML'
        ],
        entry_points = {
            'console_scripts': ['pinky=pinky.command_line:main'],
        },
        install_requires=[
            'premailer',
            'beautifulsoup4'
        ],
        # include_package_data=True,
        zip_safe=False)