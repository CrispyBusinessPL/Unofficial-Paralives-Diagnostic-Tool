# for opening the log file
import os

# for reading game files
from pathlib import Path

# for writing log file if program is closed early
import atexit

# for timestamping logs
from datetime import datetime

# for reading config file
import tomllib

DEBUGMODE = False
EXECUTION_FOLDER = Path.cwd()
OUTPUTPATH = EXECUTION_FOLDER
textformatting = [s1 := " "*1,s2 := " "*2,s3 := " "*3,s4 := " "*4,s5 := " "*5,s6 := " "*6]
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
if DEBUGMODE:
    OUTPUTFILE = OUTPUTPATH / "CBDiagnosticLog.txt"
else:
    OUTPUTFILE = OUTPUTPATH / f"CBDiagnosticLog_{timestamp}.txt"
OutputText = ""
Report = ""

# add to queue to be written to the log file
def log(text=""):
    global OutputText
    OutputText += str(text) + "\n"
    print(text)

# add to queue but do not print
def logonly(text: str=""):
    global OutputText
    OutputText += str(text) + "\n"

# write the queued logs to the log file
def appendlogtofile():
    global OutputText
    try:
        with open(OUTPUTFILE, "a", encoding="utf-8") as file:
            file.write(OutputText)
            OutputText = ""
    except PermissionError:
        print(f"Console: Could not update log file because the file is locked.\n")
atexit.register(appendlogtofile)

# for resetting log file in debugmode
def clearlogfile():
    try:
        with open(OUTPUTFILE, "w", encoding="utf-8") as file:
            pass
    except PermissionError:
        print(f"Console: Could not clear log file because the file is locked.\n")

# when testing this program
if DEBUGMODE:
    clearlogfile()

# for storing text during formatting
def report(text: str=""):
    global Report
    Report += str(text) + "\n"

def logreport():
    global Report
    global OutputText
    OutputText += f"{Report}"
    print(Report, end="")
    Report = ""

# format chapter titles in log
def printchapter(text: str="-"*38):
    length = len(text) + 6
    log("\n"+"-"*length)
    log(f"---{text}---")
    log("-"*length+"\n")
    appendlogtofile()

# remove username from paths
USERNAME = Path.home().name
def removeusername(text: str):
    return text.replace(USERNAME, "USER")

# shorten file paths to remove username
def shortenpath(x: Path) -> str:
    parts = x.parts
    if USERNAME in parts:
        index = parts.index(USERNAME)
        if index + 1 < len(parts):
            return rf"..\{str(Path(*parts[index + 1:]))}"
    return str(x)

# read .meta file and store as a dictionary
def readconfig(x: Path) -> dict:
    y = {}
    with open(x, "r", encoding="utf-8") as file:
        for l in file:
            if ":" in l:
                key, value = l.rstrip("\n").split(":", 1)
                y[key] = value
    return y

# Check for config file
config_path = EXECUTION_FOLDER / "config.toml"
if config_path.exists():
    if DEBUGMODE:
        log(f"{s2}Found config file at {shortenpath(config_path)}")
        log()
    with open(config_path, "rb") as f:
        config = tomllib.load(f)
else:
    if DEBUGMODE:
        log(f"{s2}Using default paths: No config file at {shortenpath(config_path)}")
        log()
    config = {}

