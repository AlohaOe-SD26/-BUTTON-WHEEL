; Auto-generated FILE NAME ADD + REMOVE - WORK FORMAT script - Created by Nick Robinson

#Persistent

; Initialize variables
global SelectedFolder := ""
global FileList := {}  ; Object to store all files and their states
global FileQueue := [] ; Array to store files to be processed

; Select Folder Button
Gui, Add, Button, x10 y10 w75 gSelectFolder, Select Folder

; Text input fields
Gui, Add, Text, x10 y63, Enter text to modify file names:
Gui, Add, Edit, x10 y80 vInputText w185, ; Original input field
Gui, Add, Text, x10 y105 vReplaceLabel, Enter replacement text:
Gui, Add, Edit, x10 y123 vReplacementText w185 Disabled, ; Initially disabled

; Mode - Action Selection
Gui, Add, GroupBox, x10 y150 w90 h80, Mode
Gui, Add, Radio, x20 y170 w40 vModeAdd gProcessModeChange Checked, ADD
Gui, Add, Radio, x20 y190 w40 vModeRemove gProcessModeChange, REMOVE
Gui, Add, Radio, x20 y210 w30 vModeReplace gProcessModeChange, REPLACE

; Placement options
Gui, Add, GroupBox, x105 y150 w90 h80, Placement
Gui, Add, Radio, x115 y170 w70 vPlaceFront gHandlePlacement Checked, FRONT
Gui, Add, Radio, x115 y190 w70 vPlaceEnd gHandlePlacement, END
Gui, Add, Radio, x115 y210 w70 vPlaceBoth gHandlePlacement, BOTH

; Case sensitivity toggle (always visible but initially disabled)
Gui, Add, GroupBox, x10 y230 w185 h40 vCaseGroup, Case Sensitivity
Gui, Add, CheckBox, x20 y250 vCaseSensitive Disabled, CASE SENSITIVE?

; MODE OPTION 2 - File Selection
Gui, Add, GroupBox, x10 y340 w360 h60, MODE OPTION 2
Gui, Add, CheckBox, x90 y11 w80 h13 vSpecificFiles gToggleSpecificFiles Disabled, Specific Files
Gui, Add, Button, x10 y35 w75 vSelectFilesButton gSelectFiles Disabled, Select Files
Gui, Add, Text, x90 y32 h10 vHelpText1 Hidden, Select specific files to
Gui, Add, Text, x90 y46 h10 vHelpText2 Hidden, modify their names.

; Action buttons
Gui, Add, Button, x10 y275 w90 gStartScript, START
Gui, Add, Button, x105 y275 w90 gExitScript, Exit

Gui, Show, w205 h304, File Renaming Tool

; Set initial state for replacement text label since we start in ADD mode
GuiControl, Disable, ReplaceLabel

Return

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

; Update FileList and FileQueue based on folder selection
UpdateFileList(setAllTrue := true) {
    global FileList, FileQueue, SelectedFolder
    FileList := {}  ; Clear existing file list
    FileQueue := [] ; Clear existing queue

    ; Populate FileList with all files in the folder
    Loop, Files, %SelectedFolder%\*.*
    {
        FileList[A_LoopFileName] := setAllTrue  ; Set initial toggle state
        if (setAllTrue)
            FileQueue.Push(A_LoopFileName)      ; Add to queue if TRUE
    }
}

; Handle folder selection
SelectFolder:
    FileSelectFolder, SelectedFolder, , 3, Select a folder:
    If (SelectedFolder != "") {
        GuiControl, Enable, SpecificFiles
        GuiControl,, SpecificFiles, 0  ; Uncheck the box
        ; SelectFilesButton remains disabled until SpecificFiles is checked
        UpdateFileList(true)  ; Initialize with all files set to TRUE
    }
Return

; Handle Specific Files checkbox toggle
ToggleSpecificFiles:
    Gui, Submit, NoHide
    if (SpecificFiles) {
        GuiControl, Enable, SelectFilesButton
        GuiControl, Show, HelpText1    ; Show first help text when enabled
        GuiControl, Show, HelpText2    ; Show second help text when enabled
        UpdateFileList(false)  ; Set all files to FALSE when enabling specific selection
    } else {
        GuiControl, Disable, SelectFilesButton
        GuiControl, Hide, HelpText1    ; Hide first help text when disabled
        GuiControl, Hide, HelpText2    ; Hide second help text when disabled
        UpdateFileList(true)   ; Set all files to TRUE when disabling specific selection
    }
Return

; Handle file selection
SelectFiles:
    If (SelectedFolder = "") {
        MsgBox, 48, Error, Please select a folder first.
        Return
    }

    FileSelectFile, SelectedFiles, M3, %SelectedFolder%, Select specific files:, All Files (*.*)
    If (SelectedFiles != "") {
        FileQueue := []  ; Clear existing queue
        ; Parse selected files
        Loop, Parse, SelectedFiles, 

        {
            if (A_Index = 1)  ; Skip first line (contains directory)
                continue
            if (A_LoopField = "")  ; Skip empty lines
                continue

            ; Set selected files to TRUE and add to queue
            FileList[A_LoopField] := true
            FileQueue.Push(A_LoopField)
        }
        MsgBox, % "Selected " . FileQueue.Length() . " files for processing"
    }
