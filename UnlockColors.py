"""
February 11-13, 2020
Recipe: ?????   # TODO: Q: What is recipe
@author: Vidas Sadauskas
"""
# TODO: try to rewrite the application using pygame.
# TODO: try to rewrite the application using Pyglet.
# TODO: what is the line limit according to PEP8? Why in Atom it is 80
#       characters, in PyCharm - 120, in Spyder of Anaconda - ??? Which is
#       right? How to fix it in IDE where it is not right to make them right
#       and the same in all the IDE?
# TODO: FIXME: move the main window to a secondary display ---> set to
#       fullscreen ---> the window opens fullscreen in another (main) display.
#       How to make the window remain in the same display?
# FIXME:    Sort out when instance variables and when local variables should
#           be declared and used and fix the code.

# ======================================
# Import required libraries and modules
# ======================================
import configparser
import tkinter as tk
from tkinter import Menu
from tkinter import ttk
from tkinter import messagebox
import matplotlib as mpl
import matplotlib.pyplot as plt

# ======================================
# Initialize variables
# ======================================
# TODO: Q: Are those global constants? Or should I put them in the
#       corresponding classes?
size = 0.3      # radius of the inner pie
# colors of the inner and unlocked pies.
colors = ['yellow', 'green', 'blue', 'purple', 'red', 'orange']
# colors of the outer gray pie
grays = ['lightgray', 'gainsboro', 'darkgray', 'dimgray', 'gray', 'silver']
wedgeSizes = [1., 1., 1., 1., 1., 1.]       # sized (proportions of wedges
wedgeLabels = ["--"] * 6                    # initial labels of the wedges
# TODO: Should be not an array but a list? ...
# TODO: ... How to populate a list (?) with identical values? Is it OK to
#       provide an array instead of a list (?) for an argument? And what
#       happens when we do so?
lblDistance = 0.5 + size/2  # placement of the labels (distance from the center
AppTitle = "Atrakink spalvas!"  # Title of the application


