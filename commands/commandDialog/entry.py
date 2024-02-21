import adsk.core
import adsk.fusion
import os
from ...lib import fusion360utils as futil
from ... import config
app = adsk.core.Application.get()
ui = app.userInterface


# TODO *** Specify the command identity information. ***
CMD_ID = f'{config.COMPANY_NAME}_{config.ADDIN_NAME}_cmdDialog'
CMD_NAME = 'Ski Build Parameters'
CMD_Description = 'Ski build optimization function'

# Specify that the command will be promoted to the panel.
IS_PROMOTED = False

# TODO *** Define the location where the command button will be created. ***
# This is done by specifying the workspace, the tab, and the panel, and the 
# command it will be inserted beside. Not providing the command to position it
# will insert it at the end.
WORKSPACE_ID = 'FusionSolidEnvironment'
PANEL_ID = 'SolidScriptsAddinsPanel'
COMMAND_BESIDE_ID = 'ScriptsManagerCommand'
TAB_ID = config.tools_tab_id
TAB_NAME = config.my_tab_name
PANEL_ID = config.my_panel_id
PANEL_NAME = config.my_panel_name
PANEL_AFTER = config.my_panel_after

# Resource location for command icons, here we assume a sub folder in this directory named "resources".
# TODO *** Make new icons in the resource folder for the build ski button ***
ICON_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources','')

# Local list of event handlers used to maintain a reference so
# they are not released and garbage collected.
local_handlers = []


# Executed when add-in is run.
def start():
    # Create a command Definition.
    cmd_def = ui.commandDefinitions.addButtonDefinition(CMD_ID, CMD_NAME, CMD_Description, ICON_FOLDER)

    # Define an event handler for the command created event. It will be called when the button is clicked.
    futil.add_handler(cmd_def.commandCreated, command_created)

    # ******** Add a button into the UI so the user can run the command. ********
    # Get the target workspace the button will be created in.
    workspace = ui.workspaces.itemById(WORKSPACE_ID)

    toolbar_tab = workspace.toolbarTabs.itemById(TAB_ID)
    if toolbar_tab is None:
        toolbar_tab = workspace.toolbarTabs.add(TAB_ID, TAB_NAME)

    # Get the panel the button will be created in.
    panel = workspace.toolbarPanels.itemById(PANEL_ID)
    if panel is None:
        panel = toolbar_tab.toolbarPanels.add(PANEL_ID, PANEL_NAME, PANEL_AFTER, False)

    # Create the button command control in the UI after the specified existing command.
    control = panel.controls.addCommand(cmd_def)#, COMMAND_BESIDE_ID, False)

    # Specify if the command is promoted to the main toolbar. 
    control.isPromoted = IS_PROMOTED


# Executed when add-in is stopped.
def stop():
    # Get the various UI elements for this command
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    panel = workspace.toolbarPanels.itemById(PANEL_ID)
    command_control = panel.controls.itemById(CMD_ID)
    command_definition = ui.commandDefinitions.itemById(CMD_ID)

    # Delete the button command control
    if command_control:
        command_control.deleteMe()

    # Delete the command definition
    if command_definition:
        command_definition.deleteMe()


