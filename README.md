# RE-Maya
This Maya tool allows you to import animations and cameras from RE Engine games into Maya. It currently supports Resident Evil 2 Remake (RE2R), Resident Evil 3 Remake (RE3R) and Devil May Cry 5 (DMC5).

## Changelog

7th March 2021 (v0.1):
* can now import cameras

## Requirements
Tool has been tested on Maya 2020.4

Get the game files with [REtool](https://residentevilmodding.boards.net/thread/10567/pak-tex-editing-tool).

To export animation you need the appropriate model in the scene from one of the RE Engine games.
Get the models with the noesis script and import them into Maya using FBX:

[Noesis Script Download](https://residentevilmodding.boards.net/thread/13501/exporting-custom-models-dmc5-noesis)


If you don't want seams on your model try this mel command before you import
```
FBXProperty "Import|IncludeGrp|Geometry|OverrideNormalsLock" -v 1
```
## Installation

1. Drag and drop the "install.mel" file onto the Maya viewport.

2. Click the RE Engine icon that appears on the shelf to run.


## Manual Installation

Add src/RE_Engine folder to your maya scripts directory, start Maya and run the following code in the Python script editor.

```
import RE_Engine
reload(RE_Engine)
RE_Engine.re_tool.RE_Manager(dock=False)
```
## Credits
PredatorCZ for creating the [RevilMax](https://github.com/PredatorCZ/RevilMax) importer for 3ds Max.

alphaZ, Che and Jackal for their contributions to the 010 Editor Motlist Template and  [Motlist Tool](https://residentevilmodding.boards.net/thread/14132/motlist-maxscript-custom-animations-engine) which this tool is based on.