# Create the main window
class MainWindow:
    def __init__(self, master):
        # ======================================
        # Initialize instance variables
        # ======================================
        self.MainWindowTitle = AppTitle             # Title of the main window
        # Name of the configuration file
        self.ConfigFileName = "UnlockColors.ini"
        self.ButtonLabel = "Pradėti"                # Label of the button
        # Configuration of the font of the button label
        self.ButtonFont = ('Arial', '50', 'bold')
        # Background color when the button is under the cursor
        self.ActiveButtonBackground = 'red'
        # Foreground color when the button is under the cursor.
        self.ActiveButtonForeground = 'white'
        # Label of the settings menu item
        self.ConfigMenuItemLabel = "Nustatymai"
        self.FileMenuLabel = "Meniu"          # Label of the main (file) menu
        self.ExitMenuItemLabel = "Išeiti"     # Label of the exit menu item
        self.ErrorMsgBoxTitle = "Klaida"      # Title of the error message box
        self.ErrorMsgConfigFileAccess = "Klaida mėginant nuskaityti " +\
                                        "konfigūracijos failą " +\
                                        self.ConfigFileName + "."
        self.OkButtonLabel = "Gerai"                # Label of OK button
        # Colors used in the color wheel
        self.Colors = ('yellow', 'green', 'blue', 'purple', 'red', 'orange')
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
            self.Colors[0]: "Geltonos",
            self.Colors[1]: "Žalios",
            self.Colors[2]: "Mėlynos",
            self.Colors[3]: "Purpurinės",
            self.Colors[4]: "Raudonos",
            self.Colors[5]: "Oranžinės"
        }
        # A name of the configuration file section containing the color unlock
        # codes
        self.ColorUnlockCodesSectionName = "Color Unlock Codes"
        # Here we will keep the application configuration
        self.Configuration =\
            {self.ColorUnlockCodesSectionName: self.ColorUnlockCodes}
        # Create a configuration file parser instance
        self.Config = configparser.ConfigParser()
        # Get configuration from a configuration file or set to default values
        # if the configuration file is absent.
        self.get_options()

        # Define a window for the application
        # Assign the argument "master" to the instance variable "self.master"
        # to use in other functions of the class
        self.master = master
        self.master.geometry("400x400")     # Default size of the main window

        # Set the main window title
        self.master.title(self.MainWindowTitle)

        # Create a menu bar
        self.menuBar = Menu(self.master)
        self.master.config(menu=self.menuBar)

        # Add menu items
        self.fileMenu = Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label=self.ConfigMenuItemLabel,
                                  command=lambda:
                                  self.new_window(OptionsWindow))
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label=self.ExitMenuItemLabel,
                                  command=self._quit)
        self.menuBar.add_cascade(label=self.FileMenuLabel, menu=self.fileMenu)
        # TODO: Add Help menu and About menu item

        # Empty menu. It will be used to hide the menu bar in the main window
        self.empty_menu = Menu(self.master)

        # Add a button
        self.action = tk.Button(self.master, text=self.ButtonLabel,
                                activebackground=self.ActiveButtonBackground,
                                activeforeground=self.ActiveButtonForeground,
                                font=self.ButtonFont,
                                command=self.enter_fullscreen)
        # Center the button
        self.action.place(relx=0.5, rely=0.5, anchor='center')
        # TODO: Change the size and color (and font size of the button label?)
        #       of the button

        # Bind keys with functions
        self.master.bind("<F11>", self.enter_fullscreen)
        self.master.bind("<Escape>", self.quit_fullscreen)

        # Create a canvas where pies will be placed.
        self.Canvas = tk.Canvas(self.master)
        # Create a color pie instance
        # Size of the pie compared to the containing window
        self.PieRatio = 1.0
        self.Pie = ColorPie(self.master, self.Canvas, self.ColorUnlockCodes,
                            self.PieRatio)
        # TODO: Make the size of the pie configurable in the options window
        # Create the inner color pie
        # Size of the inner pie compared to the outer pie
        self.Pie2PieRatio = 0.3
        # Size of the inner pie compared to the containing window
        self.Pie0Ratio = self.PieRatio * self.Pie2PieRatio
        self.Pie0 = ColorPie(self.master, self.Canvas, self.ColorUnlockCodes,
                             self.Pie0Ratio)

    # Make the main window full screen
    def enter_fullscreen(self, *event):
        self.master.config(menu=self.empty_menu)        # Hide the menu bar
        self.action.place_forget()                      # Hide the button
        self.master.attributes("-fullscreen", True)     # Enter full screen
        # Extend the canvas to the length of the shortest side of the window
        # Width of the calling window
        width = self.master.winfo_width()
        # Height of the calling window
        height = self.master.winfo_height()
        # Size of the canvas
        canvas_size = int(min(width, height))
        # Resize the canvas
        self.Canvas.configure(width=canvas_size, height=canvas_size)
        # Expand the pies to the full screen
        self.Pie.resize(self.master, self.PieRatio)
        self.Pie0.resize(self.master, self.Pie0Ratio)
        self.Pie.show()                                 # Show the color pie
        self.Pie0.show()                                # Show the inner pie
        # Some tasks in updating the display, such as resizing and redrawing
        # widgets, are called idle tasks because they are usually deferred
        # until the application has finished handling events and has gone back
        # to the main loop to wait for new events. If you want to force the
        # display to be updated before the application next idles, call the
        # w.update_idletasks() method on any widget.
        # TODO: Do we really need this?:
        self.master.update_idletasks()
        # FIXME:    When the window is fullscreen, the taskbar is visible an
        #           top of the window

    # Exit fullscreen
    def quit_fullscreen(self, event):
        self.master.attributes("-fullscreen", False)    # Exit full screen
        self.master.config(menu=self.menuBar)           # Restore the menu bar
        # Restore the button
        self.action.place(relx=0.5, rely=0.5, anchor='center')
        # Resize the canvas to the length of the shortest side of the window
        # Width of the calling window
        # ? print("exit fullscreen", self.width)
        width = self.master.winfo_width()
        # Height of the calling window
        height = self.master.winfo_height()
        # Size of the canvas
        canvas_size = int(min(width, height))
        # Resize the canvas
        self.Canvas.configure(width=canvas_size, height=canvas_size)
        # Shrink the pies to the normal screen
        self.Pie.resize(self.master, self.PieRatio)
        self.Pie0.resize(self.master, self.Pie0Ratio)
        self.Pie.hide()                                 # Hide the color pie
        self.Pie0.hide()                                # Hide the inner pie
        # TODO: Do we really need this?:
        self.master.update_idletasks()

    # Open a child window
    # While we need this function to open only the Options window, make it
    # universal to open any child window in the future.
    # TODO: But in this case we will need to deal with different sets of
    #       arguments first.
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
            # TODO: handle exceptions when ParsingError etc.
            #       https://docs.python.org/3.7/library/configparser.html
            # Update configuration values in the variable where application
            # configuration is kept
            for clrs in self.Colors:
                self.Configuration[self.ColorUnlockCodesSectionName][clrs] = \
                    self.Config.getint(self.ColorUnlockCodesSectionName, clrs)
                # That's all the configuration at the moment
        except FileNotFoundError:
            # If the configuration file is not found, assign current values of
            # the variable containing the configuration dictionary to the
            # configuration file parser instance.
            self.Config.read_dict(self.Configuration)
        except (IOError, PermissionError):
            # In case of other errors when trying to access the configuration
            # file, just show an error message and exit.
            messagebox.showerror(self.ErrorMsgBoxTitle,
                                 self.ErrorMsgConfigFileAccess,
                                 parent=self.master)
            self._quit()

    # Exit GUI cleanly
    # TODO: Q: How to exit GUI cleanly?
    def _quit(self):
        self.master.quit()
        self.master.destroy()
        exit()


