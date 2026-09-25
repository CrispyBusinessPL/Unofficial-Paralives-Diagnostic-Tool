
# Import files
import os
import subprocess
import sys
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import threading
import ctypes

# Project files
import Dgnt
import Localization

# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

# Debug mode
DEBUGMODE = False

# Paths
EXECUTION_FOLDER = Path.cwd()
TRANSLATION_FOLDER = EXECUTION_FOLDER / "Translations"
CONFIGURATION_FILE = EXECUTION_FOLDER / "Config.txt"

# CONSTANTS
SCREEN_SIZE = "600x400"
COLORS = {
    "dark": {"background_color_dark": "#191A1C", "background_color_light": "#34373B", "foreground_color": "#303030", "text_color": "#dfe1e5", "button_color": "#1b2d30", "edge_color": "#000000", "color_bright": "#888888", "selection_highlight_color": "#404347", "success": "#11A800","warning": "#FFA50A","fail": "#FF6B6B", "url_color": "#66b2ff", "selected_item_color": "#FFFFFF"},
    "light": {"background_color_dark": "#d6d6d6", "background_color_light": "#E6E6E6", "foreground_color": "#303030", "text_color": "#303030", "button_color": "#c4c4c4", "edge_color": "#000000", "color_bright": "#888888", "selection_highlight_color": "#b5b5b5", "success": "#11A800","warning": "#FFA50A","fail": "#FF4747", "url_color": "#0000FF", "selected_item_color": "#202020"}
}

# STATUS
CODE_IS_RUNNING = False
DARK_MODE = False

# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

# Set timestamp code
Dgnt.updatetimestamp()

# Import config file
CONFIGURATION = Dgnt.importconfig(CONFIGURATION_FILE)
LANGUAGE = CONFIGURATION.get("LANG")
print(f"Starting Language: {LANGUAGE}")

# All translations
Translations = Localization.importlanguage(TRANSLATION_FOLDER)

# Language
Lang = Localization.load_language(TRANSLATION_FOLDER, LANGUAGE)
Dgnt.Lang = Lang

# Set files paths
Dgnt.setfilepaths(CONFIGURATION,EXECUTION_FOLDER)

# Set dark mode
DARK_MODE = True if CONFIGURATION.get("Dark_Mode") in ("true", "True", True, "truee", "Truee") else False
c = COLORS["dark" if DARK_MODE else "light"]

# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

def change_language(event):
    newlanguage = LanguageVar.get().lower()
    if newlanguage != LANGUAGE.lower() :
        print(f"Language will be changed from {LANGUAGE} to {newlanguage}")
        Dgnt.updateconfig(CONFIGURATION_FILE, "LANG", newlanguage)
        restart()
    else:
        print(f"Language could NOT be changed from {LANGUAGE} to {newlanguage}")

def restart():
    if getattr(sys, "frozen", False):
        subprocess.Popen([str(EXECUTION_FOLDER / "CBParalivesDiagnosticToolGUI.exe")])
        root.destroy()
    else:
        geometry = root.geometry()
        subprocess.Popen([sys.executable, os.path.abspath(sys.argv[0]), geometry], creationflags=subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP)
        root.destroy()

# Enable scroll wheel
def scroll_canvas(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

# Create the main window
root = tk.Tk()
root.withdraw()

# Change the window attribute color
root.update_idletasks()
hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
value = ctypes.c_int(1)
ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(value), ctypes.sizeof(value))

# Bind window attributes
root.title(Lang["TITLE"])

if len(sys.argv) > 1:
    root.geometry(sys.argv[1])
else:
    root.geometry(SCREEN_SIZE)
root.bind_all("<MouseWheel>", scroll_canvas)
root.configure(bg=c["background_color_dark"])

# Icons
check_icon = tk.PhotoImage(file="images/greencheckmark.png")
warning_icon = tk.PhotoImage(file="images/warning.png")
error_icon = tk.PhotoImage(file="images/error.png")

# Style
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", rowheight=25)

# -----------------------------------------------------------------------------------------
# -----------------------------------------DARK MODE---------------------------------------
# -----------------------------------------------------------------------------------------