# array of paths to critical files
array_FilePaths = [

    # Root Folder Paths
    PATH_WORKSHOPMODSFOLDER := (Path(config.get("Workshop_Mods_Folder") or r"C:\Program Files (x86)\Steam\steamapps\workshop\content\1118520"),"Workshop Mods Folder"),
    PATH_LOCALMODSFOLDER:= (Path(config.get("Local_Mods_Folder") or Path.home() / "AppData" / "LocalLow" / "Paralives" / "Paralives"),"Local Mods Folder"),

    # Sub Folders Paths
    PATH_SAVEFOLDER := (PATH_LOCALMODSFOLDER[0] / "MySavedGames.mod", "Save Folder"),
    PATH_PREMADEHOUSEHOLDS := (PATH_LOCALMODSFOLDER[0] / "MyPremadeHouseholds.mod","Premade households"),
    PATH_PREMADELOTS := (PATH_LOCALMODSFOLDER[0] / "MyPremadeLot.mod", "Premade lots"),
    PATH_PREMADEOUTFITS := (PATH_LOCALMODSFOLDER[0] / "MyPremadeOutfits.mod", "Premade outfits"),
    PATH_LOCALDOTMOD := (PATH_LOCALMODSFOLDER[0] / "Local.mod", "Local.mod"),
    PATH_ZERODOTMOD := (PATH_LOCALMODSFOLDER[0] / "0.mod", "0.mod"),

    # File paths
    PATH_PLAYERLOG := (PATH_LOCALMODSFOLDER[0] / "Player.log", "Player Log"),
    PATH_PREVPLAYERLOG := (PATH_LOCALMODSFOLDER[0] / "Player-prev.log", "Prev-Player log"),

    # Log File
    (OUTPUTPATH,"Log folder")
]

def newlogfile():
    global OUTPUTFILE
    global timestamp

    if DEBUGMODE:
        OUTPUTFILE = OUTPUTPATH / "CBDiagnosticLog.txt"
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        OUTPUTFILE = OUTPUTPATH / f"CBDiagnosticLog_{timestamp}.txt"

def pastelogheader():
    log(timestamp)
    log("\n\n")
    log("--THE UNOFFICIAL PARALIVES DIAGNOSTIC TOOL by Crispy Business--")
    log()
    log(f"{s2}This program is in no way associated with Paralives Studios")
    printchapter("Introduction and how to read the log file")
    log(f"""{s2}OK is all good. Everything else is bad.

    {s2}Fail - this program encountered an error which prevented further testing.
    {s2}Error - something was dectected which may be causing a problem(s).
    {s2}Critical Error - something was detected which is almost certainly causing problems.
    {s2}Missing - a file is missing that is expected to be there. This does not necessarily mean there is a problem.
    {s2}Duplicate Files - multiple versions of a file when there should only be one.
""")

# ------------------------------------------------
# ------------------------------------------------
# ------------------------------------------------

def check_paths():
    # test file paths
    Test_FilePathsFailed = False

    results = []

    # check if each path in the array of paths exists
    for path, description in array_FilePaths:

        # if the path exists, log positive result. Shorten path name only in the log.
        if path.exists():

            # check is mod is enabled
            metapath = Path(f"{path}/{path.name}.meta")
            if Path(metapath).exists():
                config = readconfig(metapath)
                if "Enabled" not in config:
                    enabled = "[MISSING]"
                elif config["Enabled"]:
                    enabled = "[Enabled]"
                else:
                    enabled = "[Disabled]"
            else:
                enabled = ""

            results.append(("[OK]",f"{description} {enabled} {shortenpath(path)}"))
            logonly(f"{s2}[OK] {description.ljust(22, ".")}{enabled.ljust(9, ".")}..{shortenpath(path)}")
            print(f"{s2}[OK] {description.ljust(22, ".")}{enabled.ljust(9, ".")}..{path}")

        # if the path does not exist, log negative result. Shorten path name only in the log.
        else:
            Test_FilePathsFailed = True
            results.append(("[FAIL]", f"{description} {enabled} {shortenpath(path)}"))
            logonly(f"{s2}[FAIL] {description.ljust(22, ".")}..{shortenpath(path)}")
            print(f"{s2}[FAIL] {description.ljust(22, ".")}..{path}")

    # check test results
    # any path failures will cause errors later so the program must be aborted
    if Test_FilePathsFailed:
        log()
        log("Critical Error: Invalid file path detected. Repair folder or override the file path using the included configuration file. Press Enter to exit...")
        return False, results

    return True, results

# ------------------------------------------------
# ------------------------------------------------
# ------------------------------------------------

