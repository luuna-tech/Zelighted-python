import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = ''
with open('zelighted/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(),
                        re.MULTILINE).group(1)
if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='zelighted',
    version=version,
    description='Zelighted API Python Client',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    author='Zebrands',
    author_email='tech@zeb.mx',
    url='https://github.com/luuna-tech/Zelighted-python',
    packages=['zelighted'],
    package_dir={'zelighted': 'zelighted'},
    install_requires=['requests', 'tzlocal'],
    test_suite='test',
    test_requires=['pytz', 'tzlocal'],
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