# Toggle dark mode
def toggle_dark_mode(firsttime = False):
    global dark_mode_button, DARK_MODE, c
    if not firsttime:
        DARK_MODE = not DARK_MODE
        c = COLORS["dark" if DARK_MODE else "light"]
        Dgnt.updateconfig(CONFIGURATION_FILE,"Dark_Mode", DARK_MODE)

    # Set button text for mode
    dark_mode_button.config(text=Lang["BUTTON3a"] if DARK_MODE else Lang["BUTTON3b"])

    for tree in (UITrees1+UITrees2):
        tree[0].tag_configure("link_color", foreground=c["url_color"])  # type: ignore
        tree[0].tag_configure("fail_color", foreground=c["fail"])  # type: ignore

    # Style colors
    canvas.configure(bg=c["background_color_dark"])
    scrollbar.configure(bg=c["background_color_dark"])
    root.configure(bg=c["background_color_dark"])
    style.configure(".", background=c["background_color_dark"], foreground=c["foreground_color"], bordercolor=c["background_color_light"]) # default color
    style.configure("TLabel", background=c["background_color_dark"], foreground=c["text_color"]) # text color

    # Buttons
    style.configure("TButton", background=c["background_color_light"], foreground=c["text_color"], bordercolor=c["edge_color"], font=(Lang["FONT"], Lang["FONTSIZE"])) # button color
    style.map("TButton", background=[("active", c["color_bright"])])  # button highlighted color

    # Tree view
    style.configure("Diagnostic.Treeview", font=(Lang["FONT"], Lang["FONTSIZE"]), background=c["background_color_light"], fieldbackground=c["background_color_light"], foreground=c["text_color"], bordercolor=c["edge_color"],lightcolor=c["background_color_light"], darkcolor="black") # tree view color
    style.map("Diagnostic.Treeview", background=[("selected", c["selection_highlight_color"])],foreground=[("selected", c["selected_item_color"])])  # tree view highlighted color

    # Combo Box
    style.configure("TCombobox", padding=(1, 6),justify="center",fieldbackground=c["background_color_dark"], background=c["background_color_light"], foreground=c["text_color"],bordercolor=c["edge_color"])
    style.map("TCombobox", fieldbackground=[("readonly", c["background_color_light"])], foreground=[("readonly", c["text_color"])])
    popdown = language_dropdown.tk.call("ttk::combobox::PopdownWindow", str(language_dropdown))
    language_dropdown.tk.call(f"{popdown}.f.l", "configure", "-background", c["background_color_light"], "-foreground", c["text_color"])

# -----------------------------------------------------------------------------------------
# ------------------------------------CUSTOM SCROLL BAR------------------------------------
# -----------------------------------------------------------------------------------------

canvas = tk.Canvas(root, highlightthickness=0, bg=c["foreground_color"])
scrollable_frame = ttk.Frame(canvas)
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
scrollable_frame.columnconfigure(0, weight=1)
frame_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.bind("<Configure>", lambda e: (canvas.itemconfig(frame_window, width=e.width), canvas.configure(scrollregion=canvas.bbox("all"))))
barwidth = 20
baredge = 1
scrollbar = tk.Canvas(root, width=14, bg=c["background_color_light"], highlightthickness=0)
thumb = scrollbar.create_rectangle(baredge, 0, barwidth-baredge, 100, fill=c["color_bright"], outline="")
def update_scrollbar(first, last):
    height = scrollbar.winfo_height()
    scrollbar.coords(thumb, baredge, float(first) * height, barwidth-baredge, float(last) * height)
canvas.configure(yscrollcommand=update_scrollbar)
canvas.after(100, lambda: canvas.yview_moveto(0))
canvas.bind("<Configure>", lambda e: (canvas.itemconfig(frame_window, width=e.width), canvas.configure(scrollregion=canvas.bbox("all"))))
drag_offset = 0
def scrollbar_click(event):
    global drag_offset
    coords = scrollbar.coords(thumb)
    drag_offset = event.y - coords[1]
def scrollbar_drag(event):
    height = scrollbar.winfo_height()
    thumb_height = scrollbar.coords(thumb)[3] - scrollbar.coords(thumb)[1]
    y = event.y - drag_offset
    y = max(0, min(y, height - thumb_height))
    canvas.yview_moveto(y / height)
