# MixList

CSE 481I: Sound Design capstone project for Josh Bean, Jeremy Cruz and Gerard Gaimari

## Modules

- `analyzer` contains the code for the analyzer portion of MixList and also defines some of the data structures used throughout the pipeline
    - **NOTE**: Before running you'll need to `cd analyzer/` and run `pip install .`, the `analyzer` uses a lot of third party libraries so it's best that we put those dependencies in `setup.py`. There were a number of issues configuring the `eyed3` module 