Return

; Start script logic
StartScript:
    Gui, Submit, NoHide
    If (InputText = "") {
        MsgBox, 48, Error, Please enter text to modify file names.
        Return
    }
    If (ModeReplace && ReplacementText = "") {
        MsgBox, 48, Error, Please enter replacement text.
        Return
    }
    If (SelectedFolder = "") {
        MsgBox, 48, Error, Please select a folder.
        Return
    }
    If (FileQueue.Length() = 0) {
        MsgBox, 48, Error, No files in queue for processing.
        Return
    }

    ; Process files
    If (ModeAdd) ; ADD Mode
        ProcessFiles("ADD")
    Else If (ModeRemove) ; REMOVE Mode
        ProcessFiles("REMOVE")
    Else ; REPLACE Mode
        ProcessFiles("REPLACE")
Return

; Helper function to escape RegEx special characters
RegExEscape(String) {
    Return RegExReplace(String, "[\.\*\?\+\[\{\|\(\)\^\$\\]", "\$0")
}

; Process file renaming
ProcessFiles(mode) {
    global FileQueue, FileList, SelectedFolder, InputText, ReplacementText, PlaceFront, PlaceEnd, PlaceBoth, CaseSensitive

    ; Keep track of successful renames to update queue
    newFileQueue := []

    ; Process only files in the FileQueue
    for index, filename in FileQueue {
        SplitPath, filename, , , FileExt
        FileBase := SubStr(filename, 1, InStr(filename, "." . FileExt) - 1)
        NewName := ""

        If (mode = "ADD") {
            If (PlaceFront) ; FRONT
                NewName := InputText . filename
            Else If (PlaceEnd) ; END
                NewName := FileBase . InputText . "." . FileExt
            Else If (PlaceBoth) ; BOTH
                NewName := InputText . FileBase . InputText . "." . FileExt
        }
        Else If (mode = "REMOVE") {
            If (CaseSensitive) {
                ; Case sensitive removal
                NewBase := ""
                StartPos := 1
                While (FoundPos := InStr(FileBase, InputText, true, StartPos)) {
                    NewBase .= SubStr(FileBase, StartPos, FoundPos - StartPos)
                    StartPos := FoundPos + StrLen(InputText)
                }
                If (StartPos <= StrLen(FileBase))
                    NewBase .= SubStr(FileBase, StartPos)
                FileBase := NewBase != "" ? NewBase : FileBase
            } Else {
                StringCaseSense, Off
                StringReplace, FileBase, FileBase, %InputText%, , All
                StringCaseSense, On
            }
            NewName := FileBase . "." . FileExt
        }
        Else If (mode = "REPLACE") {
            If (CaseSensitive) {
                ; Case sensitive exact replacement
                NewBase := ""
                StartPos := 1
                While (FoundPos := InStr(FileBase, InputText, true, StartPos)) {
                    NewBase .= SubStr(FileBase, StartPos, FoundPos - StartPos)
                    NewBase .= ReplacementText ; Exact replacement from REPLACEMENT field
                    StartPos := FoundPos + StrLen(InputText)
                }
                If (StartPos <= StrLen(FileBase))
                    NewBase .= SubStr(FileBase, StartPos)
                FileBase := NewBase != "" ? NewBase : FileBase
            } Else {
                ; Case insensitive exact replacement
                NewBase := ""
                StartPos := 1
                pos := 1
                ; Loop through the string looking for matches
                While (pos := RegExMatch(FileBase, "i)" . RegExEscape(InputText), match, pos)) {
                    ; Add text before match plus exact replacement text
                    NewBase .= SubStr(FileBase, StartPos, pos - StartPos) . ReplacementText
                    StartPos := pos + StrLen(match)
                    pos := StartPos
                }
                ; Add remaining text
                If (StartPos <= StrLen(FileBase))
                    NewBase .= SubStr(FileBase, StartPos)
                FileBase := NewBase != "" ? NewBase : FileBase
            }
            NewName := FileBase . "." . FileExt
        }

        ; Rename the file if we have a new name and it's different from current name
        If (NewName != "") {
            FileMove, % SelectedFolder "\" filename, % SelectedFolder "\" NewName
            If ErrorLevel {
                MsgBox, 48, Error, Failed to rename: %filename%
                newFileQueue.Push(filename)  ; Keep old filename if rename failed
            } Else {
                newFileQueue.Push(NewName)   ; Store new filename if rename succeeded
                FileList[NewName] := true    ; Update FileList with new filename
                FileList.Delete(filename)    ; Remove old filename from FileList
            }
        } Else {
            newFileQueue.Push(filename)      ; Keep filename if no change needed
        }
    }

    ; Update FileQueue with new filenames
    FileQueue := newFileQueue

    MsgBox, 64, Success, File renaming completed.
Return
}

Esc::ExitApp

ExitScript:
    ExitApp
Return