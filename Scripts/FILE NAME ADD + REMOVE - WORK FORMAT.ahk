; Auto-generated FILE NAME ADD + REMOVE - WORK FORMAT script - Created by Nick Robinson

#Persistent

; Initialize variables
global SelectedFolder := "" ; Stores path selected by button OR validated from input
global FileList := {}      ; Object to store all files and their states
global FileQueue := []     ; Array to store files to be processed
global CurrentListFolder := "" ; Tracks the folder associated with the current FileList/Queue

; GUI Definition
; --- Folder Selection Area ---
Gui, Add, Text, x10 y10 w185, Folder Path:
Gui, Add, Edit, x10 y25 w185 vFolderPathInput gValidatePathOnChange
Gui, Add, Button, x10 y50 w90 gSelectFolder, Select Folder
Gui, Add, Button, x105 y50 w90 gValidatePathButton, Validate Path
; --- Text Modification Area ---
Gui, Add, Text, x10 y93, Enter text to modify file names:
Gui, Add, Edit, x10 y110 vInputText w185,
Gui, Add, Text, x10 y135 vReplaceLabel, Enter replacement text:
Gui, Add, Edit, x10 y153 vReplacementText w185 Disabled,
; --- Mode/Placement/Case Area ---
Gui, Add, GroupBox, x10 y180 w90 h80, Mode
Gui, Add, Radio, x20 y200 w40 vModeAdd gProcessModeChange Checked, ADD
Gui, Add, Radio, x20 y220 w40 vModeRemove gProcessModeChange, REMOVE
Gui, Add, Radio, x20 y240 w30 vModeReplace gProcessModeChange, REPLACE
Gui, Add, GroupBox, x105 y180 w90 h80, Placement
Gui, Add, Radio, x115 y200 w70 vPlaceFront gHandlePlacement Checked, FRONT
Gui, Add, Radio, x115 y220 w70 vPlaceEnd gHandlePlacement, END
Gui, Add, Radio, x115 y240 w70 vPlaceBoth gHandlePlacement, BOTH

Gui, Add, GroupBox, x10 y270 w185 h40 vCaseGroup, Case Sensitivity
Gui, Add, CheckBox, x20 y290 vCaseSensitive Disabled, CASE SENSITIVE?
; --- Specific Files Area ---
Gui, Add, GroupBox, x10 y320 w185 h60, MODE OPTION 2
Gui, Add, CheckBox, x20 y340 w80 vSpecificFiles gToggleSpecificFiles Disabled, Specific Files
Gui, Add, Button, x105 y335 w75 vSelectFilesButton gSelectFiles Disabled, Select Files
Gui, Add, Text, x20 y360 h10 vHelpText1 Hidden, Select specific files...

; --- Action Buttons Area ---
Gui, Add, Button, x10 y390 w90 gStartScript, START
Gui, Add, Button, x105 y390 w90 gExitScript, Exit

Gui, Show, w205 h425, File Renaming Tool

; Set initial state for replacement text label since we start in ADD mode
GuiControl, Disable, ReplaceLabel
Return

;===============================================================================
; GUI Event Handlers
;===============================================================================

; Process mode selection changes
ProcessModeChange:
    Gui, Submit, NoHide
    If (ModeAdd) { ; ADD Mode
        GuiControl, Enable, Placement
        GuiControl, Enable, FRONT
        GuiControl, Enable, END
        GuiControl, Enable, BOTH
        GuiControl, Disable, ReplacementText
        GuiControl, Disable, ReplaceLabel  ; Disable the label
        GuiControl, Disable, CaseSensitive
        GuiControl,, CaseSensitive, 0  ; Set to unchecked
    } Else If (ModeRemove) { ; REMOVE Mode
        GuiControl, Disable, Placement
        GuiControl, Disable, FRONT
        GuiControl, Disable, END
        GuiControl, Disable, BOTH
        GuiControl, Disable, ReplacementText
        GuiControl, Disable, ReplaceLabel  ; Disable the label
        GuiControl, Enable, CaseSensitive
        GuiControl,, CaseSensitive, 0  ; Set to unchecked by default
    } Else { ; REPLACE Mode
        GuiControl, Disable, Placement
        GuiControl, Disable, FRONT
        GuiControl, Disable, END
        GuiControl, Disable, BOTH
        GuiControl, Enable, ReplacementText
        GuiControl, Enable, ReplaceLabel   ; Enable the label
        GuiControl, Enable, CaseSensitive
        GuiControl,, CaseSensitive, 0  ; Set to unchecked by default
    }
