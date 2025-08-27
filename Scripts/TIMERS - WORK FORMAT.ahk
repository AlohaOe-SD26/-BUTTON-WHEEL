; Auto-generated TIMERS - WORK FORMAT script - Created by Nick Robinson
; Modified to include dynamic tray icon tooltips

#NoEnv
#SingleInstance, Off
#Persistent
SetWorkingDir %A_ScriptDir%

; Set the initial tooltip for the tray icon
Menu, Tray, Tip, Timer Menu

; Global variables
Global Button1, Button2, Button3, Button4, Button5
Global countdown10 := 0
Global countdown30 := 0
Global countdownCustom := 0
Global currentTimer10 := 0
Global currentTimer30 := 0
Global currentTimerCustom := 0
Global Timer10Label
Global Timer10Display
Global Timer30Label
Global Timer30Display
Global CustomTimerLabel
Global CustomTimerDisplay
Global MoveCarDisplay
Global EndTime
Global CustomName
Global CustomHours
Global CustomMinutes
Global CustomSeconds

; Create Menu GUI function
ShowMenu() {
    ; Reset tooltip only if no timers are currently running
    If !(WinExist("Timer10") || WinExist("Timer30") || WinExist("TimerCustom") || WinExist("MoveCar"))
        Menu, Tray, Tip, Timer Menu

    Gui, Menu:New
    Gui, Menu:+AlwaysOnTop
    Gui, Menu:Add, Button, x10 y10 w0 h0 vButton1 Hidden gDummyButton, Hidden
    Gui, Menu:Add, Button, x10 y10 w200 h50 vButton2 gStart10MinBreak, 10 MINUTE BREAK
    Gui, Menu:Add, Button, x10 y70 w200 h50 vButton3 gStart30MinBreak, 30 MINUTE BREAK
    Gui, Menu:Add, Button, x10 y130 w200 h50 vButton4 gStartMoveCar, MOVE CAR
    Gui, Menu:Add, Button, x10 y190 w200 h50 vButton5 gShowCustomTimer, CUSTOM TIMER
    Gui, Menu:Show, w220 h250, Timer Menu
}

ShowMenu()

; Add new Custom Timer GUI function
ShowCustomTimer() {
    Gui, Menu:Destroy
    Gui, Custom:New
    Gui, Custom:+AlwaysOnTop
    Gui, Custom:Add, Text, x10 y10, Timer Name:
    Gui, Custom:Add, Edit, x10 y30 w200 vCustomName
    Gui, Custom:Add, Text, x10 y60, Hours:
    Gui, Custom:Add, Edit, x10 y80 w60 vCustomHours Number
    Gui, Custom:Add, Text, x80 y60, Minutes:
    Gui, Custom:Add, Edit, x80 y80 w60 vCustomMinutes Number
    Gui, Custom:Add, Text, x150 y60, Seconds:
    Gui, Custom:Add, Edit, x150 y80 w60 vCustomSeconds Number
    Gui, Custom:Add, Button, x10 y120 w95 h30 gStartCustomTimer, START
    Gui, Custom:Add, Button, x115 y120 w95 h30 gCancelCustomTimer, CANCEL
    Gui, Custom:Show, w220 h160, Custom Timer
}

StartCustomTimer() {
    Gui, Custom:Submit
    if (CustomName = "") {
        MsgBox, Please enter a timer name!
        return
    }

    ; Convert empty or invalid inputs to 0
    if (CustomHours = "" || !CustomHours)
        CustomHours := 0
    if (CustomMinutes = "" || !CustomMinutes)
        CustomMinutes := 0
    if (CustomSeconds = "" || !CustomSeconds)
        CustomSeconds := 0

    ; Calculate total seconds
    totalSeconds := (CustomHours * 3600) + (CustomMinutes * 60) + CustomSeconds

    ; Check if at least some time was specified
    if (totalSeconds <= 0) {
        MsgBox, Please enter a duration greater than 0!
        ; Don't destroy the GUI here, let the user correct the input
        ; ShowCustomTimer() ; No need to call this again
        return
    }

    Gui, Custom:Destroy
    StartCustomCountdown(totalSeconds, CustomName)
}

CancelCustomTimer() {
    Gui, Custom:Destroy
    ; Tooltip will be reset by ShowMenu if no other timers are running
    ShowMenu()
}