scrollbar.bind("<Button-1>", scrollbar_click)
scrollbar.bind("<B1-Motion>", scrollbar_drag)
scrollbar.bind("<Enter>", lambda e: scrollbar.itemconfig(thumb, fill="#777777"))
scrollbar.bind("<Leave>", lambda e: scrollbar.itemconfig(thumb, fill="#999999"))
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# -----------------------------------------------------------------------------------------
# ------------------------------------CLICKABLE LINKS--------------------------------------
# -----------------------------------------------------------------------------------------

# Makes tree view links clickable
def go_to_link(event):
    global style
    global FONT
    tree = event.widget
    item = tree.identify_row(event.y)
    path = tree.item(item, "values")[0]
    if Path(path).exists():
        os.startfile(path)
    #tree.after_idle(lambda: tree.selection_remove(item))

# -----------------------------------------------------------------------------------------
# ------------------------------------BUILD UI ELEMENTS------------------------------------
# -----------------------------------------------------------------------------------------


# Title, Subtitle, and Description
UITitle = [
    (ttk.Label(scrollable_frame, text=""), 10),
    (title := ttk.Label(scrollable_frame,text=Lang["TITLE"],font=(Lang["FONT"], 20, "bold")),5),
    (subtitle := ttk.Label(scrollable_frame,text=Lang["SUBTITLE"]),5),
    (ttk.Label(scrollable_frame,text=""),5),
    (description := ttk.Label(scrollable_frame,text=Lang["DESCRIPTION"]),5),
    (ttk.Label(scrollable_frame,text=""),5),
(run_button := ttk.Button(scrollable_frame,text=Lang["BUTTON1"]),5),
]

# Main buttons and dropdown
LanguageVar = tk.StringVar(value=LANGUAGE.title())
button_frame1 = ttk.Frame(scrollable_frame)
UIButtons1 = [
    (reporttxt_button := ttk.Button(button_frame1,text=Lang["BUTTON2"], command=Dgnt.open_log),1),
    (dark_mode_button := ttk.Button(button_frame1, text=Lang["BUTTON3a"], command=toggle_dark_mode),5),
    (language_dropdown := ttk.Combobox(button_frame1, textvariable=LanguageVar, values=[x.title() for x in Translations.keys()], state="readonly", font=(Lang["FONT"], Lang["FONTSIZE"]), width=10), 5),
]
language_dropdown.configure(justify="center")
language_dropdown.bind("<MouseWheel>", lambda e: "break")
language_dropdown.bind("<FocusIn>", lambda e: language_dropdown.selection_clear())
language_dropdown.bind("<<ComboboxSelected>>", change_language) # type: ignore
language_dropdown.bind("<<ComboboxSelected>>", lambda e: language_dropdown.selection_clear(), add="+")
reporttxt_button.config(state="disabled")

# Tree views
UITrees1 = [
    gamepaths_tree := [ttk.Treeview(scrollable_frame, height=1,show="tree",style="Diagnostic.Treeview"),Lang["LABEL1"],Dgnt.check_paths,None],
]

# Tree views
UITrees2 = [
    savefiles_label := [ttk.Treeview(scrollable_frame, height=1,show="tree",style="Diagnostic.Treeview"),Lang["LABEL2"],Dgnt.check_save_files,None],
    localmods_label := [ttk.Treeview(scrollable_frame, height=1,show="tree",style="Diagnostic.Treeview"),Lang["LABEL2"],Dgnt.check_local_mods,None],
    workshopmods_label := [ttk.Treeview(scrollable_frame, height=1,show="tree",style="Diagnostic.Treeview"),Lang["LABEL4"],Dgnt.check_workshop_mods,None],
    complexmodproblems_label := [ttk.Treeview(scrollable_frame, height=1,show="tree",style="Diagnostic.Treeview"),Lang["LABEL5"],Dgnt.check_complex_mod_problems,None],
    playerlog_label := [ttk.Treeview(scrollable_frame, height=1,show="tree",style="Diagnostic.Treeview"),Lang["LABEL6"],Dgnt.check_player_log,None],
]

