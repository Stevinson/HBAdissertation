# HBAdissertation

This repository includes code for the thesis entitled 'Utilising Policy Types to Achieve 
Effective Ad Hoc Coordination in the Game Othello'. It uses Harsanyi-Bellman Ad Hoc
Coordination to model the opponent type, in this case in the board game Othello. This 
assumes that it is playing heterogeneous agents and that we do not know, a priori, how
other agents behave. Also included is a copy of the finished dissertation report.

## Setup

### play game

```
conda create env
pip install poetry
poetry config virtualenvs.create false --local
poetry install
python main.py BlackAgent="human", WhiteAgent="hba"
```

### dev

```
make git-hooks
```

Project Organization 
------------

    ├── MSc Report        <- Dissertation report
    │
    └── python            <- Python code used for the experiments
        │
        ├── agents
        │  
        └── game            
--------
