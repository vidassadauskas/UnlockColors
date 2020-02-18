"""
February 11-13, 2020
Recipe: ?????   # TODO: Q: What is recipe
@author: Vidas Sadauskas
"""
# TODO: try to rewrite the application using pygame.
# TODO: try to rewrite the application using Pyglet.

# ======================================
# Import required libraries and modules
# ======================================
import configparser
import matplotlib as mpl
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import Menu
from tkinter import ttk
from tkinter import messagebox

# ======================================
# Initialize variables
# ======================================
# TODO: Q: Are those global constants? Or should I put them in the corresponding classes?
size = 0.3      # radius of the inner pie
colors = ['orange', 'yellow', 'green', 'blue', 'purple', 'red']     # colors of the inner and unlocked pies.
grays = ['lightgray', 'gainsboro', 'darkgray', 'dimgray', 'gray', 'silver']     # colors of the outer gray pie
wedgeSizes = [1., 1., 1., 1., 1., 1.]       # sized (proportions of wedges
wedgeLabels = ["--"] * 6                    # initial labels of the wedges TODO: Should be not an array but a list? ...
# TODO: ... How to populate a list (?) with identical values? Is it OK to provide an array instead of a list (?) for ...
#       ... an argument? And what happens when we do so?
lblDistance = 0.5 + size/2                  # placement of the labels (distance from the center
AppTitle = "Atrakink spalvas!"              # Title of the application