StartCustomCountdown(duration, labelText) {
    Global countdownCustom := duration
    Global currentTimerCustom := 1

    ; Set the tray icon tooltip to the custom timer name
    Menu, Tray, Tip, %labelText%

    WindowWidth := 87
    WindowHeight := 35
    ScreenWidth := A_ScreenWidth
    ScreenHeight := A_ScreenHeight
    WindowX := ScreenWidth - WindowWidth - 335  ; Same as MoveCar for now
    WindowY := ScreenHeight - WindowHeight - 38  ; Same as MoveCar for now

    Gui, TimerCustom:+AlwaysOnTop -Caption +ToolWindow +E0x20 +Owner
    Gui, TimerCustom:Font, s9 Bold, Arial
    Gui, TimerCustom:Add, Text, x10 y0 vCustomTimerLabel, %labelText% :
    Gui, TimerCustom:Add, Text, x25 y16 h13 w60 vCustomTimerDisplay

    hours := Floor(duration / 3600)
    minutes := Floor(Mod(duration, 3600) / 60)
    seconds := Mod(duration, 60)
    TimeString := Format("{:02}:{:02}:{:02}", hours, minutes, seconds)

    GuiControl, TimerCustom:, CustomTimerDisplay, %TimeString%
    Gui, TimerCustom:Show, x%WindowX% y%WindowY% w%WindowWidth% h%WindowHeight%, TimerCustom
    WinSet, Transparent, 100, TimerCustom
    WinSet, ExStyle, +0x8000000, TimerCustom

    SetTimer, UpdateCustomTimer, 1000
    SetTimer, EnsureOnTopCustom, 1000
}

UpdateCustomTimer:
if (countdownCustom > 0) {
    countdownCustom--

    ; --- Existing logic for popups and color changes ---
    if (currentTimerCustom = 1 && countdownCustom = 300) {
        ShowPopup("5 MINUTES LEFT", "Yellow", 21)
        currentTimerCustom := 2
        GuiControl, TimerCustom:, CustomTimerDisplay, 05:00
        GuiControl, TimerCustom:+cOrange, CustomTimerDisplay
    }
    else if (currentTimerCustom = 2 && countdownCustom = 120) {
        currentTimerCustom := 3
        GuiControl, TimerCustom:, CustomTimerDisplay, 02:00
        GuiControl, TimerCustom:+cRed, CustomTimerDisplay
    }
    else if (currentTimerCustom = 3 && countdownCustom = 60) {
        ShowPopup("1 MINUTE LEFT", "Yellow", 21)
    }
    ; --- End of existing logic ---

    hours := Floor(countdownCustom / 3600)
    minutes := Floor(Mod(countdownCustom, 3600) / 60)
    seconds := Mod(countdownCustom, 60)

    if (hours > 0)
        TimeString := Format("{:02}:{:02}:{:02}", hours, minutes, seconds)
    else
        TimeString := Format("{:02}:{:02}", minutes, seconds)

    GuiControl, TimerCustom:, CustomTimerDisplay, %TimeString%
}
else if (countdownCustom = 0) {
    Gui, TimerCustom:Destroy
    SetTimer, UpdateCustomTimer, Off
    SetTimer, EnsureOnTopCustom, Off
    ; Reset tooltip if no other timers are running
    If !(WinExist("Timer10") || WinExist("Timer30") || WinExist("MoveCar"))
        Menu, Tray, Tip, Timer Menu
}
Return

EnsureOnTopCustom:
WinSet, AlwaysOnTop, On, TimerCustom
Return

#If WinActive("Timer Menu")
Escape::
Gui, Menu:Destroy
; Closing the menu doesn't stop timers, so don't reset the tooltip here
Return
#If

DummyButton:
Return

Start10MinBreak:
Gui, Menu:Destroy
StartTimer10(600, "10") ; Duration 600 seconds = 10 minutes
Return

Start30MinBreak:
Gui, Menu:Destroy
StartTimer30(1800, "30") ; Duration 1800 seconds = 30 minutes
Return

StartMoveCar:
Gui, Menu:Destroy
StartMoveCarTimer()
Return

StartTimer10(duration, labelText) {
    Global countdown10 := duration
    Global currentTimer10 := 1

    ; Set the tray icon tooltip
    Menu, Tray, Tip, 10 MINUTE BREAK

    WindowWidth := 87
    WindowHeight := 35
    ScreenWidth := A_ScreenWidth
    ScreenHeight := A_ScreenHeight
    WindowX := ScreenWidth - WindowWidth - 515
    WindowY := ScreenHeight - WindowHeight - 38

    Gui, Timer10:+AlwaysOnTop -Caption +ToolWindow +E0x20 +Owner
    Gui, Timer10:Font, s9 Bold, Arial
    Gui, Timer10:Add, Text, x10 y0 vTimer10Label, %labelText% ENDS IN:
    Gui, Timer10:Add, Text, x25 y16 vTimer10Display, % Format("{:02}:00", duration/60)
    Gui, Timer10:Show, x%WindowX% y%WindowY% w%WindowWidth% h%WindowHeight%, Timer10
    WinSet, Transparent, 100, Timer10
    WinSet, ExStyle, +0x8000000, Timer10

    SetTimer, UpdateTimer10, 1000
    SetTimer, EnsureOnTop10, 1000
}

