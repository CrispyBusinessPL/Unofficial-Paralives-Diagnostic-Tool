
-----------------------------------------------------------
THE UNOFFICIAL PARALIVES DIAGNOSTIC TOOL by Crispy Business
-----------------------------------------------------------

SUMMARY:

	A diagnostic tool for Paralives game files. This program reads your Paralives game files and displays diagnostic information. This program is not able to fix identified issues at this time.

HOW TO USE:

	1. Run CBParalivesDiagnosticTool.exe OR CBParalivesDiagnosticTool.py
	2. Review the generated report
	3. Post the report to the Paralives Discord if you would like more information or help fixing the identified issues.

REQUIREMENTS:

	* Requires Paralives game installed using Steam.
	* Python is required is use Python script.
	* No Python installation is required when using the .exe.

CONFIGURATION:

	* The program has an optional config.toml file for overriding the default file paths.
	
HOW TO READ LOG:

	* Scan the left column for [OK] which means no issues were identified.
	* Any other status means a trivial to critical issue has been identified with reasonable confidence.

CHANGELOG:

	21 Sep 2026 - 1.0 Release
		- Checks for required game folders and file paths
			* In correct location
			* Is enabled
		- Checks save files
			* Lists all save files
			* Status
		- Checks local mods for required files
			* Lists all mods
			* Status
			* Validate file structure
			* Missing files
			* If enabled
		- Checks workshop mods for required files
			* Lists all mods
			* Status
			* Validate file structure
			* Missing files
			* If enabled
			* Steam ID
		- Checks for Complex Mod Errors
			* Duplicate folders
			* Empty folders
			* .tmp files
		- Creates Folder Shortcuts
			* Save Folder
			* Workshop Mods
			* Local Mods
			* Player.log
		- Generates a log file with all identified information
			* Log files have shortened file paths to protect privacy.
		- Configuration File
			* Local mod folder can be configured
			* Workshop mod folder can be configured

POTENTIAL FUTURE FEATURES:

	- Improved problem diagnosis
	- Improved advice for how to fix identified issues
	- Ability to fix some basic file issues
		* Move mods to local (possibly make collection and unsubscribe)
		* Remove empty files and folders
		* Option to purge the appdata folder
		* Validate game files
		* Unsubscribe from workshop mods

DISCLOSURE:

This program is not affiliated with, endorsed by, or associated with Paralives Studio. Use this program at your own risk. The author is not responsible for any damage, data loss, corrupted files, or other issues that may result from using this program. This software may not be resold, redistributed, or commercially repackaged without the author's explicit permission. Copyright © 2026. All rights reserved.
