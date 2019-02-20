# Core Module Interactions

## Analyzer

### Input:

- `list of songs`:
    - directory containing audio files 
    - parses directory and gets all existing metadata from songs

### Output:
- `unordered list of song objects`:
    - `song_analysis_object`:
        - file_path (relative : string)
        - [prop_1, prop_2, ... , prop_N]
            - tempo (BPM : float)
            - key (Camelot : string)
            - mood (Scale : float)
            - energy (Scale : float)
        - [sect_1, sect_2, ... , sect_M]
            - `section`:
                - start_sample (range : long)
                - end_sample (range : long)
                - array_of_beats: [sample_num_1, sample_num_2, ... , sample_num_N] (array : long)
                - key (Camelot : string) 
                - tempo (BPM : float)
                - 4_beat_avg_amplitude_start (0 - 1 : float)
                - 4_beat_avg_amplitude_end (0 - 1 : float)
                - avg_amplitude (0 - 1 : float)
                - section_classification (chorus, verse, build-up, drop, etc... : string)
                    - determined by grouping average frequency of 4 beat sections

## Optimizer

### Input:
- `output from analyzer`

### Output:
- `ordered list of song objects (size : N)`:
    - `song_analysis_object`

- `ordered list of transition dicts (size : N - 1)` [{transition from A to B}, {transition from B to C}, ... ,{}]
    - `song_a` Track a of transition, analyzed Song object.
    - `song_b` Track b of transition, analyzed Song object.
    - `sections` [{section 0}, {section 1}, ... , {}]
        - `section`:
            - index of track A start beat (index : integer)
            - index of track B start beat (index : integer)
            - number of beats in the section (length : integer)
            - transitions applied to that section (name of transition : string) --> [transition_name_1, transition_name_2, ... , transition_name_N]
            
## Composer

### Input:
- `output from analyzer`

### Output:
- `MIXTAPE (an audio file)`