# Function that is called when a user clicks the corresponding button in the UI.
# This defines the contents of the command dialog and connects to the command related events.
def command_created(args: adsk.core.CommandCreatedEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME} Command Created Event')

    # https://help.autodesk.com/view/fusion360/ENU/?contextId=CommandInputs
    inputs = args.command.commandInputs

    # TODO Connect to the events that are needed by this command.
    futil.add_handler(args.command.execute, command_execute, local_handlers=local_handlers)
    futil.add_handler(args.command.inputChanged, command_input_changed, local_handlers=local_handlers)
    # futil.add_handler(args.command.executePreview, command_preview, local_handlers=local_handlers)
    # futil.add_handler(args.command.validateInputs, command_validate_input, local_handlers=local_handlers)
    futil.add_handler(args.command.destroy, command_destroy, local_handlers=local_handlers)

    # TODO Define the dialog for your command by adding different inputs to the command.
    mass_input = inputs.addFloatSliderCommandInput('mass_input','Skier mass [kg]','kg',20,100,False)
    height_input = inputs.addFloatSliderCommandInput('height_input','Skier height [cm]','cm',100,220,False)

    # Option 1: Drop down menu for skier level selection
    ski_lvl_drop_down_style = adsk.core.DropDownStyles.LabeledIconDropDownStyle
    ski_lvl_drop_down_input = inputs.addDropDownCommandInput('ski_lvl_drop_down_input', 'Skier Level', ski_lvl_drop_down_style)
    ski_lvl_drop_down_items = ski_lvl_drop_down_input.listItems
    ski_lvl_drop_down_items.add('Beginnger', False)
    ski_lvl_drop_down_items.add('Intermediate', True)
    ski_lvl_drop_down_items.add('Advanced', False)

    # Option 2: Radio Group menu for skier level selection
    # ski_lvl_radio_input = inputs.addRadioButtonGroupCommandInput('ski_lvl_radio_input', 'Skier Level')
    # ski_lvl_radio_items = ski_lvl_radio_input.listItems
    # ski_lvl_radio_items.add('Beginner', False)
    # ski_lvl_radio_items.add('Intermediate', True)
    # ski_lvl_radio_items.add('Advanced', False)
    # ski_lvl_radio_input.isFullWidth = True

    # # Option 3: Button row for skier level selection
    # ski_lvl_button_row_input = inputs.addButtonRowCommandInput('ski_lvl_button_row_input', 'Skier Level', False)
    # ski_lvl_button_row_input_list_items = ski_lvl_button_row_input.listItems
    # ski_lvl_button_row_input_list_items.add('Beginner', False,ICON_FOLDER)
    # ski_lvl_button_row_input_list_items.add('Intermediate', True,ICON_FOLDER)
    # ski_lvl_button_row_input_list_items.add('Advanced', False,ICON_FOLDER)
    # ski_lvl_button_row_input.isFullWidth = False

    # Option 1: Drop down menu for ski type selection
    # ski_type_drop_down_style = adsk.core.DropDownStyles.LabeledIconDropDownStyle
    # ski_type_drop_down_input = inputs.addDropDownCommandInput('ski_type_drop_down_input', 'Ski Type', ski_type_drop_down_style)
    # ski_type_drop_down_items = ski_type_drop_down_input.listItems
    # ski_type_drop_down_items.add('All mountain', True)
    # ski_type_drop_down_items.add('Downhill', False)
    # ski_type_drop_down_items.add('Backcountry', False)
    # ski_type_drop_down_items.add('Cross-country', False)
    # ski_type_drop_down_items.add('Nordic', False)

    # Option 2: Radio Group menu for ski type selection
    ski_type_radio_input = inputs.addRadioButtonGroupCommandInput('ski_type_radio_input', 'Ski Type')
    ski_type_radio_items = ski_type_radio_input.listItems
    ski_type_radio_items.add('All mountain', True)
    ski_type_radio_items.add('Downhill', False)
    ski_type_radio_items.add('Backcountry', False)
    ski_type_radio_items.add('Cross-country', False)
    ski_type_radio_items.add('Nordic', False)
    ski_type_radio_input.isFullWidth = True

    # Create some advanced selection criteria with core type and other?
    advanced_settings = inputs.addGroupCommandInput('advanced_settings', 'Advanced Settings')
    advanced_settings.isExpanded = False
    advanced_settings_children = advanced_settings.children

    # core_button_row_input = advanced_settings_children.addButtonRowCommandInput('core_button_row_input', 'Core Type', False)
    # core_button_row_input_list_items = core_button_row_input.listItems
    # core_button_row_input_list_items.add('Wood', False)
    # core_button_row_input_list_items.add('Honeycomb', True)
    # core_button_row_input_list_items.add('Metal', False)

    core_input = advanced_settings_children.addRadioButtonGroupCommandInput('core_input', 'Core Type')
    core_items = core_input.listItems
    core_items.add('Wood', True)
    core_items.add('Honeycomb', False)
    core_items.add('Metal', False)
    core_input.isFullWidth = True

    boot_offset_input = advanced_settings_children.addIntegerSliderCommandInput('boot_offset_input','Boot offset [cm]',-10,10)

    # # Create a value input field and set the default using 1 unit of the default length unit.
    # defaultLengthUnits = app.activeProduct.unitsManager.defaultLengthUnits
    # default_value = adsk.core.ValueInput.createByString('1')
    # inputs.addValueInput('value_input', 'Some Value', defaultLengthUnits, default_value)


