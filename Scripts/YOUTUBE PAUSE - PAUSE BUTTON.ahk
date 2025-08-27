; Auto-generated YOUTUBE PAUSE - PAUSE BUTTON script - Created by Nick Robinson

; Set the coordinate mode to screen
CoordMode, Mouse, Screen

; Define variables to store the selected click location and the original mouse location
global ClickX := 245
global ClickY := 103
global OriginalX := 0
global OriginalY := 0

; Hotkey to select the click location
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

    ; Log the current mouse position
    MouseGetPos, OriginalX, OriginalY

    ; Increase volume by 1
    Send {Volume_Up}
    Sleep, 50

    ; Decrease volume by 1
    Send {Volume_Down}
    Sleep, 50

    ; Teleport to the selected location and click
    MouseMove, %ClickX%, %ClickY%, 0
    Click
    Sleep, 50

    ; Teleport back to the original position
    MouseMove, %OriginalX%, %OriginalY%, 0

    return
}

; Hotkeys to perform the sequence
::
PerformSequence()
return

Pause::
PerformSequence()
return
