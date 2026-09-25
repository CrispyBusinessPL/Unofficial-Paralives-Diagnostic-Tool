import tomllib
from pathlib import Path

DEFAULTS = {
"FLAG": "FLAG",
"FONT": "Arial",
"FONTSIZE": 10,
"TITLE": "Unofficial Paralives Diagnostic Tool",
"SUBTITLE": "Diagnostic tool for fixing game files and mods",
"DESCRIPTION": """[DEFAULT LANG]
Fail - this program encountered an error which prevented further testing.
Error - something was detected which may be causing a problem(s).
Critical Error - something was detected which is almost certainly causing problems.
Missing - a file is missing that is expected to be there. This does not necessarily mean there is a problem.
Duplicate Files - multiple versions of a file when there should only be one.""",
"LABEL1": "Game Paths",
"LABEL2": "Save Files",
"LABEL3": "Local Mods",
"LABEL4": "Workshop Mods",
"LABEL5": "Complex Problems",
"LABEL6": "Player Log",
"BUTTON1": "Run Diagnostic",
"BUTTON2": "Open Report",
"BUTTON3a": "Dark Mode",
"BUTTON3b": "Light Mode",
"BUTTON4": "Saves",
"BUTTON5": "Local Mods",
"BUTTON6": "Workshop Mods",
"BUTTON7": "Player Log",
"TXT_UNCHECKED": "Unchecked",
"TXT_CHECKING": "Checking",
"TXT_COMPLETE": "Complete",
"TXT_VALID": "Valid",
"TXT_INVALID": "Invalid",
"TXT_MISSINGCRITICALFILE": "Missing critical file",
"TXT_FILE": "File"
}

# Check for language files and ingest data
def importlanguage(path, DEBUGMODE = False):

    if path.exists():

        localizations = {}

        for file in Path(path).glob("*.txt"):
            try:
                with open(file, "rb") as f:
                    localizations[file.stem] = tomllib.load(f)
            except (OSError, tomllib.TOMLDecodeError) as e:
                print(f"Error loading {file.name}: {e}")

        if DEBUGMODE:
            print(f"Translation folder found at {path}")
            for key, value in localizations.items():
                #print(f"{key} = {value}")
                print(f"{key}")

        return localizations

    else:
        print(f"Using default translations: No translations at {path}")
        return {}

def load_language(path, dict):

    Languages = importlanguage(path)
    return {**DEFAULTS, **Languages.get(dict, {})}



















