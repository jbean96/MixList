import sys
from setuptools import setup

magic_dist = None
if sys.platform.startswith('win32'):
    magic_dist = "python-magic-bin==0.4.14"
else:
    magic_dist = "python-magic==0.4.15"

setup(name="analyzer",
        version="0.1",
        description="Analyzer submodule for mixlist",
        author="Josh Bean",
        author_email="jbean96@cs.washington.edu",
        license="MIT",
        packages=["analyzer"],
        install_requires=[
            "librosa",
            "dill",
            "spotipy",
            magic_dist,
            "eyed3",
            "pytest",
            "tqdm"
        ],
        zip_safe=False)