def check_save_files():

    # TODO: CHECK IF SAVE IS AN AUTOSAVE

    results = []

    # Check for save files
    # Check save files are formatted correctly
    printchapter("Checking saves for required files")

    log(f"{s1}Meta Files:")

    # files required to be in the save folder
    SaveMetaRequiredItems = (
        "MySavedGames.mod.meta",
        "steam_autocloud.vdf",
    )

    # get the files at the save file location and ignore folders
    SaveMetaFiles = [folderpath.name for folderpath in PATH_SAVEFOLDER[0].iterdir() if not folderpath.is_dir()]

    if len(SaveMetaRequiredItems) < len(SaveMetaFiles):
        log(f"{s2}[WARNING] More meta files in the save folder than expected {shortenpath(PATH_SAVEFOLDER[0])} ")
        results.append(("[WARNING]", f"More meta files in the save folder than expected {shortenpath(PATH_SAVEFOLDER[0])}"))

    for savemetarequireditem in SaveMetaRequiredItems:
        if savemetarequireditem in SaveMetaFiles:
            log(f"{s2}[OK] {savemetarequireditem}")
            results.append(("[OK]", f"{savemetarequireditem}"))
        else:
            log(f"{s2}[MISSING] {savemetarequireditem}")
            results.append(("[MISSING]", f"{savemetarequireditem}"))
    log()
    log(f"{s1}Save Files:")

    # SaveRequiredItems(name, if file name must match folder name)
    SaveRequiredItems = (
        (".town", False),
        (".saved.import", True),
        (".saved.meta", True),
        (".saved.thumbnail", True),
        (".gamestats", False),
        (".gamestats.meta", False)
    )

    # get all the folders at the save file location and ignore non-folders
    SaveFolders = [folderpath for folderpath in PATH_SAVEFOLDER[0].iterdir() if folderpath.is_dir()]

    # test condition for any failures
    Test_CheckForSaveFilesFailed = False

    # if the save folder is empty
    if not SaveFolders:
        log("No save files found in the save folder.")
        log("Skipping save file integrity check...")
        results.append(("[ERROR]", "No save files found in the save folder."))

    # if the save folder is not empty
    else:

        # look for each required file in each save file
        for folder in SaveFolders:
            for requirement in SaveRequiredItems:
                found_files = [file for file in folder.iterdir() if file.name.endswith(requirement[0])]

                # if the required file was not found
                if len(found_files) < 1:
                    Test_CheckForSaveFilesFailed = True
                    report(f"{s6}[Missing] {requirement[0]}")

                # if to many files were found
                elif len(found_files) > 1 and requirement[1]:
                    Test_CheckForSaveFilesFailed = True
                    report(f"{s6}[Duplicate Files] {requirement[0]}")

                # if required file must also match the name of the save
                elif requirement[1] and found_files[0].stem != folder.name:
                    Test_CheckForSaveFilesFailed = True
                    report(f"{s6}[!NAME] {requirement[0]}")

            # if the report is empty then return good result
            if not Report:
                log(f"{s2}[OK] {folder.name}")
                results.append(("[OK]", f"{folder.name}"))

            # if errors in report then return bad result
            else:
                log(f"{s2}[ERROR] {folder.name}")
                logreport()
                results.append(("[ERROR]", f"{folder.name}"))

    return results

# ------------------------------------------------
# ------------------------------------------------
# ------------------------------------------------

