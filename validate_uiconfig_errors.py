"""
Validate UI Config errors commonly caused by third party plugins

How to run:
import validate_uiconfig_errors as vue
vue.auto_fix()
"""
import maya.cmds as cmds
import re


# Constants
# List desired UI Callbacks to be removed and compile them into a regex pattern object
BAD_UI_CALLBACKS = ['DCF_updateViewportList;', 'CgAbBlastPanelOptChangeCallback', 'onModelChange3dc']
BAD_UI_CALLBACKS_COMPILED = re.compile('|'.join(BAD_UI_CALLBACKS))
BAD_PANEL_DICT = {}

# Functions 
def validate():
    """
    Validate and report if there are error prone callbacks in the model panels
    """
    # Check model panels for bad callbacks and add to dict
    for model_panel in cmds.getPanel(typ="modelPanel"):
        model_callback = cmds.modelEditor(model_panel, query=True, editorChanged=True)
        bad_cb = re.match(BAD_UI_CALLBACKS_COMPILED, model_callback)
        if bad_cb:
            # Add the entire matched callback to a dict for fixing later
            # (this can include other non erroneous callbacks if they are alongside the bad callback)
            BAD_PANEL_DICT[model_panel] = bad_cb.string

    if BAD_PANEL_DICT:
        print("Bad UI callbacks found: {0}.".format(BAD_PANEL_DICT.values()))
        return BAD_PANEL_DICT
    else:
        print('No bad UI callbacks found.')

def fix():
    """
    Fix error prone callbacks in the model panels
    """
    try:
        for model_panel in BAD_PANEL_DICT:
            # remove the bad callbacks from the panels while preserving non erroneous callbacks
            new_callback = re.sub(BAD_UI_CALLBACKS_COMPILED, '', BAD_PANEL_DICT[model_panel])
            cmds.modelEditor(model_panel, edit=True, editorChanged=new_callback)
    except Exception as e:
        print(e)
    else:
        print("Removed bad UI callbacks: {0}.".format(BAD_PANEL_DICT.values()))

def auto_fix():
    """
    Validate and fix
    """
    if validate():
        fix()