# This event handler is called when the user clicks the OK button in the command dialog or 
# is immediately called after the created event not command inputs were created for the dialog.
def command_execute(args: adsk.core.CommandEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME} Command Execute Event')

    # TODO ******************************** Your code here ********************************

    #%% TODO *** create new design parameters with the input values from the dialog box ***
    # Create the design so that we can put our variables somewhere
    design = adsk.fusion.Design.cast(app.activeProduct)

    #%% TODO create new user parameters to store the input values indicated by the user

    #%% TODO *** call the buildSki python scripts to define load conditions, solve for stiffness matrix, optimize ply layup ***
    
    #%% TODO Use the solved optimization problem to define the camber profile line

    # Derive the ski parameters from the user input variables (PLACEHOLDERS)
    height = 162.0      # [cm]
    L_ski = height-20   # [cm]
    L_eff = L_ski-25    # [cm]
    boot_offset = 0     # [cm]
    w_waist = 9         # [cm]
    w_toe = 15          # [cm]
    w_tail = 15         # [cm]

    #%% Create the ski shape sketch from the derived parameters
    rootComp = design.rootComponent
    sketches = rootComp.sketches
    sketch: adsk.fusion.Sketch = sketches.add(rootComp.xYConstructionPlane)
    sketch.name = 'ski_base_shape'

    # Create a construction line for the full length of the ski
    sketchLines = sketch.sketchCurves.sketchLines
    startPoint = adsk.core.Point3D.create(0,0,0)
    endPoint = adsk.core.Point3D.create(L_ski,0,0)
    full_length = sketchLines.addByTwoPoints(startPoint,endPoint)
    full_length.isConstruction = True

    sketch.geometricConstraints.addCoincident(sketch.originPoint,full_length.startSketchPoint)
    sketch.geometricConstraints.addHorizontal(full_length)
    sketch.sketchDimensions.addDistanceDimension(full_length.startSketchPoint,full_length.endSketchPoint,0,startPoint)

    # Create a constructin line for the effective contact length of the ski
    start_eff = adsk.core.Point3D.create((L_ski-L_eff)/2-boot_offset,0,0)
    end_eff = adsk.core.Point3D.create((L_ski-L_eff)/2+L_eff-boot_offset,0,0)
    eff_length = sketchLines.addByTwoPoints(start_eff,end_eff)
    eff_length.isConstruction = True 

    sketch.geometricConstraints.addCollinear(eff_length,full_length)
    sketch.sketchDimensions.addDistanceDimension(eff_length.startSketchPoint,eff_length.endSketchPoint,0,start_eff)
    sketch.sketchDimensions.addDistanceDimension(full_length.startSketchPoint,eff_length.startSketchPoint,0,start_eff)

    # Create a construction line with waist, toe, and tail width
    waist_point_e = adsk.core.Point3D.create(L_ski/2,w_waist/2,0)
    waist_point_mirror_e = adsk.core.Point3D.create(L_ski/2,-w_waist/2,0)
    waist_point_s = adsk.core.Point3D.create(L_ski/2,0,0)
    waist = sketchLines.addByTwoPoints(waist_point_s,waist_point_e)
    waist.isConstruction = True

    waist_mirror = sketchLines.addByTwoPoints(waist_point_s,waist_point_mirror_e)
    waist_mirror.isConstruction = True

    mid_point = sketch.sketchPoints.add(adsk.core.Point3D.create(L_ski/2,0,0))
    mid_point.isFixed = True

    sketch.geometricConstraints.addCoincident(mid_point,waist.startSketchPoint)
    sketch.geometricConstraints.addVertical(waist)
    sketch.sketchDimensions.addDistanceDimension(waist.startSketchPoint,waist.endSketchPoint,0,waist_point_s)

    sketch.geometricConstraints.addCoincident(mid_point,waist_mirror.startSketchPoint)
    sketch.geometricConstraints.addVertical(waist_mirror)
    sketch.sketchDimensions.addDistanceDimension(waist_mirror.startSketchPoint,waist_mirror.endSketchPoint,0,waist_point_s)

    toe_point = adsk.core.Point3D.create((L_ski-L_eff)/2-boot_offset,w_toe/2,0)
    toe_point_mirror = adsk.core.Point3D.create((L_ski-L_eff)/2-boot_offset,-w_toe/2,0)
    toe_point_s = adsk.core.Point3D.create((L_ski-L_eff)/2-boot_offset,0,0)
    toe = sketchLines.addByTwoPoints(toe_point_s,toe_point)
    toe.isConstruction = True

    toe_mirror = sketchLines.addByTwoPoints(toe_point_s,toe_point_mirror)
    toe_mirror.isConstruction = True

    sketch.geometricConstraints.addCoincident(eff_length.startSketchPoint,toe.startSketchPoint)
    sketch.geometricConstraints.addVertical(toe)
    sketch.sketchDimensions.addDistanceDimension(toe.startSketchPoint,toe.endSketchPoint,0,toe_point)

    sketch.geometricConstraints.addCoincident(eff_length.startSketchPoint,toe_mirror.startSketchPoint)
    sketch.geometricConstraints.addVertical(toe_mirror)
    sketch.sketchDimensions.addDistanceDimension(toe_mirror.startSketchPoint,toe_mirror.endSketchPoint,0,toe_point_mirror)

    tail_point = adsk.core.Point3D.create((L_ski-L_eff)/2+L_eff-boot_offset,w_tail/2,0)
    tail_point_mirror = adsk.core.Point3D.create((L_ski-L_eff)/2+L_eff-boot_offset,-w_tail/2,0)
    tail_point_s = adsk.core.Point3D.create((L_ski-L_eff)/2+L_eff-boot_offset,0,0)
    tail = sketchLines.addByTwoPoints(tail_point_s,tail_point)
    tail.isConstruction = True

    tail_mirror = sketchLines.addByTwoPoints(tail_point_s,tail_point_mirror)
    tail_mirror.isConstruction = True

    sketch.geometricConstraints.addCoincident(eff_length.endSketchPoint,tail.startSketchPoint)
    sketch.geometricConstraints.addVertical(tail)
    sketch.sketchDimensions.addDistanceDimension(tail.startSketchPoint,tail.endSketchPoint,0,tail_point)

    sketch.geometricConstraints.addCoincident(eff_length.endSketchPoint,tail_mirror.startSketchPoint)
    sketch.geometricConstraints.addVertical(tail_mirror)
    sketch.sketchDimensions.addDistanceDimension(tail_mirror.startSketchPoint,tail_mirror.endSketchPoint,0,tail_point_mirror)

    # Create the side cut arc
    sketchArcs = sketch.sketchCurves.sketchArcs
    sidecut = sketchArcs.addByThreePoints(toe_point,waist_point_e,tail_point)
    sketch.geometricConstraints.addCoincident(sidecut.startSketchPoint,toe.endSketchPoint)
    sketch.geometricConstraints.addCoincident(sidecut.endSketchPoint,tail.endSketchPoint)
    sketch.sketchDimensions.addRadialDimension(sidecut,waist_point_e)

    sidecut_mirror = sketchArcs.addByThreePoints(tail_point_mirror,waist_point_mirror_e,toe_point_mirror)
    sketch.geometricConstraints.addCoincident(sidecut_mirror.endSketchPoint,toe_mirror.endSketchPoint)
    sketch.geometricConstraints.addCoincident(sidecut_mirror.startSketchPoint,tail_mirror.endSketchPoint)
    sketch.sketchDimensions.addRadialDimension(sidecut_mirror,waist_point_mirror_e)

    # Create the toe and tail shapes
    sketchSplines = sketch.sketchCurves.sketchFittedSplines
    
    toe_points = adsk.core.ObjectCollection.create()
    toe_points.add(toe_point)
    toe_points.add(startPoint)
    toe_spline = sketchSplines.add(toe_points)
    toe_spline1 = toe_spline.activateTangentHandle(toe_spline.fitPoints.item(0))
    toe_spline2 = toe_spline.activateTangentHandle(toe_spline.fitPoints.item(1))
    
    sketch.geometricConstraints.addTangent(toe_spline1,sidecut)
    sketch.geometricConstraints.addVertical(toe_spline2)

    toe_points_mirror = adsk.core.ObjectCollection.create()
    toe_points_mirror.add(toe_point_mirror)
    toe_points_mirror.add(startPoint)
    toe_spline_mirror = sketchSplines.add(toe_points_mirror)
    toe_spline_mirror1 = toe_spline_mirror.activateTangentHandle(toe_spline_mirror.fitPoints.item(0))
    toe_spline_mirror2 = toe_spline_mirror.activateTangentHandle(toe_spline_mirror.fitPoints.item(1))
    
    sketch.geometricConstraints.addTangent(toe_spline_mirror1,sidecut_mirror)
    sketch.geometricConstraints.addVertical(toe_spline_mirror2)
    
    tail_points = adsk.core.ObjectCollection.create()
    tail_points.add(tail_point)
    tail_points.add(endPoint)
    tail_spline = sketchSplines.add(tail_points)
    tail_spline1 = tail_spline.activateTangentHandle(tail_spline.fitPoints.item(0))
    tail_spline2 = tail_spline.activateTangentHandle(tail_spline.fitPoints.item(1))
    
    sketch.geometricConstraints.addTangent(tail_spline1,sidecut)
    sketch.geometricConstraints.addVertical(tail_spline2)

    tail_points_mirror = adsk.core.ObjectCollection.create()
    tail_points_mirror.add(tail_point_mirror)
    tail_points_mirror.add(endPoint)
    tail_spline_mirror = sketchSplines.add(tail_points_mirror)
    tail_spline_mirror1 = tail_spline_mirror.activateTangentHandle(tail_spline_mirror.fitPoints.item(0))
    tail_spline_mirror2 = tail_spline_mirror.activateTangentHandle(tail_spline_mirror.fitPoints.item(1))
    
    sketch.geometricConstraints.addTangent(tail_spline_mirror1,sidecut_mirror)
    sketch.geometricConstraints.addVertical(tail_spline_mirror2)
    
    sketch.sketchDimensions.addDistanceDimension(toe_spline1.endSketchPoint, toe_spline1.startSketchPoint,0,startPoint)
    sketch.sketchDimensions.addDistanceDimension(toe_spline2.endSketchPoint, toe_spline2.startSketchPoint,0,startPoint)
    sketch.sketchDimensions.addDistanceDimension(toe_spline_mirror1.endSketchPoint, toe_spline_mirror1.startSketchPoint,0,startPoint)
    sketch.sketchDimensions.addDistanceDimension(toe_spline_mirror2.endSketchPoint, toe_spline_mirror2.startSketchPoint,0,startPoint)
    sketch.sketchDimensions.addDistanceDimension(tail_spline1.endSketchPoint, tail_spline1.startSketchPoint,0,startPoint)
    sketch.sketchDimensions.addDistanceDimension(tail_spline2.endSketchPoint, tail_spline2.startSketchPoint,0,startPoint)
    sketch.sketchDimensions.addDistanceDimension(tail_spline_mirror1.endSketchPoint, tail_spline_mirror1.startSketchPoint,0,startPoint)
    sketch.sketchDimensions.addDistanceDimension(tail_spline_mirror2.endSketchPoint, tail_spline_mirror2.startSketchPoint,0,startPoint)

    #%% TODO Create a sketch line defined by the camber profile line

    #%% TODO Create the 3d model of the ski

    #%% TODO Add top layer picture

    #%% TODO Generate 3d model & save & export step file for modeling in FEM

    #%% Get a reference to your command's inputs.
    inputs = args.command.commandInputs
    text_box: adsk.core.TextBoxCommandInput = inputs.itemById('text_box')
    value_input: adsk.core.ValueCommandInput = inputs.itemById('value_input')
    # print(inputs)

    # Display the palette that represents the TEXT COMMANDS palette
    text_palette = ui.palettes.itemById('TextCommands')
    if not text_palette.isVisible:
        text_palette.isVisible = True
    
    # Do something interesting
    # text = text_box.text
    # expression = value_input.expression
    msg = f'See cmmand summary logs in the Text Commands Palette'
    ui.messageBox(msg)


# This event handler is called when the command needs to compute a new preview in the graphics window.
def command_preview(args: adsk.core.CommandEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME} Command Preview Event')
    inputs = args.command.commandInputs


# This event handler is called when the user changes anything in the command dialog
# allowing you to modify values of other inputs based on that change.
def command_input_changed(args: adsk.core.InputChangedEventArgs):
    changed_input = args.input
    inputs = args.inputs

    # General logging for debug.
    futil.log(f'{CMD_NAME} Input Changed Event fired from a change to {changed_input.id}')


# This event handler is called when the user interacts with any of the inputs in the dialog
# which allows you to verify that all of the inputs are valid and enables the OK button.
def command_validate_input(args: adsk.core.ValidateInputsEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME} Validate Input Event')

    inputs = args.inputs
    
    # Verify the validity of the input values. This controls if the OK button is enabled or not.
    valueInput = inputs.itemById('value_input')
    if valueInput.value >= 0:
        args.areInputsValid = True
    else:
        args.areInputsValid = False
        

# This event handler is called when the command terminates.
def command_destroy(args: adsk.core.CommandEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME} Command Destroy Event')

    global local_handlers
    local_handlers = []