def check_local_mods():

    results = []

    # Check LOCAL mods are formatted correctly
    printchapter("Checking local mods for required files")

    # ModRequiredItems(name, if file name must match folder name)
    ModRequiredItems = (
        ("_Metacache", False),
        ("Settings", False),
        (".mod.meta", True)
    )

    # Folders which are not local mods or do not need to be checked at this time
    ExemptFolders = (
        "MyOptions.mod",
        "Local.mod",
        "0.mod",
        "MySavedGames.mod",
        "MyPremadeLot.mod",
        "MyPremadeOutfits.mod",
        "com.unity.addressables",
        "MyPremadeHouseholds.mod"
    )

    # get local mod folders from local mod folder
    ModFolders = [folderpath for folderpath in PATH_LOCALMODSFOLDER[0].iterdir() if folderpath.is_dir() and folderpath.name not in ExemptFolders]
    Test_CheckForLocalModFilesFailed = False

    # check if any local mods in local mod folder
    if not ModFolders:
        log(f"No local mod files found in the local mods folder.")
        log(f"Skipping local mods file integrity check...")
        results.append(("--", f"No local mod files found in the local mods folder."))
        results.append(("--", f"Skipping local mods file integrity check..."))

    else:

        index = len(results) - 1

        # look for each required file in each mod in the local mods folder
        for folder in ModFolders:
            for requirement in ModRequiredItems:

                # find files which match the required file
                found_files = [file for file in folder.iterdir() if file.name.endswith(requirement[0])]

                # no file found
                if len(found_files) < 1:
                    Test_CheckForLocalModFilesFailed = True
                    report(f"{s6}[Missing] {requirement[0]}")
                    results.append(("", f"[Missing] {requirement[0]}"))

                # too many files found
                elif len(found_files) > 1:
                    Test_CheckForLocalModFilesFailed = True
                    report(f"{s6}[Duplicate Files] {requirement[0]}")
                    results.append(("", f"[Duplicate Files] {requirement[0]}"))

                # if the required file must also match the name of the mod
                elif requirement[1] and found_files[0].stem != folder.name:
                    Test_CheckForLocalModFilesFailed = True
                    report(f"{s6}[Name mismatch] {requirement[0]}")
                    results.append(("", f"[Name mismatch] {requirement[0]}"))

            # check is mod is enabled
            metapath = Path(f"{folder}/{folder.name}.meta")
            enabled = ""
            if Path(metapath).exists():
                config = readconfig(metapath)
                if "Enabled" not in config:
                    enabled = "[MISSING]"
                elif config["Enabled"] == "True":
                    enabled = "Enabled"
                elif config["Enabled"] == "False":
                    enabled = "Disabled"

            if not Report:
                log(f"{s2}[OK] {enabled} {folder.name}")
                results.append(("[OK]", f"{enabled} {folder.name}"))
            else:
                log(f"{s2}[ERROR] {enabled} {folder.name}")
                logreport()
                results.append(("[ERROR]", f"{enabled} {folder.name}"))

    # check test results
    if Test_CheckForLocalModFilesFailed:
        log()
        log("ERROR: Mod file error detected. Automatic fix not possible.")

    return results

# ------------------------------------------------
# ------------------------------------------------
# ------------------------------------------------

