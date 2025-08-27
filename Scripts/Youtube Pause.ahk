
; Auto-generated YOUTUBE PAUSE - PAUSE BUTTON script - Created by ButtonWheel Python Script

; Set the coordinate mode to screen relative to the active window initially
CoordMode, Mouse, Screen

; Define variables to store the selected click location and the original mouse location
global ClickX := 245 ; Default X
global ClickY := 103 ; Default Y
global OriginalX := 0
global OriginalY := 0

; Hotkey to select the click location (Alt+*)
!*::
{
    MouseGetPos, ClickX, ClickY
    MsgBox, Click location set to: %ClickX%, %ClickY%
    return
}

; Function to perform the volume up, volume down, and click sequence
PerformSequence()
{
    global ClickX, ClickY, OriginalX, OriginalY

    ; Store original mouse position
    MouseGetPos, OriginalX, OriginalY

    ; Increase volume by 1 step (or specific key if needed)
    Send {Volume_Up}
    Sleep, 50 ; Short delay

    ; Decrease volume by 1 step
    Send {Volume_Down}
    Sleep, 50 ; Short delay

    ; Move mouse to the saved location, click, and move back
    ; Using BlockInput to potentially make mouse movements more reliable
    ; BlockInput, MouseMove
    MouseMove, %ClickX%, %ClickY%, 0 ; Move instantly
    Sleep, 30 ; Slight pause before click
    Click
    Sleep, 50 ; Wait briefly after click
    MouseMove, %OriginalX%, %OriginalY%, 0 ; Move back instantly
    ; BlockInput, Off
    return
}

; Hotkeys to perform the sequence
; Using #IfWinActive ahk_class Chrome_WidgetWin_1 might restrict too much,
; keep it global for now unless specific window targeting is needed.

; Hotkey: Backtick ` (change if needed)
; `::
; PerformSequence()
; return

; Hotkey: Pause/Break key
Pause::
PerformSequence()
return
