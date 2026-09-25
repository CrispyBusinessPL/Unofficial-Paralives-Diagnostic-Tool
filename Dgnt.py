# for opening the log file
import os

# for reading game files
from pathlib import Path

# for timestamping logs
from datetime import datetime

# for reading config file
import tomllib

# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

TimeStamp = ""
TEXTFORMATTING = [s1 := " "*1,s2 := " "*2,s3 := " "*3,s4 := " "*4,s5 := " "*5,s6 := " "*6]
OutputText = ""
Report = ""
Lang = {}

# array of paths to critical files
FilePaths = {}

# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

def outputfilepath():
    return FilePaths["OUTPUTPATH"] / f"CBDiagnosticLog_{TimeStamp}.txt"

def updatetimestamp():
    global TimeStamp
    TimeStamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# set global file paths
def setfilepaths(configuration,executionfolder):
    global FilePaths

    DEFAULT_WORKSHOP_FOLDER = r"C:\Program Files (x86)\Steam\steamapps\workshop\content\1118520"
    DEFAULT_LOCAL_MODS_FOLDER = Path.home() / "AppData" / "LocalLow" / "Paralives" / "Paralives"

    WORKSHOP_MODS_FOLDER = Path(configuration.get("Workshop_Mods_Folder") or DEFAULT_WORKSHOP_FOLDER)
    LOCAL_MODS_FOLDER = Path(configuration.get("Local_Mods_Folder") or DEFAULT_LOCAL_MODS_FOLDER)

    paths = {
        # root folders
        "PATH_WORKSHOPMODSFOLDER": WORKSHOP_MODS_FOLDER,
        "PATH_LOCALMODSFOLDER": LOCAL_MODS_FOLDER,

        # sub folders
        "PATH_SAVEFOLDER": Path(LOCAL_MODS_FOLDER / "MySavedGames.mod"),
        "PATH_PREMADEHOUSEHOLDS": Path(LOCAL_MODS_FOLDER / "MyPremadeHouseholds.mod"),
        "PATH_PREMADELOTS": Path(LOCAL_MODS_FOLDER / "MyPremadeLot.mod"),
        "PATH_PREMADEOUTFITS": Path(LOCAL_MODS_FOLDER / "MyPremadeOutfits.mod"),
        "PATH_LOCALDOTMOD": Path(LOCAL_MODS_FOLDER / "Local.mod"),
        "PATH_ZERODOTMOD": Path(LOCAL_MODS_FOLDER / "0.mod"),
        "PATH_PLAYERLOG": Path(LOCAL_MODS_FOLDER / "Player.log"),
        "PATH_PREVPLAYERLOG": Path(LOCAL_MODS_FOLDER / "Player-prev.log"),

        # output path
        "OUTPUTPATH": executionfolder,
    }
    FilePaths = paths

# add to queue to be written to the log file
def log(text=""):
    global OutputText
    OutputText += str(text) + "\n"
    #print(text)

# add to queue but do not print
def logonly(text: str=""):
    global OutputText
    OutputText += str(text) + "\n"

# write the queued logs to the log file
def appendlogtofile():
    global OutputText
    try:
        with open(outputfilepath(), "a", encoding="utf-8") as file:
            file.write(OutputText)
            OutputText = ""
    except PermissionError:
        print(f"Console: Could not update log file because the file is locked.\n")

# Resets log file in debugmode
def clearlogfile():
    try:
        with open(f"{FilePaths["OUTPUTPATH"]}_{TimeStamp}", "w", encoding="utf-8") as file:
            pass
    except PermissionError:
        print(f"Console: Could not clear log file because the file is locked.\n")

# Stores text during formatting
def report(text: str=""):
    global Report
    Report += str(text) + "\n"

# Logs outstanding reports
def logreport():
    global Report
    global OutputText
    OutputText += f"{Report}"
    print(Report, end="")
    Report = ""

