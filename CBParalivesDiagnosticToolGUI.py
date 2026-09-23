import tkinter as tk
from tkinter import ttk
import Dgnt
import threading

def resize_tree(event):
    tree = event.widget
    tree.after(1, lambda: tree.config(height=1 if not tree.item(tree.get_children()[0], "open") else len(tree.get_children(tree.get_children()[0])) + 1))

def scroll_canvas(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

# Create the main window
root = tk.Tk()
root.title("Unofficial Paralives Diagnostic Tool")
root.geometry("600x400")
root.bind_all("<MouseWheel>", scroll_canvas)

# Tree view style
style = ttk.Style()
#style.layout("Diagnostic.Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
style.configure("Diagnostic.Treeview", rowheight=20, borderwidth=0, relief="flat", background=root.cget("bg"), fieldbackground=root.cget("bg"), font=("Arial", 10), padding=0)
style.map("Diagnostic.Treeview", background=[("selected", root.cget("bg"))], foreground=[("selected", "black")])

# Scrollbar
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
scrollable_frame.columnconfigure(0, weight=1)
frame_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.bind("<Configure>", lambda e: canvas.itemconfig(frame_window, width=e.width))
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

UIElements = [
    (ttk.Label(scrollable_frame, text=""), 10),
    (title := ttk.Label(scrollable_frame,text="Paralives Diagnostic Tool",font=("Arial", 20, "bold")),20),
    (description := ttk.Label(scrollable_frame,text="Run a diagnostic scan of your Paralives game files."),5),
    (run_button := ttk.Button(scrollable_frame,text="Run Diagnostics"),5),
]

UITrees1 = [
    gamepaths_tree := [ttk.Treeview(scrollable_frame, height=1,show="tree",style="Diagnostic.Treeview"),"Game Paths",Dgnt.check_paths,None],
]

UITrees2 = [
    savefiles_label := [ttk.Treeview(scrollable_frame, height=1,show="tree",style="Diagnostic.Treeview"),"Save Files",Dgnt.check_save_files,None],
    localmods_label := [ttk.Treeview(scrollable_frame, height=1,show="tree",style="Diagnostic.Treeview"),"Local Mods",Dgnt.check_local_mods,None],
    workshopmods_label := [ttk.Treeview(scrollable_frame, height=1,show="tree",style="Diagnostic.Treeview"),"Workshop Mods",Dgnt.check_workshop_mods,None],
    complexmodproblems_label := [ttk.Treeview(scrollable_frame, height=1,show="tree",style="Diagnostic.Treeview"),"Complex Mod Problems",Dgnt.check_complex_mod_problems,None],
    playerlog_label := [ttk.Treeview(scrollable_frame, height=1,show="tree",style="Diagnostic.Treeview"),"Player.log",Dgnt.check_player_log,None],
]

UIButtons = [
    (ttk.Label(scrollable_frame,text=""),10),
    (savefolder_button := ttk.Button(scrollable_frame,text="Open save folder", command=Dgnt.open_savefolder),1),
    (localmods_button := ttk.Button(scrollable_frame, text="Open local mods folder", command=Dgnt.open_localmods), 1),
    (workshopmods_button := ttk.Button(scrollable_frame,text="Open workshop mods folder", command=Dgnt.open_workshopmods),1),
    (playerlog_button := ttk.Button(scrollable_frame,text="Open Player.log", command=Dgnt.open_player_log),1),
    (reporttxt_button := ttk.Button(scrollable_frame,text="Open Report"),1),
    (ttk.Label(scrollable_frame, text=""), 40),
]

rowcounter = 0

for element in UIElements:
    element[0].grid(row=rowcounter, column=0,pady=element[1]) # type: ignore
    rowcounter += 1

for element in UITrees1:
    element[0].grid(row=rowcounter,column=0,padx=20,pady=5,sticky="ew") # type: ignore
    element[0].bind("<Button-1>", resize_tree) # type: ignore
    element[3] = element[0].insert("","end",text=f"{element[1]}: Unchecked") # type: ignore
    rowcounter += 1

for element in UITrees2:
    element[0].grid(row=rowcounter,column=0,padx=20,pady=5,sticky="ew") # type: ignore
    element[0].bind("<Button-1>", resize_tree) # type: ignore
    element[3] = element[0].insert("","end",text=f"{element[1]}: Unchecked") # type: ignore
    rowcounter += 1

for element in UIButtons:
    element[0].grid(row=rowcounter, column=0,pady=element[1])  # type: ignore
    rowcounter += 1

# ------------------------------------------------
# ------------------------------------------------
# ------------------------------------------------

# Run functions to check game files and return findings
def run_diagnostics():

    # Disable the start button
    run_button.config(state="disabled")

    Dgnt.newlogfile()
    Dgnt.pastelogheader()

    # Set file path tree to default
    gamepaths_tree[0].delete(*gamepaths_tree[0].get_children(gamepaths_tree[3])) # type: ignore
    gamepaths_tree[0].item(gamepaths_tree[3],text=f"{gamepaths_tree[1]}: Checking...",open=True) # type: ignore

    # Check file paths are valid before proceeding
    pathresults, data = Dgnt.check_paths()
    update_tree(gamepaths_tree, data)

    if pathresults:
        gamepaths_tree[0].item(gamepaths_tree[3], text=f"{gamepaths_tree[1]}: Valid", open=True)  # type: ignore

        # start background thread
        threading.Thread(target=run_diagnostics_thread,daemon=True).start()

        # Set all result trees to default
        for element in UITrees2:
            element[0].delete(*element[0].get_children(element[3]))  # type: ignore
            element[0].item(element[3], text=f"{element[1]}: Checking...", open=True)  # type: ignore

    else:
        gamepaths_tree[0].item(gamepaths_tree[3], text=f"{gamepaths_tree[1]}: Invalid Paths", open=True)  # type: ignore

run_button.config(command=run_diagnostics)

# ------------------------------------------------
# ------------------------------------------------
# ------------------------------------------------

def update_tree(tree, results):
    tree_widget = tree[0]
    parent_id = tree[3]
    tree[0].delete(*tree[0].get_children(tree[3]))  # type: ignore
    tree[0].item(tree[3], text=f"{tree[1]}: Complete", open=True)  # type: ignore

    for result in results:

        if not result[0]:
            tree_widget.insert(parent_id, "end", text=f"             {result[1]}")
        elif not result[1]:
            tree_widget.insert(parent_id, "end", text=f"{result[0]}")
        else:
            tree_widget.insert(parent_id, "end", text=f"{result[0]}: {result[1]}")

    tree_widget.config(height=len(results) + 1)

def run_diagnostics_thread():
    try:
        for tree in UITrees2:
            results = tree[2]()
            root.after(0, update_tree, tree, results)
    finally:
        root.after(0, diagnostics_finished)  # type: ignore

def diagnostics_finished():
    run_button.config(state="normal")

# Start the GUI
root.mainloop()