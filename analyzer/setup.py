from setuptools import setup

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
            "python-magic-bin==0.4.14",
            "eyed3",
            "pytest",
            "tqdm"
        ],
        zip_safe=False)