StartTimer30(duration, labelText) {
    Global countdown30 := duration
    Global currentTimer30 := 1

    ; Set the tray icon tooltip
    Menu, Tray, Tip, 30 MINUTE BREAK

    WindowWidth := 87
    WindowHeight := 35
    ScreenWidth := A_ScreenWidth
    ScreenHeight := A_ScreenHeight
    WindowX := ScreenWidth - WindowWidth - 425
    WindowY := ScreenHeight - WindowHeight - 38

    Gui, Timer30:+AlwaysOnTop -Caption +ToolWindow +E0x20 +Owner
    Gui, Timer30:Font, s9 Bold, Arial
    Gui, Timer30:Add, Text, x10 y0 vTimer30Label, %labelText% ENDS IN:
    Gui, Timer30:Add, Text, x25 y16 vTimer30Display, % Format("{:02}:00", duration/60)
    Gui, Timer30:Show, x%WindowX% y%WindowY% w%WindowWidth% h%WindowHeight%, Timer30
    WinSet, Transparent, 100, Timer30
    WinSet, ExStyle, +0x8000000, Timer30

    SetTimer, UpdateTimer30, 1000
    SetTimer, EnsureOnTop30, 1000
}

UpdateTimer10:
if (countdown10 > 0) { ; Check if greater than 0 before decrementing
    countdown10--

    ; --- Existing logic for popups and color changes ---
    if (currentTimer10 = 1 && countdown10 = 300) {
        ShowPopup("5 MINUTES LEFT OF BREAK", "Yellow", 21)
        ; countdown10 := 300 ; No need to reset countdown here, let it continue
        currentTimer10 := 2
        GuiControl, Timer10:, Timer10Display, 05:00
        GuiControl, Timer10:+cOrange, Timer10Display
        ; Return ; Don't return, allow timer update below
    }
    else if (currentTimer10 = 2 && countdown10 = 120) {
        ; countdown10 := 120 ; No need to reset countdown here
        currentTimer10 := 3
        GuiControl, Timer10:, Timer10Display, 02:00
        GuiControl, Timer10:+cRed, Timer10Display
        ; Return ; Don't return, allow timer update below
    }
    else if (currentTimer10 = 3 && countdown10 = 60) {
        ShowPopup("1 MINUTE LEFT OF BREAK", "Yellow", 21)
    }
    else if (currentTimer10 = 3 && countdown10 = 30) { ; Changed from == 30 to <= 30 to ensure it fires once
        ShowPopup("BREAK IS OVER! CLOCK BACK IN!", "Red", 27)
        currentTimer10 := 4 ; Prevent firing again
    }
    ; --- End of existing logic ---

    ; Update display only if countdown > 0
    if (countdown10 > 0) {
        minutes := Floor(countdown10 / 60)
        seconds := Mod(countdown10, 60)
        TimeString := Format("{:02}:{:02}", minutes, seconds)
        GuiControl, Timer10:, Timer10Display, %TimeString%
    }
}

if (countdown10 <= 0) { ; Use <= 0 to catch the final state
    Gui, Timer10:Destroy
    SetTimer, UpdateTimer10, Off
    SetTimer, EnsureOnTop10, Off
    ; Reset tooltip if no other timers are running
    If !(WinExist("Timer30") || WinExist("TimerCustom") || WinExist("MoveCar"))
        Menu, Tray, Tip, Timer Menu
    Return ; Exit the subroutine
}
Return ; Continue timer update

UpdateTimer30:
if (countdown30 > 0) { ; Check if greater than 0 before decrementing
    countdown30--

    ; --- Existing logic for popups and color changes ---
    if (countdown30 = 900) {
        ShowPopup("15 MINUTES LEFT", "Yellow", 21)
    }
    else if (currentTimer30 = 1 && countdown30 = 300) {
        ShowPopup("5 MINUTES LEFT OF BREAK", "Yellow", 21)
        ; countdown30 := 300 ; No need to reset countdown here
        currentTimer30 := 2
        GuiControl, Timer30:, Timer30Display, 05:00
        GuiControl, Timer30:+cOrange, Timer30Display
        ; Return ; Don't return
    }
    else if (currentTimer30 = 2 && countdown30 = 120) {
        ; countdown30 := 120 ; No need to reset countdown here
        currentTimer30 := 3
        GuiControl, Timer30:, Timer30Display, 02:00
        GuiControl, Timer30:+cRed, Timer30Display
        ; Return ; Don't return
    }
    else if (currentTimer30 = 3 && countdown30 = 60) {
        ShowPopup("1 MINUTE LEFT OF BREAK", "Yellow", 21)
    }
    else if (currentTimer30 = 3 && countdown30 <= 30) { ; Changed from == 30 to <= 30
        ShowPopup("BREAK IS OVER! CLOCK BACK IN!", "Red", 27)
        currentTimer30 := 4 ; Prevent firing again
    }
     ; --- End of existing logic ---

    ; Update display only if countdown > 0
    if (countdown30 > 0) {
        minutes := Floor(countdown30 / 60)
        seconds := Mod(countdown30, 60)
        TimeString := Format("{:02}:{:02}", minutes, seconds)
        GuiControl, Timer30:, Timer30Display, %TimeString%
    }
}