def check_workshop_mods():

    results = []

    # Check WORKSHOP mods are formatted correctly
    printchapter("Checking workshop mods for required files")

    log("Status of each workshop mod and if enabled.")
    log()

    # ModRequiredItems(name, if file name must match folder name)
    ModRequiredItems = (
        ("_Metacache", False),
        ("Settings", False),
        (".mod.meta", True)
    )

    # get workshop mod folders from workshop mod folder
    NumberedFolders = [folderpath for folderpath in PATH_WORKSHOPMODSFOLDER[0].iterdir() if folderpath.is_dir()]
    Test_CheckForWorkshopModFilesFailed = False

    # check if numbered workshop mods folder is empty
    if not NumberedFolders:
        log("No workshop mod files found in the workshop mods folder.")
        log("Skipping local mods file integrity check...")
        results.append(("--", f"No workshop mod files found in the workshop mods folder."))
        results.append(("--", f"Skipping local mods file integrity check..."))

    else:

        # for each numbered folder in numbered folders
        for SingleNumberedFolder in NumberedFolders:
            namedfolders = [folderpath for folderpath in SingleNumberedFolder.iterdir()]

            # if there is no folder inside, something is wrong
            if not SingleNumberedFolder.name.isdigit():
                Test_CheckForWorkshopModFilesFailed = True
                log(f"{s2}[ERROR] {shortenpath(SingleNumberedFolder)}")
                log(f"{s6}[Incorrect File in Location]")

                results.append(("[ERROR]", f"{shortenpath(SingleNumberedFolder)}"))
                results.append(("", f"[Incorrect File in Location]"))

            # if there is no folder
            elif len(namedfolders) < 1:
                Test_CheckForWorkshopModFilesFailed = True
                log(f"{s2}[ERROR] {SingleNumberedFolder.name}")
                log(f"{s6}[Empty Folder] Delete this folder.")

                results.append(("[ERROR]", f"{SingleNumberedFolder.name}"))
                results.append(("[Empty Folder]", f"Delete this folder"))

            # if there is more than one folder inside, something is wrong
            elif len(namedfolders) > 1:
                Test_CheckForWorkshopModFilesFailed = True
                log(f"{s2}[ERROR] {SingleNumberedFolder.name}")
                log(f"{s6}[CRITICAL ERROR: Found excess folders]")

                results.append(("[ERROR]", f"Found excess folders"))
                results.append(("[CRITICAL ERROR]", f"Found excess folders"))


            # else there must be the correct number of folders
            else:

                # look for each required file in the mod folder
                for requirement in ModRequiredItems:
                    found_files = [file for file in namedfolders[0].iterdir() if file.name.endswith(requirement[0])]

                    # if none found, negative result
                    if len(found_files) < 1:
                        Test_CheckForWorkshopModFilesFailed = True
                        log(f"{s2}[Missing] {requirement[0]}")
                        results.append(("[Missing]", f"{requirement[0]}"))

                    # if too many found, negative result
                    elif len(found_files) > 1:
                        Test_CheckForWorkshopModFilesFailed = True
                        log(f"{s2}[Duplicate Files] {requirement[0]}")
                        results.append(("[Duplicate Files]", f"{requirement[0]}"))

                    # if required file must also match the name of the mod
                    elif requirement[1] and found_files[0].stem != namedfolders[0].name:
                        Test_CheckForWorkshopModFilesFailed = True
                        log(f"{s2}[Name mismatch] {requirement[0]}")
                        results.append(("[Name mismatch]", f"{requirement[0]}"))

                # check is mod is enabled
                metapath = Path(f"{namedfolders[0]}/{namedfolders[0].name}.meta")
                enabled = ""
                if Path(metapath).exists():
                    config = readconfig(metapath)
                    if "Enabled" not in config:
                        enabled = "[MISSING]"
                    elif config["Enabled"] == "True":
                        enabled = "Enabled"
                    elif config["Enabled"] == "False":
                        enabled = "Disabled"

                log(f"{s2}[OK] {enabled} {namedfolders[0].name} SteamID:{SingleNumberedFolder.name}")
                results.append(("[OK]", f"{enabled} {namedfolders[0].name} SteamID:{SingleNumberedFolder.name}"))

    # check test results
    if Test_CheckForWorkshopModFilesFailed:
        log()
        log("ERROR: Mod file error detected. Automatic fix not possible.")

    return results

# ------------------------------------------------
# ------------------------------------------------
# ------------------------------------------------

