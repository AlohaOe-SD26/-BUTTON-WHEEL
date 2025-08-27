; Auto-generated FLOATING CLIPBOARD - CLUB420 - WORK FORMAT Script - Created by Nick Robinson

#SingleInstance force

; Global variables to track GUI state
global GuiExists := false
global Window_Width := 160
global Window_Height := 500
global Button_Width := 140

; Window coordinates
global Window_TopLeft_X := -4
global Window_TopLeft_Y := 120

; Arrays to store text content
global FSD_Text := []
global H80_Text := []

; Load text content on startup
LoadTextFiles()

; Call the CreateGui function immediately to show the GUI on script launch
CreateGui()

LoadTextFiles() {
    global FSD_Text, H80_Text

    iniPath := A_ScriptDir . "\CLIPBOARD_BUTTON_TEXT_WORK.INI"

    ; Load FSD text
    Loop, 5 {
        IniRead, txtPath, %iniPath%, FilePaths, FSDButton%A_Index%, ERROR
        if (txtPath != "ERROR" && FileExist(txtPath)) {
            FileRead, fileContent, %txtPath%
            if !ErrorLevel
                FSD_Text[A_Index] := fileContent
            else
                FSD_Text[A_Index] := "Error reading file"
        } else {
            FSD_Text[A_Index] := "File not found"
        }
    }

    ; Load H80 text
    Loop, 5 {
        IniRead, txtPath, %iniPath%, FilePaths, H80Button%A_Index%, ERROR
        if (txtPath != "ERROR" && FileExist(txtPath)) {
            FileRead, fileContent, %txtPath%
            if !ErrorLevel
                H80_Text[A_Index] := fileContent
            else
                H80_Text[A_Index] := "Error reading file"
        } else {
            H80_Text[A_Index] := "File not found"
        }
    }
}

CreateGui() {
    global
    ; Explicitly create GUI 1
    Gui, 1:New, +AlwaysOnTop, Clipboard Manager

    ; Add hidden dummy button that will receive initial focus
    Gui, Add, Button, x-100 y-100 w1 h1 vDummyBtn0, Hidden

    Gui, Font, s15, Bold

    ; Add FSD buttons
    Gui, Font, s12
    Gui, Add, Text, x10 y10, FSD Section
    Gui, Add, Button, x10 y40 w140 h30 gCopyText vFSDBtn1, REGULAR
    Gui, Add, Button, x10 y80 w140 h30 gCopyText vFSDBtn2, END DATE
    Gui, Add, Button, x10 y120 w140 h30 gCopyText vFSDBtn3, LIMITED
    Gui, Add, Button, x10 y160 w140 h30 gCopyText vFSDBtn4, SALE AD
    Gui, Add, Button, x10 y200 w140 h30 gCopyText vFSDBtn5, SALE LIVE

    ; Add H80 buttons below FSD section
    Gui, Add, Text, x10 y250, H80 Section
    Gui, Add, Button, x10 y280 w140 h30 gCopyText vH80Btn1, REGULAR
    Gui, Add, Button, x10 y320 w140 h30 gCopyText vH80Btn2, END DATE
    Gui, Add, Button, x10 y360 w140 h30 gCopyText vH80Btn3, LIMITED
    Gui, Add, Button, x10 y400 w140 h30 gCopyText vH80Btn4, SALE AD
    Gui, Add, Button, x10 y440 w140 h30 gCopyText vH80Btn5, SALE LIVE

    ; Show the GUI at the specified position
    Gui, Show, x%Window_TopLeft_X% y%Window_TopLeft_Y% w%Window_Width% h%Window_Height%, Clipboard Manager
}

; Handle button clicks to copy the formatted text to the clipboard
CopyText:
    Gui, Submit, NoHide
    Loop, 5 {
        GuiControlGet, ctrl, FocusV
        if (InStr(ctrl, "FSDBtn" . A_Index)) {
            Clipboard := FSD_Text[A_Index]
            break
        } else if (InStr(ctrl, "H80Btn" . A_Index)) {
            Clipboard := H80_Text[A_Index]
            break
        }
    }
Return

Esc::ExitApp