Return

; Handle placement updates
HandlePlacement:
    Gui, Submit, NoHide
Return

; Handle folder selection via Button
SelectFolder:
    FileSelectFolder, TempSelectedFolder, , 3, Select a folder:
    If (TempSelectedFolder != "") {
        SelectedFolder := TempSelectedFolder ; Update the global variable
        GuiControl,, FolderPathInput, %SelectedFolder% ; Update the Edit control
        ; Check if path is valid and enable downstream controls
        If (PathIsValid(SelectedFolder)) {
             HandleValidFolderSelected(SelectedFolder)
        } Else {
             MsgBox, 48, Error, The selected path is not a valid folder.
             GuiControl,, FolderPathInput, ; Clear input field if invalid
             SelectedFolder := "" ; Reset global variable
        }
    }
Return

; Validate Path from Input Field (triggered by button or on change)
ValidatePathButton: ; Also called by g-label
ValidatePathOnChange:
    If (A_GuiControlEvent == "Normal") ; Triggered by Button or Enter press
        Gui, Submit, NoHide
    Else ; Triggered by focus change or programmatic update - don't submit yet
        GuiControlGet, FolderPathInput,, FolderPathInput

    TempInputPath := FolderPathInput
    If PathIsValid(TempInputPath) {
        ; If path is valid and DIFFERENT from the currently processed folder, update
        if (TempInputPath != SelectedFolder) {
            SelectedFolder := TempInputPath
            HandleValidFolderSelected(SelectedFolder)
            ; Optionally add a visual cue like changing background color briefly
        }
    } Else {
        ; Optional: Indicate invalid path visually (e.g., red background)
        ; GuiControl, +BackgroundFF0000, FolderPathInput
        ; ToolTip, Path is not a valid folder
        ; SetTimer, RemoveToolTip, -1000
    }
return

; RemoveToolTip:
;  ToolTip
; return


; Handle enabling downstream controls and updating file list when a VALID folder is confirmed
HandleValidFolderSelected(validPath) {
    global CurrentListFolder, SpecificFiles
    GuiControl, Enable, SpecificFiles
    GuiControl, Enable, InputText ; Enable main input now that we have a folder
    GuiControl, Enable, StartScript ; Can enable start once folder is valid

    ; Reset Specific Files state if folder changes
    GuiControl,, SpecificFiles, 0
    GuiControl, Disable, SelectFilesButton
    GuiControl, Hide, HelpText1

    ; Reset FileList and Queue
    UpdateFileList(true) ; Initialize with all files selected by default
}


; Handle Specific Files checkbox toggle
ToggleSpecificFiles:
    Gui, Submit, NoHide
    if (SpecificFiles) {
        GuiControl, Enable, SelectFilesButton
        GuiControl, Show, HelpText1
        UpdateFileList(false) ; Set all files to FALSE when enabling specific selection
    } else {
        GuiControl, Disable, SelectFilesButton
        GuiControl, Hide, HelpText1
        UpdateFileList(true)  ; Set all files to TRUE when disabling specific selection
    }
Return