# Bottom shortcut buttons
button_frame2 = ttk.Frame(scrollable_frame)
UIButtons2 = [
    (ttk.Label(button_frame2,text=""),10),
    (savefolder_button := ttk.Button(button_frame2,text=Lang["BUTTON4"], command=Dgnt.open_savefolder),1),
    (localmods_button := ttk.Button(button_frame2, text=Lang["BUTTON5"], command=Dgnt.open_localmods), 1),
    (workshopmods_button := ttk.Button(button_frame2,text=Lang["BUTTON6"], command=Dgnt.open_workshopmods),1),
    (playerlog_button := ttk.Button(button_frame2,text=Lang["BUTTON7"], command=Dgnt.open_player_log),1),
    (ttk.Label(button_frame2, text=""), 40),
]

# Run the dark mode without toggling to ensure all configurations are correct on startup
toggle_dark_mode(True)

# -----------------------------------------------------------------------------------------
# ------------------------------------POSITION UI ELEMENTS---------------------------------
# -----------------------------------------------------------------------------------------

rowcounter = 0
columncounter = 0

# Title and description
for element in UITitle:
    element[0].grid(row=rowcounter, column=0,pady=element[1]) # type: ignore
    rowcounter += 1

# Top buttons
button_frame1.grid(row=rowcounter, column=0, pady=5)
rowcounter += 1
for element in UIButtons1:
    element[0].pack(side="left", padx=5)

# Add visual divider
ttk.Label(scrollable_frame, text="").grid(row=rowcounter, column=0,pady=0)
rowcounter += 1

# Event for expanding tree views
def resize_tree(event):
    tree = event.widget
    tree.after(1, lambda: tree.config(height=1 if not tree.item(tree.get_children()[0], "open") else len(tree.get_children(tree.get_children()[0])) + 1))

# Tree view for resultss
for element in (UITrees1+UITrees2):
    element[0].grid(row=rowcounter,column=0,padx=20,pady=1,sticky="ew") # type: ignore
    element[0].bind("<Button-1>", resize_tree) # type: ignore
    element[3] = element[0].insert("","end",text=f"{element[1]}: {Lang["TXT_UNCHECKED"]}") # type: ignore
    rowcounter += 1

# Add visual divider
ttk.Label(scrollable_frame, text="").grid(row=rowcounter, column=0,pady=0)
rowcounter += 1

# Bottom buttons
button_frame2.grid(row=rowcounter, column=0, pady=5)
rowcounter += 1
for element in UIButtons2:
    element[0].pack(side="left", padx=5)

# Add visual divider
ttk.Label(scrollable_frame, text="").grid(row=rowcounter, column=0,pady=40)
rowcounter += 1

# -----------------------------------------------------------------------------------------
# -----------------------------------CLEAR SELECTIONS--------------------------------------
# -----------------------------------------------------------------------------------------

# When making a new selection in the tree view, remove old selections
def clear_other_selections(event):
    clicked_tree = event.widget

    for tree in (UITrees1+UITrees2):
        if tree[0] != clicked_tree:
            tree[0].selection_remove(tree[0].selection()) # type: ignore

# Bind event to view tree
for element in (UITrees1+UITrees2):
    element[0].bind("<Button-1>", clear_other_selections, add="+") # type: ignore

# -----------------------------------------------------------------------------------------
# -----------------------------------CHECK FILES-------------------------------------------
# -----------------------------------------------------------------------------------------