def check_complex_mod_problems():

    results = []

    # Check player.log for errors
    printchapter(f"Check for complex mod errors")

    # ---------------------------------------------------------------------------------------
    # ----------------------------CHECK FOR DUPLICATE MODS-----------------------------------
    # ---------------------------------------------------------------------------------------

    # get mod folders
    workshop_folders = {folder.name for folder in PATH_WORKSHOPMODSFOLDER[0].rglob("*") if folder.is_dir() and folder.name.endswith(".mod")}
    local_folders = {folder.name for folder in PATH_LOCALMODSFOLDER[0].rglob("*") if folder.is_dir()}

    # put overlap into an array
    duplicates = workshop_folders & local_folders

    # print array of duplicates
    if duplicates:
        log(f"{s2}[ERROR] Duplicate folders are usually caused by moving mods to the local folder and not unsubcribing from the mod. Duplicate mods need to be removed.")
        results.append(("[ERROR]", f"Duplicate folders are usually caused by moving mods to the local folder and not unsubcribing from the mod. Duplicate mods need to be removed."))
        for folder in duplicates:
            log(f"{s4}[DUPLICATE FOLDER] {folder}")
            results.append(("", f"[DUPLICATE FOLDER] {folder}"))
    else:
        log(f"{s2}[OK] No duplicates found")
        results.append(("[OK]",f"No duplicates found"))

    # ---------------------------------------------------------------------------------------
    # -------------------------------CHECK FOR EMPTY FOLDERS---------------------------------
    # ---------------------------------------------------------------------------------------

    empty_folders = [folder for folder in PATH_WORKSHOPMODSFOLDER[0].rglob("*") if
                     folder.is_dir() and not any(folder.iterdir())]

    if len(empty_folders) > 0:
        log()
        log(f"{s2}[ERROR] Empty folders are usually caused by moving mods to the local folder and not removing the numbered folders. Empty folders need to be removed.")
        for folder in empty_folders:
            log(f"{s4}[EMPTY FOLDER] {folder}")
            results.append(("", f"[EMPTY FOLDER] {folder}"))
    else:
        log()
        log(f"{s2}[OK] No empty folders found")
        results.append(("[OK]", f"No empty folders found"))

    # ---------------------------------------------------------------------------------------
    # --------------------------------CHECK FOR .TMP FILES-----------------------------------
    # ---------------------------------------------------------------------------------------

    workshop_tmp = [file for file in PATH_WORKSHOPMODSFOLDER[0].rglob("*.tmp") if file.is_file()]
    local_tmp = [file for file in PATH_LOCALMODSFOLDER[0].rglob("*.tmp") if file.is_file()]
    if workshop_tmp or local_tmp:
        log()
        log(f"{s2}[ERROR] .tmp files found in mods")
        results.append(("[ERROR]", f"Tmp files found in mods"))
        if workshop_tmp:
            log(f"{s3}workshop mods:")
            results.append(("workshop mods",""))
            for file in workshop_tmp:
                log(f"{s4}[TMP] {shortenpath(file)}")
                results.append(("", f"[TMP] {shortenpath(file)}"))
        if local_tmp:
            log(f"{s3}local mods:")
            results.append(("local mods", ""))
            for file in local_tmp:
                log(f"{s4}[TMP] {shortenpath(file)}")
                results.append(("", f"[TMP] {shortenpath(file)}"))
    else:
        log()
        log(f"{s2}[OK] No .tmp files found")
        results.append(("[OK]", f"No .tmp files found"))

    return results

# ------------------------------------------------
# ------------------------------------------------
# ------------------------------------------------

def check_player_log():

    results = []

    # number of lines to read in the player.log
    LinesToRead = 500

    # number of errors to look for
    NumberOfErrors = 15

    # Check player.log for errors
    printchapter(f"Errors in Player.log")

    # ingest player.log
    with open(PATH_PLAYERLOG[0], encoding="utf-8") as file:
        lines = []
        for _ in range(LinesToRead):
            line = file.readline()
            if not line:
                break
            lines.append(line.rstrip("\n"))

    # known errors
    KnownErrors = {
        "An error ocurred",
        "Material builder",
        "FileNotFound",
        "Failed to",
        "Could not",
        "System Exception",
        "Runtime data",
        "OperationException",
        "DirectoryNot"
    }

    errors = []

    # scan for errors
    for line_number, line in enumerate(lines, start=1):
        for error in KnownErrors:
            if line.startswith(error):
                errors.append((error, line_number, line))
                break
        if len(errors) >= NumberOfErrors:
            break

    # check how many errors were found
    if len(errors) <= 0:
        log(f"{s2}No known errors found in the Player.Log. Still take a look at the Player.log for errors.")
        results.append(("No known errors found in the Player.Log. Still take a look at the Player.log for errors.", ""))
    else:
        log(f"{s2}Note: Focus on the earliest errors which likely caused the later errors.")
        log()
        results.append(("Note: Focus on the earliest errors which likely caused the later errors.", ""))

    # print found errors
    for error, line_number, line in errors[:10]:
        log(f"{s3}Line {line_number}: {removeusername(line)}...")
        results.append((f"Line {line_number}", f"{removeusername(line)}..."))

    return results

# ------------------------------------------------
# ------------------OPEN FOLDERS------------------
# ------------------------------------------------

def open_savefolder():
    os.startfile(PATH_SAVEFOLDER[0])

def open_localmods():
    os.startfile(PATH_LOCALMODSFOLDER[0])

def open_workshopmods():
    os.startfile(PATH_WORKSHOPMODSFOLDER[0])

def open_player_log():
    os.startfile(PATH_PLAYERLOG[0])