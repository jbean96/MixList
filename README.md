# MixList

CSE 481I: Sound Design capstone project for Josh Bean, Jeremy Cruz and Gerard Gaimari

## Updates

Use this section to write about TODOs and other updates on your part of the project

### Analyzer

(2/5/19) Working on integrating the Spotify API to get metadata about songs and matching the correct song with the songs that the user wants to use in their mix. 

**TODO**
- [ ] Finish integrating Spotify matching
- [ ] Make matching and song loading run in parallel
- [ ] Add key detection on the user loaded song
- [ ] Indicate which of the detected beats are downbeats with a boolean

**NOTES**
[Downbeat Detection](https://www.eecs.qmul.ac.uk/~markp/2006/DaviesPlumbley06-eusipco.pdf)

### Optimizer

### Composer

Composer class contains of a list of instructions and methods for carrying out instructions
(2/14/19) - Contact Audacity regarding float support for SelectTime command

**TODO**
- [ ] Finish implementing effects
- [ ] Fix bugs regarding SelectTime
- [ ] Converting Optimizer output from samples to timestamps 

## Other

Resources, papers, other things to note

### Resources

[LibROSA](https://librosa.github.io/librosa/)<br/>
[Onset/Beat Detection Paper](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=1495485)<br/>
[Beat Tracking Algorithm](http://www.ee.columbia.edu/~dpwe/pubs/Ellis07-beattrack.pdf)<br/>
