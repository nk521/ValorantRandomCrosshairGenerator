# Valorant Random Crosshair Generator (VRCG)

## Installation
### Method 1
1. Download exe from here: https://github.com/nk521/ValorantRandomCrosshairGenerator/releases/latest
2. Run it and allow UAC

### Method 2
```bash
python3 -m pip install virtualenv
python3 -m virtualenv env
. env/bin/activate

# in virtual enviornment
pip install -r requirements.txt
```

To run:
```bash
python valorant_crosshair.py [optional]
```

* If ran without optional:
    * In valorant, click on import crosshair and hit F12 to automatically fill it with new crosshair code.
    * Note that everytime you hit F12, it is going to fill your's computer clipboard history.

* If ran with optional:
    * Just hit `enter`/`return` to generate a new crosshair and copy it to clipboard automatically!
    * Enter `q`, `exit` or `quit` to quit the prompt.
    * Enter an `int` to generate that many crosshairs; these won't be copied to clipboard.
