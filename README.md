# The Unofficial Paralives Diagnostic Tool

**by Crispy Business**

A diagnostic tool for Paralives game files. This program reads your Paralives game files and displays diagnostic information. **This program is currently unable to fix identified issues.**

## How to Use

1. Run `CBParalivesDiagnosticTool.exe` **or** `CBParalivesDiagnosticTool.py`.
2. Review the generated report.
3. If you would like more information or help fixing identified issues, post the report to the Paralives Discord.

## Requirements

* Paralives must be installed using Steam.
* Python is required to use the `.py` script.
* No Python installation is required when using the `.exe`.

## Configuration

The program optionally supports a `config.toml` file for overriding the default file paths.

## How to Read the Log

* Look for `[OK]` in the left column. This means no issues were identified.
* Any other status indicates that a trivial-to-critical issue has been identified with reasonable confidence.

## Changelog

### 21 Sep 2026 — Version 1.0

**Game folders and file paths**

* Checks for required game folders and file paths:

  * Correct location
  * Enabled status

**Save files**

* Lists all save files
* Reports status

**Local mods**

* Lists all local mods
* Reports status
* Validates file structure
* Identifies missing files
* Checks whether mods are enabled

**Workshop mods**

* Lists all Workshop mods
* Reports status
* Validates file structure
* Identifies missing files
* Checks whether mods are enabled
* Displays Steam ID

**Complex Mod Errors**

* Detects duplicate folders
* Detects empty folders
* Detects `.tmp` files

**Folder Shortcuts**

* Save folder
* Workshop Mods folder
* Local Mods folder
* `Player.log`

**Diagnostic Log**

* Generates a log file containing all identified information
* Log files use shortened file paths to help protect user privacy

**Configuration File**

* Local Mods folder can be configured
* Workshop Mods folder can be configured

## Potential Future Features

* Improved problem diagnosis
* Improved advice for fixing identified issues
* Ability to fix some basic file issues:

  * Move mods to the Local Mods folder
  * Possibly create a collection and unsubscribe from Workshop mods
  * Remove empty files and folders
  * Option to purge the AppData folder
  * Validate game files
  * Unsubscribe from Workshop mods

## Disclosure

This program is **not affiliated with, endorsed by, or associated with Paralives Studio**.

Use this program at your own risk. The author is not responsible for any damage, data loss, corrupted files, or other issues that may result from using this software.

This software may not be resold, redistributed, or commercially repackaged without the author's explicit permission.

**Copyright © 2026 Crispy Business. All rights reserved.**