# Run functions to check game files and return findings
def run_diagnostics():
    global CODE_IS_RUNNING

    # Disable the start button
    CODE_IS_RUNNING = True
    run_button.config(state="disabled")
    language_dropdown.config(state="disabled")

    # Start new log file and set header
    Dgnt.updatetimestamp()
    Dgnt.pastelogheader()

    # Set file path tree to default
    gamepaths_tree[0].delete(*gamepaths_tree[0].get_children(gamepaths_tree[3])) # type: ignore
    gamepaths_tree[0].item(gamepaths_tree[3], text=f"{gamepaths_tree[1]}: {Lang["TXT_CHECKING"]}...", open=True) # type: ignore

    # Check file paths are valid before proceeding
    pathresults, data = Dgnt.check_paths()
    update_tree(gamepaths_tree, data)

    # If file paths are valid proceed to gathering data
    if pathresults:
        gamepaths_tree[0].item(gamepaths_tree[3], text=f"{gamepaths_tree[1]}: {Lang["TXT_VALID"]}", open=True)  # type: ignore

        # Start background thread and begin collecting data
        threading.Thread(target=run_diagnostics_thread,daemon=True).start()

        # Empty all trees and set tree title to checking
        for element in UITrees2:
            element[0].delete(*element[0].get_children(element[3]))  # type: ignore
            element[0].item(element[3], text=f"{element[1]}: {Lang["TXT_CHECKING"]}...", open=True)  # type: ignore

    # If file paths are not valid then do not proceed
    else:
        gamepaths_tree[0].item(gamepaths_tree[3], text=f"{gamepaths_tree[1]}: {Lang["TXT_INVALID"]}", open=True)  # type: ignore
        for element in UITrees2:
            element[0].delete(*element[0].get_children(element[3]))  # type: ignore
            element[0].item(element[3], text=f"{element[1]}: {Lang["TXT_MISSINGCRITICALFILE"]}", open=True)  # type: ignore
        run_button.config(state="normal")
        reporttxt_button.config(state="normal")
        language_dropdown.config(state="normal")

        CODE_IS_RUNNING = False

run_button.config(command=run_diagnostics)

# -----------------------------------------------------------------------------------------
# ---------------------------PUT RESULTS IN TREE VIEW--------------------------------------
# -----------------------------------------------------------------------------------------

# Populate tree views
def update_tree(tree, results):

    tree_widget = tree[0]
    parent_id = tree[3]

    # Empty the tree and set tree title
    tree_widget.delete(*tree_widget.get_children(parent_id))
    tree_widget.item(parent_id, text=f"{tree[1]}: {Lang["TXT_COMPLETE"]}", open=True)

    # Setup color tags
    tree_widget.tag_configure("success_color", foreground=c["success"])
    tree_widget.tag_configure("warning_color", foreground=c["warning"])
    tree_widget.tag_configure("fail_color", foreground=c["fail"])
    tree_widget.tag_configure("link_color", foreground=c["url_color"], font=(Lang["FONT"],Lang["FONTSIZE"], "underline"))
    tree_widget.tag_bind("hyperlink", "<Button-1>", go_to_link)

    for result in results:
        if not result[0]:
            tree_widget.insert(parent_id, "end", text=f"          {result[1]}")
        elif not result[1]:
            tree_widget.insert(parent_id, "end", text=f"       {result[0]}")
        elif result[0] == "[OK]":
            tree_widget.insert(parent_id, "end", text=f" {result[1]}", image=check_icon)
        elif result[0] == "[WARNING]":
            tree_widget.insert(parent_id, "end", text=f" {result[1]}", image=warning_icon, tags=("fail_color",))
        elif result[0] == "[ERROR]":
            tree_widget.insert(parent_id, "end", text=f" {result[1]}", image=error_icon, tags=("fail_color",))
        elif result[0] == "[PATHOK]":
            tree_widget.insert(parent_id, "end", text=f" {result[1]}", image=check_icon)
            tree_widget.insert(parent_id, "end", text=f"{result[2]}", values=(result[2],), tags=("hyperlink", "link_color"))
        elif result[0] == "[PATHFAIL]":
            tree_widget.insert(parent_id, "end", text=f" {result[1]} {result[2]}", image=error_icon, tags=("fail_color",))
        else:
            tree_widget.insert(parent_id, "end", text=f"{result[0]}: {result[1]}")

    tree_widget.config(height=len(tree_widget.get_children(parent_id)) + 1)

# -----------------------------------------------------------------------------------------
# -------------------BACKGROUND THREAD WHICH COLLECTS USER GAME DATA-----------------------
# -----------------------------------------------------------------------------------------

# Background thread to process data
def run_diagnostics_thread():
    try:
        for tree in UITrees2:
            stored_function = tree[2]()
            results = stored_function
            root.after(0, update_tree, tree, results)
    finally:
        root.after(0, diagnostics_finished)  # type: ignore

# Background thread finished
def diagnostics_finished():
    global CODE_IS_RUNNING
    run_button.config(state="normal")
    reporttxt_button.config(state="normal")
    language_dropdown.config(state="normal")
    CODE_IS_RUNNING = False

root.deiconify()

# Start the GUI
root.mainloop()















