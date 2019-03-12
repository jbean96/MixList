# MixList

CSE 481I: Sound Design capstone project for Josh Bean, Jeremy Cruz and Gerard Gaimari

## Installing Audacity

Before everything can work together you need to download the source code for Audacity and install it with `mod-script-pipe` enabled. There are instructions for downloading the source code and installing it [here](https://www.audacityteam.org/download/source/). There is also some information about enabling `mod-script-pipe` [here](https://manual.audacityteam.org/man/scripting.html). In order to get it to run on Windows we had to build and run from Visual Studio. For some reason running Audacity from the executable file wouldn't allow `mod-script-pipe` to work even though it was enabled.

## Top Level

- `main.py` runs the GUI for MixList. By default it will create a cache in the folder you are running it from called `mixlist_cache`. There it will store all the serialized analyses for files that it has analyzed.
- `pipe_test.py` is called from `main.py` to test the connection to Audacity. For some reason, after mixing one song and pressing `Test Audacity` it doesn't work correctly although you can still mix.

## Folders/Modules

- `analyzer` contains the code for the analyzer portion of MixList and also defines some of the data structures used throughout the pipeline
    - **NOTE**: Before running you'll need to `cd analyzer/` and run `pip install .`, the `analyzer` uses a lot of third party libraries so it's best that we put those dependencies in `setup.py`. There were a number of issues configuring the `eyed3` module however we reverted the version to be installed to not import the `python-magic` library which was causing issues.
- `composer` contains the code for the MixList composer.
- `composer_scripts` was a folder containing some of the test scripts we used when developing the composer.
- `keyfinder` contains code for a keyfinding algorithm. It's a fairly simple module since it can just use the LibROSA command for getting the constant q transform of an audio file which otherwise would be a fair amount of code. We didn't end up integrating this into our platform because the results weren't great.
- `optimizer` contains the code for MixList optimization.
- `proposal` contains the writeup of our proposal and a script to compile it with `pandoc`
- `scripts` contains some scripts that we used during the development process