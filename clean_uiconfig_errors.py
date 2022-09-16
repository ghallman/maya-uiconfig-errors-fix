"""
Modified script from https://gist.github.com/BigRoy for broader usage
Iterates through model panels to remove problematic callbacks
"""
import maya.cmds as cmds
import re

# List desired UI Callbacks to be removed and compile them into a regex pattern object
bad_ui_callbacks = ['DCF_updateViewportList;','CgAbBlastPanelOptChangeCallback','onModelChange3dc']
bad_ui_callbacks = re.compile('|'.join(bad_ui_callbacks))

for model_panel in cmds.getPanel(typ="modelPanel"):
    # Get callback of the model editor
    model_callback = cmds.modelEditor(model_panel, query=True, editorChanged=True)
    # Replace bad callbacks with empty string
    new_callback = re.sub(bad_ui_callbacks, '', model_callback)
    
    # Remove callback
    cmds.modelEditor(model_panel, edit=True, editorChanged=new_callback)
