"""===============================================================================

        FILE: setup.py

       USAGE: (not intended to be directly executed)

 DESCRIPTION: 

     OPTIONS: ---
REQUIREMENTS: ---
        BUGS: ---
       NOTES: ---
      AUTHOR: Alex Leontiev (nailbiter@dtws-work.in)
ORGANIZATION: Datawise Inc.
     VERSION: ---
     CREATED: 2020-11-18T15:49:09.362113
    REVISION: ---

==============================================================================="""

from setuptools import setup, find_packages


def get_install_requires(fn="requirements.txt"):
    with open(fn) as f:
        lines = f.readlines()
    lines = map(lambda s: s.strip(), lines)
    lines = filter(lambda s: not s.startswith("#"), lines)
    return list(lines)


setup(
    name='alex_eel',
    version='1.0.1',
    py_modules=[]
    packages=find_packages(
        include=["alex_eel"],
        # exclude=["bin"]
    ),
    install_requires=get_install_requires(),
    #    entry_points='''
    #        [console_scripts]
    #        acomposer2=acomposer2:cli
    #    ''',
)