# The color pie
class ColorPie:
    def __init__(self, master, canvas, color_unlock_codes, ratio):
        # ======================================
        # Initialize instance variables
        # ======================================
        self.Wedges = []    # An array of wedges forming a color pie
        # Assign arguments to instance variables to use them in other functions
        # of the class
        self.master = master
        self.canvas = canvas
        self.ColorUnlockCodes = color_unlock_codes
        # TODO: what is the correct form of naming of instance variables:
        #       camelCase, CamelCase or snake_case?
        # ratio - a ratio of diameter of the pie and the shortest border
        # (width or height, given as arguments to this function) of the
        # calling window.
        # Expected values are from 0.0 to 1.0. 1.0 means the pie fills all the
        # window, i. e. 100%. If the value is greater than 1.0 then it is set
        # to 1.0. If the value is less than 0.0 (i. e. if it is a negative
        # value) then it is set to 0.0.
        self.ratio = max(min(ratio, 1.0), 0.0)
        # Width of the calling window

        # Create a canvas for the color pie but do not show it yet.
        length = len(self.ColorUnlockCodes)     # Total number of wedges
        a = int('60', 16)       # Decimal code of the lightest shade of gray
        b = int('A0', 16)       # Decimal code of the darkest shade of gray
        self.outline_thickness = 10   # Thickness of active outline of a pie
        # Create a color pie as an array wedges but do not show them yet
        # Using enumerate since we need indexes (remember that dictionaries
        # don't have an order):
        for index, color in enumerate(self.ColorUnlockCodes):
            # Shades of gray have to be distributed evenly from the lightest
            # to the darkest.
            rnd = format(int(a + index * (b - a) / length), 'x')
            shade_of_gray = "#" + rnd * 3
            self.Wedges.append(
                self.canvas.create_arc(0, 0, 1, 1,
                                       start=(index+1)*360/length,
                                       extent=360/length,
                                       fill=shade_of_gray,
                                       outline=shade_of_gray,
                                       activeoutline=color,
                                       activewidth=self.outline_thickness,
                                       disabledfill=color,
                                       tags=color, style=tk.PIESLICE,
                                       state=tk.HIDDEN)
                                 )

    # Resize the pie
    def resize(self, master, ratio):
        self.master = master
        # ratio - a ratio of diameter of the pie and the shortest border
        # (width or height, given as arguments to this function) of the
        # calling window.
        # Expected values are from 0.0 to 1.0. 1.0 means the pie fills all the
        # window, i. e. 100%. If the value is greater than 1.0 then it is set
        # to 1.0. If the value is less than 0.0 (i. e. if it is a negative
        # value) then it is set to 0.0.
        self.ratio = max(min(ratio, 1.0), 0.0)
        # Size of the canvas
        canvas_size = min(self.master.winfo_width(),
                          self.master.winfo_height())
        # A diameter of the pie
        diam = int(canvas_size * self.ratio)

        # Coordinates of the pie
        # Left upper corner
        xy0 = (canvas_size - diam) / 2 + self.outline_thickness
        # Right lower corner
        xy1 = (canvas_size + diam) / 2 - self.outline_thickness

        # Resize wedges of the pie
        # self.outline_thickness - leave some place between canvas border and
        # the pie to display thick outline
        for wedge in self.Wedges:
            self.canvas.coords(wedge, xy0, xy0, xy1, xy1)

    # Display the canvas with the color pie
    def show(self):
        # TODO: what are option for place? could we use any of them?
        # Make the canvas visible and centered
        self.canvas.place(relx=0.5, rely=0.5, anchor='center')
        # Make the wedge visible
        for wedge in self.Wedges:
            self.canvas.itemconfigure(wedge, state=tk.NORMAL)

    # Hide the canvas with the color pie
    def hide(self):
        # TODO: what are option for place? could we use any of them?
        self.canvas.place_forget()                  # Make the canvas invisible
        # Make the wedges invisible
        for wedge in self.Wedges:
            self.canvas.itemconfigure(wedge, state=tk.HIDDEN)

    def unlock_wedge(self, wedge_id, color):
        # FIXME: color?:
        self.canvas.itemconfigure(wedge_id, fill=color, outline=color)