if (countdown30 <= 0) { ; Use <= 0 to catch the final state
    Gui, Timer30:Destroy
    SetTimer, UpdateTimer30, Off
    SetTimer, EnsureOnTop30, Off
    ; Reset tooltip if no other timers are running
    If !(WinExist("Timer10") || WinExist("TimerCustom") || WinExist("MoveCar"))
        Menu, Tray, Tip, Timer Menu
    Return ; Exit the subroutine
}
Return ; Continue timer update

EnsureOnTop10:
WinSet, AlwaysOnTop, On, Timer10
Return

EnsureOnTop30:
WinSet, AlwaysOnTop, On, Timer30
Return

StartMoveCarTimer() {
    ; Set the tray icon tooltip
    Menu, Tray, Tip, MOVE CAR

    WindowWidth := 87
    WindowHeight := 35
    ScreenWidth := A_ScreenWidth
    ScreenHeight := A_ScreenHeight
    WindowX := ScreenWidth - WindowWidth - 335
    WindowY := ScreenHeight - WindowHeight - 38

    StartTime := A_TickCount
    Global EndTime := StartTime + (110 * 60 * 1000)  ; 1 hour 50 minutes

    Gui, MoveCar:+AlwaysOnTop -Caption +ToolWindow +E0x20 +Owner
    Gui, MoveCar:Font, s9 Bold, Arial
    Gui, MoveCar:Add, Text, x10 y0, MOVE CAR IN:
    Gui, MoveCar:Add, Text, x25 y16 vMoveCarDisplay, 01:50:00
    Gui, MoveCar:Show, x%WindowX% y%WindowY% w%WindowWidth% h%WindowHeight%, MoveCar
    WinSet, Transparent, 100, MoveCar
    WinSet, ExStyle, +0x8000000, MoveCar

    SetTimer, UpdateMoveCarTimer, 1000
    SetTimer, EnsureOnTopCar, 1000 ; Changed from 10ms to 1000ms (1s) - less resource intensive
}

UpdateMoveCarTimer:
TimeLeft := EndTime - A_TickCount
if (TimeLeft <= 0) {
    Gui, MoveCar:Destroy
    ShowPopup("TIME TO MOVE CAR!", "Black", 24)
    SetTimer, UpdateMoveCarTimer, Off
    SetTimer, EnsureOnTopCar, Off
    ; Reset tooltip if no other timers are running
    If !(WinExist("Timer10") || WinExist("Timer30") || WinExist("TimerCustom"))
        Menu, Tray, Tip, Timer Menu
    Return
}
Hours := Floor(TimeLeft / 3600000)
Minutes := Mod(Floor(TimeLeft / 60000), 60)
Seconds := Mod(Floor(TimeLeft / 1000), 60)
TimeString := Format("{:02}:{:02}:{:02}", Hours, Minutes, Seconds)
GuiControl, MoveCar:, MoveCarDisplay, %TimeString%
Return

EnsureOnTopCar:
WinSet, AlwaysOnTop, On, MoveCar
Return

ShowPopup(message, color, fontSize) {
    Gui, Popup:+AlwaysOnTop -Caption +ToolWindow ; Added +ToolWindow to prevent showing in taskbar
    Gui, Popup:Font, s%fontSize% Bold
    Gui, Popup:Color, %color%
    ; Calculate text width to potentially adjust GUI width (optional, but good practice)
    ; Gui, Popup:Add, Text, Center vPopupText, %message%
    ; GuiControlGet, PopupText, Popup:Pos
    ; GuiWidth := PopupTextW + 40 ; Add some padding
    ; if (GuiWidth < 300) ; Ensure minimum width
    ;     GuiWidth := 300
    Gui, Popup:Add, Text, Center, %message%
    Gui, Popup:Show, Center w600 h300, Popup ; Keeping original size for now
    if (color = "Red")
        WinSet, Transparent, 200, A
    Sleep, 3000
    Gui, Popup:Destroy
    Return
}

; --- Optional: Handle script exit ---
OnExit("ExitCleanup")

ExitCleanup(ExitReason, ExitCode)
{
    ; Perform any necessary cleanup before exiting
    ExitApp ; Ensures the script terminates properly
}

MenuGuiClose:
MenuGuiEscape:
Gui, Menu:Destroy
; No tooltip reset here, as timers might still be running
Return
