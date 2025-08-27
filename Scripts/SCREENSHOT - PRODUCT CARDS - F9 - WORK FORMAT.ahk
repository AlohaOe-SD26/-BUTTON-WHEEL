; Auto-generated SCREENSHOT - PRODUCT CARDS - F9 - WORK FORMAT script - Created by Nick Robinson

#NoEnv
#SingleInstance force
SendMode Input
SetWorkingDir %A_ScriptDir%

; Show GUI on script launch
ShowScreenshotGui()

ShowScreenshotGui() {
    global
    Gui, 1:New, +AlwaysOnTop, Screenshot Select
    Gui, Add, Button, x-100 y-100 w1 h1 vBtn1, Hidden
    Gui, Add, Button, x10 y10 w140 h30 gScreenshotFunction vBtn2, PRODUCT CARD
    Gui, Add, Button, x10 y50 w140 h30 gScreenshotFunction vBtn3, CURRENT WINDOW
    Gui, Add, Button, x10 y90 w140 h30 gScreenshotFunction vBtn4, ENTIRE SCREEN
    Gui, Show, w160 h130
}

ScreenshotFunction:
    GuiControlGet, ctrl, FocusV
    if (ctrl = "Btn2" || ctrl = "Btn3" || ctrl = "Btn4") {
        Gui, Submit
        Gui, Destroy
        Sleep, 100
        if (ctrl = "Btn2")
            ProductCardFunction()
        else if (ctrl = "Btn3")
            CurrentWindowFunction()
        else if (ctrl = "Btn4")
            EntireScreenFunction()
    }
return

ProductCardFunction() {
    Run, C:\Windows\System32\SnippingTool.exe
    Sleep, 300
    Send, !m
    Sleep, 200
    Send, r
    Sleep, 500
    CoordMode, Mouse, Screen
    MouseMove, 410, 370
    Sleep, 50
    MouseClick, left, 410, 370, 1, 0, D
    Sleep, 50
    MouseMove, 1562, 929, 0
    Sleep, 50
    MouseClick, left, 1562, 929, 1, 0, U
    Sleep, 100
    Send, ^s
    Sleep, 300
    WaitForSaveDialog()
    CloseSnippingTool()
    ShowScreenshotGui()
}

CurrentWindowFunction() {
    Run, C:\Windows\System32\SnippingTool.exe
    Sleep, 300
    Send, !m
    Sleep, 200
    Send, w
    Sleep, 200
    KeyWait, LButton, D
    Sleep, 300
    Send, ^s
    Sleep, 300
    WaitForSaveDialog()
    CloseSnippingTool()
    ShowScreenshotGui()
}

EntireScreenFunction() {
    Run, C:\Windows\System32\SnippingTool.exe
    Sleep, 300
    Send, !m
    Sleep, 200
    Send, s
    Sleep, 200
    Send, ^s
    Sleep, 300
    WaitForSaveDialog()
    CloseSnippingTool()
    ShowScreenshotGui()
}

WaitForSaveDialog() {
    ; Wait until the Save As dialog appears
    WinWait, Save As
    ; Wait until the Save As dialog closes (indicating the file was saved)
    WinWaitClose, Save As
}

CloseSnippingTool() {
    Sleep, 200
    Process, Close, SnippingTool.exe
    Sleep, 100
}

Esc::
    CloseSnippingTool()
    ExitApp