# Create the main window
class MainWindow:
    def __init__(self, master):
        # ======================================
        # Initialize instance variables
        # ======================================
        self.MainWindowTitle = AppTitle             # Title of the main window
        self.ConfigFileName = "UnlockColors.ini"    # Name of the configuration file
        self.ButtonLabel = "Pradėti"                # Label of the button
        self.ButtonFont = ('Arial', '50', 'bold')   # Configuration of the font of the button label
        self.ActiveButtonBackground = 'red'         # Background color when the button is under the cursor
        self.ActiveButtonForeground = 'white'       # Foreground color when the button is under the cursor.
        self.ConfigMenuItemLabel = "Nustatymai"     # Label of the settings menu item
        self.FileMenuLabel = "Meniu"                # Label of the main (file) menu
        self.ExitMenuItemLabel = "Išeiti"           # Label of the exit menu item
        self.ErrorMsgBoxTitle = "Klaida"            # Title of the error message box
        self.ErrorMsgConfigFileAccess = "Klaida mėginant nuskaityti konfigūracijos failą " + self.ConfigFileName + "."
        self.OkButtonLabel = "Gerai"                # Label of OK button
        # Colors used in the color wheel
        self.Colors = ('red', 'orange', 'yellow', 'green', 'blue', 'purple')
        # Here we will keep color unlock codes
        self.ColorUnlockCodes = {
            self.Colors[0]: 99,
            self.Colors[1]: 99,
            self.Colors[2]: 99,
            self.Colors[3]: 99,
            self.Colors[4]: 99,
            self.Colors[5]: 99
        }
        self.FieldLabelColorNames = {
            self.Colors[0]: "Raudonos",
            self.Colors[1]: "Oranžinės",
            self.Colors[2]: "Geltonos",
            self.Colors[3]: "Žalios",
            self.Colors[4]: "Mėlynos",
            self.Colors[5]: "Purpurinės"
        }
        # A name of the configuration file section containing the color unlock codes
        self.ColorUnlockCodesSectionName = "Color Unlock Codes"
        # Here we will keep the application configuration
        self.Configuration = {self.ColorUnlockCodesSectionName: self.ColorUnlockCodes}
        # Create a configuration file parser instance
        self.Config = configparser.ConfigParser()
        # Get configuration from a configuration file or set to default values if the configuration file is absent.
        self.get_options()

        # Define a window for the application
        # Assign the argument "master" to the instance variable "self.master" to use in other functions of the class
        self.master = master
        self.master.geometry("400x400")     # TODO: do we need to specify the geometry of the window? Try to comment out
        #                                           and see what happens.

        # Set the main window title
        self.master.title(self.MainWindowTitle)

        # Add a button
        self.action = tk.Button(self.master, text=self.ButtonLabel, activebackground=self.ActiveButtonBackground,
                                activeforeground=self.ActiveButtonForeground, font=self.ButtonFont,
                                command=self.enter_fullscreen)
        # Center the button
        self.action.place(relx=0.5, rely=0.5, anchor='center')
        # TODO: Change the size and color (and font size of the button label?) of the button

        # Create a menu bar
        self.menuBar = Menu(self.master)
        self.master.config(menu=self.menuBar)

        # Add menu items
        self.fileMenu = Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label=self.ConfigMenuItemLabel, command=lambda: self.new_window(OptionsWindow))
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label=self.ExitMenuItemLabel, command=self._quit)
        self.menuBar.add_cascade(label=self.FileMenuLabel, menu=self.fileMenu)
        # TODO: Add Help menu and About menu item

        # Empty menu. It will be used to hide the menu bar in the main window
        self.empty_menu = Menu(self.master)

        # Bind keys with functions
        self.master.bind("<F11>", self.enter_fullscreen)
        self.master.bind("<Escape>", self.quit_fullscreen)

    # Make the main window full screen
    def enter_fullscreen(self, *event):
        self.master.attributes("-fullscreen", True)     # Enter full screen
        self.master.config(menu=self.empty_menu)        # Hide the menu bar
        self.action.place_forget()                      # Hide the button

    # Exit fullscreen
    def quit_fullscreen(self, event):
        self.master.attributes("-fullscreen", False)            # Exit full screen
        self.master.config(menu=self.menuBar)                   # Restore the menu bar
        self.action.place(relx=0.5, rely=0.5, anchor='center')  # Restore the button

    # Open a child window
    # While we need this function to open only the Options window, make it universal to open any child window in the
    # future.
    # TODO: But in this case we will need to deal with different sets of arguments first.
    def new_window(self, _class):
        # Avoiding opening the same window more than once.
        try:
            if self.new.state() == 'normal':
                self.new.focus()
        # TODO: ERROR: "Too broad exception clause"
        except:
            # TODO: ERROR: "Instance attribute new defined outside __init__"
            self.new = tk.Toplevel(self.master, takefocus=True)
            self.new.focus()
            _class(self.new, self)

    # Retrieve options from a configuration file
    def get_options(self):
        # Check if the configuration file exists
        try:
            # Read configurations from the configuration file
            f = open(self.ConfigFileName)
            self.Config.read_file(f)
            f.close()
            # TODO: handle exceptions when ParsingError etc. https://docs.python.org/3.7/library/configparser.html
            # Update configuration values in the variable where application configuration is kept
            for clrs in self.Colors:
                index = self.Colors.index(clrs)
                self.Configuration[self.ColorUnlockCodesSectionName][clrs] = \
                    self.Config.getint(self.ColorUnlockCodesSectionName, clrs)
                # That's all the configuration at the moment
        except FileNotFoundError:
            # If the configuration file is not found, assign current values of the variable containing
            # the configuration dictionary to the configuration file parser instance.
            self.Config.read_dict(self.Configuration)
        except (IOError, PermissionError):
            # In case of other errors when trying to access the configuration file, just show an error message and exit.
            messagebox.showerror(self.ErrorMsgBoxTitle, self.ErrorMsgConfigFileAccess, parent=self.master)
            self._quit()

        # TODO: handle the case when the configuration file is not found
        # TODO: How to detect that the configuration file is present of absent?
        # TODO: Config parsers do not guess data types of values in configuration files, always storing them internally
        #       as strings.This means that if you need other data types, you should convert on your own:
        #          >> > int(topsecret['Port'])

    # TODO: Canvas widget
    #       https://web.archive.org/web/20190510131423/http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/canvas.html)
    #       To create a Canvas object:
    #           w = tk.Canvas(parent, option=value, ...)
    #       A canvas is a rectangular area intended for drawing pictures or other complex layouts.
    #       On it you can place graphics, text, widgets, or frames.
    #       Supported options include:
    #           height      Size of the canvas in the Y dimension. See Section 5.1, “Dimensions”.
    #           width       Size of the canvas in the X dimension. See Section 5.1, “Dimensions”
    #           confine      If true (the default), the canvas cannot be scrolled outside of the scrollregion
    #                       (see below).
    #           .......
    # TODO: Canvas arc objects
    #       An arc object on a canvas, in its most general form, is a wedge-shaped slice taken out of an ellipse.
    #        To create an arc object on a canvas C, use:
    #            id = C.create_arc(x0, y0, x1, y1, option, ...)
    #        Point (x0, y0) is the top left corner and (x1, y1) the lower right corner of a rectangle into which the
    #        ellipse is fit. If this rectangle is square, you get a circle.
    #       The various options include:
    #           extent      Width of the slice in degrees. The slice starts at the angle given by the start option
    #                       and extends counterclockwise for extent degrees.
    #           start       Starting angle for the slice, in degrees, measured from +x direction.
    #                       If omitted, you get the entire ellipse.
    #           state       This option is tk.NORMAL by default. It may be set to tk.HIDDEN to make the arc invisible
    #                       or to tk.DISABLED to gray out the arc and make it unresponsive to events.
    #           style       The default is to draw the whole arc; use style=tk.PIESLICE for this style.
    #           .....
    # TODO: Canvas oval objects
    #       Ovals, mathematically, are ellipses, including circles as a special case.
    #       To create an ellipse on a canvas C, use:
    #            id = C.create_oval(x0, y0, x1, y1, option, ...)
    #        Options for ovals:
    #           state        By default, oval items are created in state tk.NORMAL. Set this option to tk.DISABLED to
    #                        make the oval unresponsive to mouse actions. Set it to tk.HIDDEN to make the item
    #                        invisible.
    #           .....
    # TODO: Canvas text objects
    #       You can display one or more lines of text on a canvas C by creating a text object:
    #           id = C.create_text(x, y, option, ...)
    #       Options include:
    #           state       By default, the text item's state is tk.NORMAL. Set this option to tk.DISABLED to make in
    #                       unresponsive to mouse events, or set it to tk.HIDDEN to make it invisible.
    #           text        The text to be displayed in the object, as a string. Use newline characters ('\n')
    #                       to force line breaks.
    #       You can change the text displayed in a text item.
    #           - To retrieve the text from an item with object ID I on a canvas C, call C.itemcget(I, 'text').
    #           - To replace the text in an item with object ID I on a canvas C with the text from a string S,
    #               call C.itemconfigure(I, text=S).
    # TODO: Canvas window objects
    #       You can place any Tkinter widget onto a canvas by using a canvas window object. A window is a rectangular
    #       area that can hold one Tkinter widget. The widget must be the child of the same top-level window as
    #       the canvas, or the child of some widget located in the same top-level window.
    #       To create a new canvas window object on a canvas C:
    #           id = C.create_window(x, y, option, ...)
    #       Options include:
    #           window      Use window=w where w is the widget you want to place onto the canvas. If this is omitted
    #                       initially, you can later call C.itemconfigure (id, window=w) to place the widget w onto
    #                       the canvas, where id is the window's object ID..
    #           ......
    #
    #       aa
    #

    # Exit GUI cleanly
    # TODO: Q: How to exit GUI cleanly?
    def _quit(self):
        self.master.quit()
        self.master.destroy()
        exit()


