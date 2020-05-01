from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="py-json-serialize", 
    version="0.8.0",
    description = "json serialize library for Python 2 and 3",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/randydu/py-json-serialize.git",
    author="Randy Du",
    author_email="randydu@gmail.com",
    packages=["py_json_serialize"],
    keywords=["serialize", "json"],
    license="MIT",
    classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers', 
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
  ],

)