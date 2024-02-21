# Assuming you have not changed the general structure of the template no modification is needed in this file.
from . import commands
from .lib import fusion360utils as futil
import adsk.core
import adsk.fusion

def run(context):
    try:
        # Display a message when the add-in is manually run.
        if not context['IsApplicationStartup']:
            app = adsk.core.Application.get()
            ui = app.userInterface
            ui.messageBox('A new "Build Ski" panel has been added to the "UTILITIES" tab.', 'Command Samples')

        # This will run the start function in each of your commands as defined in commands/__init__.py which will get the user input values
        commands.start()

    except:
        futil.handle_error('run')


def stop(context):
    try:
        # Remove all of the event handlers your app has created
        futil.clear_handlers()

        # This will run the start function in each of your commands as defined in commands/__init__.py
        commands.stop()

    except:
        futil.handle_error('stop')