# Options window
class OptionsWindow:
    def __init__(self, master, parent):
        # ======================================
        # Initialize instance variables
        # ======================================
        # Title of the window
        self.OptionsWindowTitle = AppTitle + " - Nustatymai"
        # Label of the tab where color unlocking codes are set
        self.Tab1Label = "Spalvų atrakinimo kodai"
        # Label of the frame with unlocking codes
        self.Frame1Label = " Čia surašykite spalvų atrakinimo kodus: "
        # An array of labels for entries of color unlock codes
        self.ColorUnlockFieldLabels = []
        self.SaveButtonLabel = "Išsaugoti"      # Label of the Save button
        self.CancelButtonLabel = "Uždaryti"     # Label of the Cancel button
        # An array of variables associated with entries of color unlock codes
        self.ColorUnlockCodes = []
        # An array of Textbox Entry widgets for color unlock code
        self.ColorUnlockCodeEntries = []

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
        # ~ Tab Control introduced here -------------------------------------

        # We are creating a container frame to hold all other widgets
        self.Frame1 = ttk.LabelFrame(self.tab1, text=self.Frame1Label)
        self.Frame1.grid(column=0, row=0, padx=16, pady=16)

        for clrs in self.parent.Colors:
            index = self.parent.Colors.index(clrs)
            # Populate the array of labels for fields of color unlock codes
            self.ColorUnlockFieldLabels.append(
                self.parent.FieldLabelColorNames[clrs] + " spalvos kodas: "
                )
            # Create the array of variables associated with entries of color
            # unlock codes
            self.ColorUnlockCodes.append(tk.IntVar())
            # Populate the array with current unlock code values from the main
            # window
            self.ColorUnlockCodes[index].set(
                self.parent.Configuration[
                    self.parent.ColorUnlockCodesSectionName
                    ][clrs]
                )
            # Set a label for a fields of color unlock code
            ttk.Label(self.Frame1,
                      text=self.ColorUnlockFieldLabels[index]).grid(
                            column=0, row=index, padx=4, pady=4, sticky='E'
                            )
            # Add a Textbox Entry widget for color unlock code
            # TODO: Somehow ensure that entered value is either one- or
            #       two-digit number.
            #       See https://web.archive.org/web/20190524022302/...
            #       ...http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/...
            #       ...entry-validation.html
            self.ColorUnlockCodeEntries.append(
                ttk.Entry(self.Frame1, width=12,
                          textvariable=self.ColorUnlockCodes[index])
                )
            self.ColorUnlockCodeEntries[index].grid(column=1, row=index,
                                                    padx=4, pady=4, sticky='W')

        # Create Save button
        # Adding a Button
        self.SaveButton = ttk.Button(self.master, text=self.SaveButtonLabel,
                                     command=self.save_options)
        self.SaveButton.pack(expand=1, fill='x', side='left')

        # Create Cancel button
        # Adding a Button
        self.CancelButton = ttk.Button(self.master,
                                       text=self.CancelButtonLabel,
                                       command=self._quit)
        # self.CancelButton.grid(column=2, row=1)
        self.CancelButton.pack(expand=1, fill='x', side='right')

    # Save options to a configuration file
    def save_options(self):
        # Update the variables keeping the configuration dictionary
        # Update color unlock codes to the values in the corresponding entries
        for clrs in self.parent.Colors:
            index = self.parent.Colors.index(clrs)
            self.parent.Config.set(self.parent.ColorUnlockCodesSectionName,
                                   clrs,
                                   str(self.ColorUnlockCodes[index].get())
                                   )
            self.parent.Configuration[
                self.parent.ColorUnlockCodesSectionName
                ][clrs] = self.ColorUnlockCodes[index].get()
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
wedges, texts = ax.pie(wedgeSizes, radius=1, colors=grays, labels=wedgeLabels,
                       labeldistance=lblDistance,
                       wedgeprops=dict(width=1-size),
                       textprops=dict(va='center', ha='center')
                       )
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