; Handle specific file selection via button
SelectFiles:
    If !PathIsValid(SelectedFolder) { ; Double check folder validity
        MsgBox, 48, Error, Please select or enter a valid folder first.
        Return
    }

    FileSelectFile, TempSelectedFiles, M3, %SelectedFolder%, Select specific files:, All Files (*.*)
    If (TempSelectedFiles != "") {
        ; Reset queue and list states before adding selected
        UpdateFileList(false) ; Set all to false
        FileQueue := []       ; Clear queue

        ; Base directory is the first line
        Loop, Parse, TempSelectedFiles, `n
        {
            if (A_Index = 1) {
                baseDir := A_LoopField
                continue
            }
            if (A_LoopField = "") ; Skip empty lines if any
                continue

            ; Set selected file to TRUE and add to queue
            FileList[A_LoopField] := true
            FileQueue.Push(A_LoopField)
        }
         MsgBox, 64, Info, % "Selected " . FileQueue.Length() . " files for processing in " . baseDir
    }
Return

; Start script logic
StartScript:
    Gui, Submit, NoHide
    ChosenPath := "" ; Initialize ChosenPath for clarity

    ; --- 1. Determine and Validate Folder Path ---
    InputPath := FolderPathInput
    ButtonPath := SelectedFolder ; This holds the last validated path (either from button or input)

    if PathIsValid(InputPath) {
        ChosenPath := InputPath
    } else if PathIsValid(ButtonPath) {
        ChosenPath := ButtonPath
        GuiControl,, FolderPathInput, %ChosenPath% ; Update input field if ButtonPath was used
    } else {
        MsgBox, 48, Error, No valid folder path specified.`nPlease enter a valid path or use 'Select Folder'.
        Return
    }

    ; --- 2. Check if Folder Changed and Update File List/Queue ---
    if (ChosenPath != CurrentListFolder) {
        SelectedFolder := ChosenPath ; Update global variable for other functions
        if (SpecificFiles) {
            UpdateFileList(false) ; Reset states
            FileQueue := []       ; Clear queue
            MsgBox, 64, Info, Folder path changed. File list reset.`nPlease use 'Select Files' again if needed.
            ; No return here, let it proceed, the queue length check below will catch it
        } else {
            UpdateFileList(true) ; Update list for new folder (all files selected)
        }
         ; Ensure CurrentListFolder is updated by UpdateFileList
    }

    ; --- 3. Validate Other Inputs ---
    If (InputText = "") {
        MsgBox, 48, Error, Please enter text to modify file names.
        Return
    }
    If (ModeReplace && ReplacementText = "") {
        MsgBox, 48, Error, Please enter replacement text for REPLACE mode.
        Return
    }
    If (FileQueue.Length() = 0) {
        if (SpecificFiles)
             MsgBox, 48, Error, No specific files selected for processing. Use 'Select Files'.
        else
             MsgBox, 64, Info, No files found or selected in the target folder to process. ; Could be an empty folder
        Return
    }

    ; --- 4. Process Files ---
    SetBatchLines, -1 ; Improve performance
    If (ModeAdd)
        ProcessFiles("ADD", ChosenPath)
    Else If (ModeRemove)
        ProcessFiles("REMOVE", ChosenPath)
    Else ; REPLACE Mode
        ProcessFiles("REPLACE", ChosenPath)
    SetBatchLines, 10ms ; Restore default
Return


; Exit button or Esc key
ExitScript:
GuiClose:
Esc::
    ExitApp
Return

;===============================================================================
; Helper Functions
;===============================================================================

; Helper function to check if a path is a valid existing directory
PathIsValid(path) {
    local Attribs ; Good practice to declare variables used only in the function as local

    ; Basic checks first
    if (path = "" || !FileExist(path)) {
        Return false
    }

    ; Get the attributes using the command syntax
    FileGetAttrib, Attribs, %path% ; Note the command syntax and %path%

    ; Check if FileGetAttrib itself encountered an error
    if ErrorLevel {
        Return false
    }

    ; Check if the retrieved attributes contain 'D'
    if InStr(Attribs, "D") {
        Return true ; It's a directory
    } else {
        Return false ; It exists but is not a directory
    }
}


; Update FileList and FileQueue based on folder selection
; setAllTrue = true means select all files by default (SpecificFiles unchecked)
; setAllTrue = false means deselect all files (SpecificFiles checked, before user selects)
UpdateFileList(setAllTrue := true) {
    global FileList, FileQueue, SelectedFolder, CurrentListFolder

    ; Ensure SelectedFolder is valid before proceeding
    if !PathIsValid(SelectedFolder) {
        CurrentListFolder := "" ; Clear current folder tracker
        Return ; Don't try to loop if folder is invalid
    }

    FileList := {}      ; Clear existing file list
    FileQueue := []     ; Clear existing queue
    CurrentListFolder := SelectedFolder ; Track the folder we are listing

    Loop, Files, %SelectedFolder%\*.*
    { ; Brace for Loop
        FileList[A_LoopFileName] := setAllTrue  ; Set initial toggle state
        if (setAllTrue)
            FileQueue.Push(A_LoopFileName)      ; Add to queue if TRUE
    } ; Brace for Loop
    ; If SpecificFiles mode is NOT active, FileQueue now holds all files.
    ; If SpecificFiles mode IS active, FileQueue will be empty until user selects files.
} ; Brace for UpdateFileList function

; Helper function to escape RegEx special characters
RegExEscape(String) {
    Return RegExReplace(String, "[\.\*\?\+\[\{\|\(\)\^\$\\]", "\$0")
} ; Brace for RegExEscape function

; Process file renaming
; Added 'folderPath' parameter to ensure the correct path is used
ProcessFiles(mode, folderPath)
{ ; Opening Brace for ProcessFiles function
    ; Make global declarations the first thing inside the function body
    global FileList, FileQueue, InputText, ReplacementText, PlaceFront, PlaceEnd, PlaceBoth, CaseSensitive

    ; Keep track of successful renames to update queue
    newFileQueue := []
    processedCount := 0
    errorCount := 0

    ; Process only files in the FileQueue
    for index, filename in FileQueue
    { ; Opening Brace for For loop
        ; Ensure the file still exists before processing (could be deleted externally)
        If !FileExist(folderPath "\" filename) {
             ; FileList.Delete(filename) ; Remove from internal list (optional)
             continue ; Skip this file
        }

        SplitPath, filename, , , FileExt
        FileBase := SubStr(filename, 1, InStr(filename, "." . FileExt, false, 0) - 1) ; Use InStr with 0 offset for end search
        if (FileBase = "" and FileExt = filename) { ; Handle files with no extension
            FileBase := filename
            FileExt := ""
        }

        NewName := ""
        NewBase := "" ; Initialize NewBase

        If (mode = "ADD")
        { ; Brace for If mode = ADD
            If (PlaceFront)
                NewName := InputText . filename
            Else If (PlaceEnd)
                NewName := FileBase . InputText . (FileExt ? "." . FileExt : "")
            Else If (PlaceBoth)
                NewName := InputText . FileBase . InputText . (FileExt ? "." . FileExt : "")
        } ; Brace for If mode = ADD
        Else If (mode = "REMOVE")
        { ; Brace for Else If mode = REMOVE
            TempBase := FileBase ; Work on a temporary copy
            If (CaseSensitive) {
                StringReplace, NewBase, TempBase, %InputText%, , All ; Case sensitive replace with nothing
            } Else {
                StringCaseSense, Off
                StringReplace, NewBase, TempBase, %InputText%, , All ; Case insensitive replace with nothing
                StringCaseSense, On
            }
            ; Only form NewName if Base actually changed
            if (NewBase != FileBase)
                 NewName := NewBase . (FileExt ? "." . FileExt : "")
            else
                 NewName := filename ; No change needed

        } ; Brace for Else If mode = REMOVE
        Else If (mode = "REPLACE")
        { ; Brace for Else If mode = REPLACE
            TempBase := FileBase
            if (InputText = "") { ; Avoid infinite loop if replacing nothing
                NewName := filename ; No change possible
                continue
            }

            If (CaseSensitive) {
                 StringReplace, NewBase, TempBase, %InputText%, %ReplacementText%, All
            } Else {
                 ; Case-insensitive replacement using RegEx for robustness
                 NewBase := RegExReplace(TempBase, "i)" . RegExEscape(InputText), ReplacementText)
            }
             ; Only form NewName if Base actually changed
            if (NewBase != FileBase)
                 NewName := NewBase . (FileExt ? "." . FileExt : "")
            else
                 NewName := filename ; No change needed
        } ; Brace for Else If mode = REPLACE

        ; Rename the file if NewName was formed and is different from current name
        If (NewName != "" && NewName != filename)
        { ; Brace for If NewName != filename
            FileMove, % folderPath "\" filename, % folderPath "\" NewName
            If ErrorLevel
            { ; Brace for If ErrorLevel
                MsgBox, 48, Error, Failed to rename: %filename%`nTo: %NewName%`nError Code: %ErrorLevel%
                newFileQueue.Push(filename) ; Keep old filename in queue if rename failed
                errorCount++
            } ; Brace for If ErrorLevel
             Else
            { ; Brace for Else (ErrorLevel=0)
                newFileQueue.Push(NewName)  ; Store new filename if rename succeeded
                FileList.Delete(filename)   ; Remove old filename from FileList
                FileList[NewName] := true   ; Update FileList with new filename state
                processedCount++
            } ; Brace for Else (ErrorLevel=0)
        } ; Brace for If NewName != filename
         Else
        { ; Brace for Else (NewName == filename)
            newFileQueue.Push(filename)   ; Keep filename if no change was needed or possible
        } ; Brace for Else (NewName == filename)
    } ; Closing Brace for For loop

    ; Update FileQueue with potentially new filenames
    FileQueue := newFileQueue

    MsgBox, 64, Success, File renaming completed.`n%processedCount% files renamed.`n%errorCount% errors.
Return
} ; Closing Brace for ProcessFiles function