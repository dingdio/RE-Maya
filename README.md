# RE-Maya
These Maya tools allow you to import animation from RE Engine games. Currently RE2R, RE3R and DMC have been tested.

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