# Format chapter titles in log
def printchapter(text: str="-"*38):
    length = len(text) + 6
    log("\n"+"-"*length)
    log(f"---{text}---")
    log("-"*length+"\n")
    appendlogtofile()

# remove username from paths
USERNAME = Path.home().name
def removeusername(text: str):
    return text.replace(USERNAME, "********")

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

# Check for config file and ingest data
def importconfig(path):

    if path.exists():
        print(f"Found config file at {path}")
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        text = text.replace("\\", "\\\\")
        return tomllib.loads(text)

    else:
        print(f"Using default paths: No config file at {path}")
        return {}

# Update external config file with new information
def updateconfig(path,key,value):
    if Path(path).exists():
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if line.strip().startswith(key) and "=" in line:
                lines[i] = f'{key} = "{value}"\n'
                break

        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)

def pastelogheader():
    log(TimeStamp)
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
    for path in FilePaths.values():

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

            logonly(f"{s2}[OK] {path.name.ljust(22, ".")}{enabled.ljust(9, ".")}..{shortenpath(path)}")
            #print(f"{s2}[OK] {description.ljust(22, ".")}{enabled.ljust(9, ".")}..{path}")
            results.append(("[PATHOK]", f"{path.name} {enabled}",f"{path}"))

        # if the path does not exist, log negative result. Shorten path name only in the log.
        else:
            Test_FilePathsFailed = True
            logonly(f"{s2}[FAIL] {path.name.ljust(22, ".")}..{shortenpath(path)}")
            #print(f"{s2}[FAIL] {description.ljust(22, ".")}..{path}")
            results.append(("[PATHFAIL]", f"{path.name}",f"{path}"))

    appendlogtofile()
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
    SaveMetaFiles = [folderpath.name for folderpath in FilePaths["PATH_SAVEFOLDER"].iterdir() if not folderpath.is_dir()]

    if len(SaveMetaRequiredItems) < len(SaveMetaFiles):
        log(f"{s2}[WARNING] More meta files in the save folder than expected {shortenpath(FilePaths["PATH_SAVEFOLDER"])} ")
        results.append(("[WARNING]", f"More meta files in the save folder than expected {shortenpath(FilePaths["PATH_SAVEFOLDER"])}"))

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
    SaveFolders = [folderpath for folderpath in FilePaths["PATH_SAVEFOLDER"].iterdir() if folderpath.is_dir()]

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

    appendlogtofile()
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
        ("_Metacache", False, "Folder"),
        ("Settings", False, "Folder"),
        (".mod.meta", True, "File")
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
    ModFolders = [folderpath for folderpath in FilePaths["PATH_LOCALMODSFOLDER"].iterdir() if folderpath.is_dir() and folderpath.name not in ExemptFolders]
    Test_CheckForLocalModFilesFailed = False

    # check if any local mods in local mod folder
    if not ModFolders:
        log(f"No local mod files found in the local mods folder.")
        log(f"Skipping local mods file integrity check...")
        results.append(("--", f"No local mod files found in the local mods folder."))
        results.append(("--", f"Skipping local mods file integrity check..."))

    else:

        # look for each required file in each mod in the local mods folder
        for folder in ModFolders:

            index = len(results)
            results.append(["Local Mod", f"{folder.name}"])
            #results.append(("[ERROR]", f"{enabled} {folder.name}"))

            for requirement in ModRequiredItems:

                # find files which match the required file
                found_files = [file for file in folder.iterdir() if file.name.endswith(requirement[0])]

                # no file found
                if len(found_files) < 1:
                    Test_CheckForLocalModFilesFailed = True
                    report(f"{s6}[Missing] {requirement[0]} {requirement[2]}")
                    results.append(("", f"[Missing] {requirement[0]} {requirement[2]}"))

                # too many files found
                elif len(found_files) > 1:
                    Test_CheckForLocalModFilesFailed = True
                    report(f"{s6}[Duplicate Files] {requirement[0]} {requirement[2]}")
                    results.append(("", f"[Duplicate Files] {requirement[0]} {requirement[2]}"))

                # if the required file must also match the name of the mod
                elif requirement[1] and found_files[0].stem != folder.name:
                    Test_CheckForLocalModFilesFailed = True
                    report(f"{s6}[Name mismatch] {requirement[0]} {requirement[2]}")
                    results.append(("", f"[Name mismatch] {requirement[0]} {requirement[2]}"))

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
                results[index][0] = f"[OK]"
                results[index][1] = f"{enabled} {results[index][1]}"
            else:
                log(f"{s2}[ERROR] {enabled} {folder.name}")
                logreport()
                results[index][0] = f"[ERROR]"
                results[index][1] = f"{enabled} {results[index][1]}"


    # check test results
    if Test_CheckForLocalModFilesFailed:
        log()
        log("ERROR: Mod file error detected. Automatic fix not possible.")

    appendlogtofile()
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
    NumberedFolders = [folderpath for folderpath in FilePaths["PATH_WORKSHOPMODSFOLDER"].iterdir() if folderpath.is_dir()]
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

    appendlogtofile()
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
    workshop_folders = {folder.name for folder in FilePaths["PATH_WORKSHOPMODSFOLDER"].rglob("*") if folder.is_dir() and folder.name.endswith(".mod")}
    local_folders = {folder.name for folder in FilePaths["PATH_LOCALMODSFOLDER"].rglob("*") if folder.is_dir()}

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

    empty_folders = [folder for folder in FilePaths["PATH_WORKSHOPMODSFOLDER"].rglob("*") if
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

    workshop_tmp = [file for file in FilePaths["PATH_WORKSHOPMODSFOLDER"].rglob("*.tmp") if file.is_file()]
    local_tmp = [file for file in FilePaths["PATH_LOCALMODSFOLDER"].rglob("*.tmp") if file.is_file()]
    if workshop_tmp or local_tmp:
        log()
        log(f"{s2}[ERROR] .tmp files found in mods")
        results.append(("[ERROR]", f"Tmp files found in mods"))
        if workshop_tmp:
            log(f"{s3}workshop mods:")
            results.append(("workshop mods:",""))
            for file in workshop_tmp:
                log(f"{s4}[TMP] {shortenpath(file)}")
                results.append(("", f"[TMP] {file}"))
        if local_tmp:
            log(f"{s3}local mods:")
            results.append(("local mods:", ""))
            for file in local_tmp:
                log(f"{s4}[TMP] {shortenpath(file)}")
                results.append(("", f"[TMP] {file}"))
    else:
        log()
        log(f"{s2}[OK] No .tmp files found")
        results.append(("[OK]", f"No .tmp files found"))

    appendlogtofile()
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
    with open(FilePaths["PATH_PLAYERLOG"], encoding="utf-8") as file:
        lines = []
        for _ in range(LinesToRead):
            line = file.readline()
            if not line:
                break
            lines.append(line.rstrip("\n"))

    if not lines:
        log(f"{s2}Player.log is empty.")
        appendlogtofile()
        results.append(("[ERROR]", "Player.log is empty."))
        return results

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

    appendlogtofile()
    return results

# ------------------------------------------------
# ------------------OPEN FOLDERS------------------
# ------------------------------------------------

def open_savefolder():
    if Path(FilePaths["PATH_SAVEFOLDER"]).exists():
        os.startfile(FilePaths["PATH_SAVEFOLDER"])

def open_localmods():
    if Path(FilePaths["PATH_LOCALMODSFOLDER"]).exists():
        os.startfile(FilePaths["PATH_LOCALMODSFOLDER"])

def open_workshopmods():
    if Path(FilePaths["PATH_WORKSHOPMODSFOLDER"]).exists():
        os.startfile(FilePaths["PATH_WORKSHOPMODSFOLDER"])

def open_player_log():
    if Path(FilePaths["PATH_PLAYERLOG"]).exists():
        os.startfile(FilePaths["PATH_PLAYERLOG"])

def open_log():
    if Path(outputfilepath()).exists():
        os.startfile(outputfilepath())