# Options window
class OptionsWindow:
    def __init__(self, master, parent):
        # ======================================
        # Initialize instance variables
        # ======================================
        self.OptionsWindowTitle = AppTitle + " - Nustatymai"    # Title of the window
        self.Tab1Label = "Spalvų atrakinimo kodai"     # Label of the tab where color unlocking codes are set
        self.Frame1Label = " Čia surašykite spalvų atrakinimo kodus: "     # Label of the frame with unlocking codes
        self.ColorUnlockFieldLabels = []                    # An array of labels for entries of color unlock codes
        self.SaveButtonLabel = "Išsaugoti"                  # Label of the Save button
        self.CancelButtonLabel = "Uždaryti"                 # Label of the Cancel button
        self.ColorUnlockCodes = []              # An array of variables associated with entries of color unlock codes
        self.ColorUnlockCodeEntries = []   # An array of Textbox Entry widgets for color unlock code

        self.master = master
        self.parent = parent

        # Set the title of the configuration window
        self.master.title("Nustatymai - Atrakink spalvas!")

        # Create all the tabs. labels, fields etc of the window
        self.create_widgets()

    def create_widgets(self):
        # Tab Control introduced here --------------------------------------
        self.tabControl = ttk.Notebook(self.master)     # Create Tab Control

        self.tab1 = ttk.Frame(self.tabControl)          # Create a tab
        self.tabControl.add(self.tab1, text=self.Tab1Label)  # Add the tab

        self.tabControl.pack(expand=1, fill="both")  # Pack to make visible
        # ~ Tab Control introduced here -----------------------------------------

        # We are creating a container frame to hold all other widgets
        self.Frame1 = ttk.LabelFrame(self.tab1, text=self.Frame1Label)
        self.Frame1.grid(column=0, row=0, padx=16, pady=16)

        for clrs in self.parent.Colors:
            index = self.parent.Colors.index(clrs)
            # Populate the array of labels for fields of color unlock codes
            self.ColorUnlockFieldLabels.append(self.parent.FieldLabelColorNames[clrs] + " spalvos kodas: ")
            # Create the array of variables associated with entries of color unlock codes
            self.ColorUnlockCodes.append(tk.IntVar())
            # Populate the array with current unlock code values from the main window
            self.ColorUnlockCodes[index].set(self.parent.Configuration[self.parent.ColorUnlockCodesSectionName][clrs])
            # Set a label for a fields of color unlock code
            ttk.Label(self.Frame1,
                      text=self.ColorUnlockFieldLabels[index]).grid(column=0, row=index, padx=4, pady=4, sticky='E')
            # Add a Textbox Entry widget for color unlock code
            # TODO: Somehow ensure that entered value is either one- or two-digit number.
            #       See https://web.archive.org/web/20190524022302/...
            #       ...http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/entry-validation.html
            self.ColorUnlockCodeEntries.append(ttk.Entry(self.Frame1, width=12,
                                                         textvariable=self.ColorUnlockCodes[index]))
            self.ColorUnlockCodeEntries[index].grid(column=1, row=index, padx=4, pady=4, sticky='W')

        # Create Save button
        # Adding a Button
        self.SaveButton = ttk.Button(self.master, text=self.SaveButtonLabel, command=self.save_options)
        self.SaveButton.pack(expand=1, fill='x', side='left')

        # Create Cancel button
        # Adding a Button
        self.CancelButton = ttk.Button(self.master, text=self.CancelButtonLabel, command=self._quit)
        # self.CancelButton.grid(column=2, row=1)
        self.CancelButton.pack(expand=1, fill='x', side='right')

    # Save options to a configuration file
    def save_options(self):
        # Update the variables keeping the configuration dictionary
        # Update color unlock codes to the values in the corresponding entries
        for clrs in self.parent.Colors:
            index = self.parent.Colors.index(clrs)
            self.parent.Config.set(self.parent.ColorUnlockCodesSectionName, clrs,
                                   str(self.ColorUnlockCodes[index].get()))
            self.parent.Configuration[self.parent.ColorUnlockCodesSectionName][clrs] = \
                self.ColorUnlockCodes[index].get()
            # That's all the configuration at the moment
        # Write the configuration to the configuration file
        with open(self.parent.ConfigFileName, 'w') as self.ConfigFile:
            self.parent.Config.write(self.ConfigFile)

    # Exit GUI cleanly
    def _quit(self):
        self.master.destroy()


# Create instance of the main window
win = tk.Tk()
app = MainWindow(win)

# TODO: set application icon
# Change the main windows icon
# win.iconbitmap(r'C:\Python34\DLLs\pyc.ico')

# create a figure with subplots
fig, ax = plt.subplots()

# change the font size of the labels by dynamically changing the rc settings
mpl.rcParams['font.size'] = 40.0

# draw the outer pie (donut)
wedges, texts = ax.pie(wedgeSizes, radius=1, colors=grays, labels=wedgeLabels, labeldistance=lblDistance,
                       wedgeprops=dict(width=1-size), textprops=dict(va='center', ha='center'))
# draw the inner pie
ax.pie(wedgeSizes, radius=size, colors=colors, wedgeprops=dict(width=size))

# trying to manipulate a separate wedge of the donut
# plt.setp(wedges[0], color='red')

# ======================================
# Show the plot
# ======================================
# plt.show()

if __name__ == "__main__":      # TODO: Why is this needed?
    # ======================================
    # Start GUI
    # ======================================
    win.mainloop()
