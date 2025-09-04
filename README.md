# High Framerate Video Recorder
*v0.1.0*

Little CLI tool written in Python made to record videos at high framerate with the Alvium cameras from Allied Vision.

## Installation

To test the tool, just clone the project, install the dependencies and your're good to go !

```console
git clone https://github.com/1m0ut0n/av-alvium-cli-recorder.git
cd av-alvium-cli-recorder
pip install -r requirements.txt
py cli.py --help
```

But I recommmend using a virtual environment.

```console
git clone https://github.com/1m0ut0n/av-alvium-cli-recorder.git
cd av-alvium-cli-recorder
python -m venv .venv
pip install -r requirements.txt
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate  # Windows
py cli.py --help
```

## Usage

The tool give you two differents commands :

**`infos` :** Configure the camera with the given options and then print all the valuable infos about the current configuration. To know how to use it, type  `py cli.py infos --help`.

**`record` :** Configure the camera with the given options and record a video that is then saved in the output path. To know how to use it, type  `py cli.py record --help`.

## Current limitations

**This tool has currently some limitations, some choices had to be made for the short timing that we had...** It maybe will be improved in the future. You can also feel free to fork it or make some PR !
- It is impossible to decide of the FPS, it will always be set to the max available value depending on the current camera configuration.
- Sometimes, the video encoding codec does not support the specific framerate that is set on the camera, and we don't check it before, so depending on the current FPS, an error can be raised.
- Sometimes, at very high framerates, it seems that some frames misses somes chunk of data at the bottom

## Tech stack

## Roadmap

- [ ] Put the video writer logic into a specific well written class
- [ ] Fix the imncomplete frame problem, certainly comming from the buffer logic
- [ ] Make the camera framerate changeable
- [ ] Make the tool packageable so that it can be installed with `pip`

## Changelog

 - ***v0.0.1:** Main features (command line tool, camera handler, video recorder, ...)*