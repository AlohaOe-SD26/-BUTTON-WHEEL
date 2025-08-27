; Auto-generated AUTO TREEZ 2.5 - WORK FORMAT script - Created by Nick Robinson

#Persistent  ; Keep the script running indefinitely
SetTimer, CheckColor, 500  ; Continuously check for colors every 500ms

; Start Prompt
ShowStartPrompt()
return

; Use ESC to close the script
Esc::ExitApp

ShowStartPrompt() {
; Display the start prompt in the center of the screen
Gui, StartPrompt:New
Gui, StartPrompt:+AlwaysOnTop +ToolWindow
Gui, Font, s12
Gui, Add, Text, Center, BEFORE CONTINUING, MAKE SURE:
Gui, Add, Text, Center, - YOU ARE ON GOOGLE SHEET SCREEN
Gui, Add, Text, Center, - THE NEXT WINDOW IS TREEZ DISCOUNT MANAGEMENT
Gui, Add, Text, Center, WHEN YOU ARE READY TO BEGIN, CLICK THE START BUTTON.
Gui, Add, Button, gStartScript w150 Default, START
Gui, StartPrompt:Show, Center
SetTimer, CheckColor, Off  ; Stop detecting colors while the START prompt is shown
}

StartScript:
; Close the prompt and perform the initial actions
Gui, StartPrompt:Destroy

; Perform initial actions immediately (no delay here)
Send, ^{Home}
Sleep, 500
Click, 101, 982  ; PREP FOR NEXT
Sleep, 500
Send, {Down}

; Add a 600ms delay before enabling color detection
Sleep, 600
SetTimer, CheckColor, 500  ; Resume color detection after delay
return

CheckColor:
; Wait for 500ms before each search to avoid constant looping without delay
Sleep, 500

; Define the screen area to search (left, top, right, bottom)
x1 := 90  ; Example values, adjust according to your needs
y1 := 300
x2 := 110
y2 := 300

; Check for specific colors and run the corresponding sequence
PixelSearch, Px, Py, x1, y1, x2, y2, 0xFF9900, 2, Fast RGB  ; BOGO - Orange
if (!ErrorLevel) {
RunBOGOSequence()
return
}

PixelSearch, Px, Py, x1, y1, x2, y2, 0x00FF00, 2, Fast RGB  ; B2G1 - Green
if (!ErrorLevel) {
RunB2G1Sequence()
return
}

PixelSearch, Px, Py, x1, y1, x2, y2, 0xFFFF00, 2, Fast RGB  ; B1G2 - Yellow
if (!ErrorLevel) {
RunB1G2Sequence()
return
}

PixelSearch, Px, Py, x1, y1, x2, y2, 0x00FFFF, 2, Fast RGB  ; XforX - Cyan
if (!ErrorLevel) {
RunXForSequence()
return
}

PixelSearch, Px, Py, x1, y1, x2, y2, 0x0000FF, 2, Fast RGB  ; %Off - Blue
if (!ErrorLevel) {
RunPercentOffSequence()
return
}

PixelSearch, Px, Py, x1, y1, x2, y2, 0x9900FF, 2, Fast RGB  ; $Off - Purple
if (!ErrorLevel) {
RunDollarOffSequence()
return
}

PixelSearch, Px, Py, x1, y1, x2, y2, 0xFF00FF, 2, Fast RGB  ; Reset - Magenta
if (!ErrorLevel) {
; Detected color FF00FF, restart the script
ShowStartPrompt()  ; Show the start prompt again
return
}

return


RunBOGOSequence() {
Click, 1911, 1003  ; SLIDE RIGHT
Sleep, 300
Click, 380, 306  ; DEAL TITLE
Sleep, 300
Send, ^c
Sleep, 300
Send, !{Tab}
Sleep, 300
Click, 1445, 286  ; NEW DEAL BUTTON
Sleep, 700
Click, 914, 351  ; DISCOUNT TITLE
Sleep, 300
Send, ^v
Sleep, 300
Click, 917, 431  ; DISCOUNT METHOD
Sleep, 300
Click, 879, 521  ; BOGO
Sleep, 300
Send, !{Tab}
Sleep, 300
Click, 105, 306  ; BIN 1 VALUE
Sleep, 100
Send, ^c
Sleep, 100
Send, !{Tab}
Sleep, 300
Click, 1285, 898  ; BIN 1 INPUT
Sleep, 300
Send, ^v
Sleep, 300
Send, {PgDn}
Sleep, 300
Send, {PgDn}
Sleep, 300
Click, 1285, 699  ; BIN 2 INPUT
Sleep, 300
Send, ^v
Sleep, 300
Send, !{Tab}
Sleep, 300
Click, 300, 306  ; DISCOUNT VALUE
Sleep, 100
Send, ^c
Sleep, 100
Send, !{Tab}
Sleep, 300
Click, 1601, 618  ; BOGO DISCOUNT VALUE TYPE
Sleep, 300
Click, 1582, 650  ; BOGO DISCOUNT DOLLAR TYPE
Sleep, 500
Click, 1758, 625  ; BOGO DISCOUNT VALUE
Sleep, 300
Send, ^v
Sleep, 300
Click, 251, 633  ; CLOSE DISCOUNT SCREEN
Sleep, 300
Send, !{Tab}
Sleep, 300
Click, 84, 981  ; PREP FOR NEXT
Sleep, 300
Send, {Down}
Sleep, 300
Send, {Left}
}

RunB2G1Sequence() {
Click, 1911, 1003  ; SLIDE RIGHT
Sleep, 300
Click, 380, 306  ; DEAL TITLE
Sleep, 300
Send, ^c
Sleep, 300
Send, !{Tab}
Sleep, 300
Click, 1445, 286  ; NEW DEAL BUTTON
Sleep, 700
Click, 914, 351  ; DISCOUNT TITLE
Sleep, 300
Send, ^v
Sleep, 300
Click, 917, 431  ; DISCOUNT METHOD
Sleep, 300
Click, 879, 521  ; BOGO
Sleep, 300
Send, !{Tab}
Sleep, 300
Click, 105, 306  ; BIN 1 VALUE
Sleep, 100
Send, ^c
Sleep, 100
Send, !{Tab}
Sleep, 300
Click, 1285, 898  ; BIN 1 INPUT
Sleep, 300
Send, ^v
Sleep, 300
Send, !{Tab}
Sleep, 300
Click, 209, 306  ; BIN 2 VALUE
Sleep, 100
Send, ^c
Sleep, 100
Send, !{Tab}
Sleep, 300
Send, {PgDn}
Sleep, 300
Send, {PgDn}
Sleep, 300
Click, 1285, 699  ; BIN 2 INPUT
Sleep, 300
Send, ^v
Sleep, 300
Send, !{Tab}
Sleep, 300
Click, 300, 306  ; DISCOUNT VALUE
Sleep, 100
Send, ^c
Sleep, 100
Send, !{Tab}
Sleep, 300
Click, 1601, 618  ; BOGO DISCOUNT VALUE TYPE
Sleep, 300
Click, 1582, 650  ; BOGO DISCOUNT DOLLAR TYPE
Sleep, 500
Click, 1758, 625  ; BOGO DISCOUNT VALUE
Sleep, 300
Send, ^v
Sleep, 300
Click, 251, 633  ; CLOSE DISCOUNT SCREEN
Sleep, 300
Send, !{Tab}
Sleep, 300
Click, 84, 981  ; PREP FOR NEXT
Sleep, 300
Send, {Down}
Sleep, 300
Send, {Left}
}

RunB1G2Sequence() {
Click, 1911, 1003  ; SLIDE RIGHT
Sleep, 300
Click, 380, 306  ; DEAL TITLE
Sleep, 300
Send, ^c
Sleep, 300
Send, !{Tab}
Sleep, 300
Click, 1445, 286  ; NEW DEAL BUTTON
Sleep, 700
Click, 914, 351  ; DISCOUNT TITLE
Sleep, 300
Send, ^v
Sleep, 300
Click, 917, 431  ; DISCOUNT METHOD
Sleep, 300
Click, 879, 521  ; BOGO
Sleep, 300
Send, !{Tab}
Sleep, 300
Click, 105, 306  ; BIN 1 VALUE
Sleep, 100
Send, ^c
Sleep, 100
Send, !{Tab}
Sleep, 300
Click, 1285, 898  ; BIN 1 INPUT
Sleep, 300
Send, ^v
Sleep, 300
Send, !{Tab}
Sleep, 300
Click, 209, 306  ; BIN 2 VALUE
Sleep, 100
Send, ^c
Sleep, 100
Send, !{Tab}
Sleep, 300
Send, {PgDn}
Sleep, 300
Send, {PgDn}
Sleep, 300
Click, 1285, 699  ; BIN 2 INPUT
Sleep, 300
Send, ^v
Sleep, 300
Send, !{Tab}
Sleep, 300
Click, 300, 306  ; DISCOUNT VALUE
Sleep, 100
Send, ^c
Sleep, 100
Send, !{Tab}
Sleep, 300
Click, 1601, 618  ; BOGO DISCOUNT VALUE TYPE
Sleep, 300
Click, 1582, 650  ; BOGO DISCOUNT DOLLAR TYPE
Sleep, 500
Click, 1758, 625  ; BOGO DISCOUNT VALUE
Sleep, 300
Send, ^v
Sleep, 300
Click, 251, 633  ; CLOSE DISCOUNT SCREEN
Sleep, 300
Send, !{Tab}
Sleep, 300
Click, 251, 633  ; CLOSE DISCOUNT SCREEN
Sleep, 300
Send, {Down}
Sleep, 300
Send, {Left}
}

RunXForSequence() {
Click, 1911, 1003  ; SLIDE RIGHT
Sleep, 300
Click, 380, 306  ; DEAL TITLE
Sleep, 100
Send, ^c
Sleep, 100
Send, !{Tab}
Sleep, 300
Click, 1445, 286  ; NEW DEAL BUTTON
Sleep, 700
Click, 914, 351  ; DISCOUNT TITLE
Sleep, 300
Send, ^v
Sleep, 300
Click, 917, 431  ; DISCOUNT METHOD
Sleep, 300
Click, 879, 521  ; BOGO
Sleep, 300
Send, !{Tab}
Sleep, 300
Click, 105, 306  ; BIN 1 VALUE
Sleep, 100
Send, ^c
Sleep, 100
Send, !{Tab}
Sleep, 300
Click, 1285, 898  ; BIN 1 INPUT
Sleep, 300
Send, ^v
Sleep, 300
Send, !{Tab}
Sleep, 300
Click, 209, 306  ; BIN 2 VALUE
Sleep, 100
Send, ^c
Sleep, 100
Send, !{Tab}
Sleep, 300
Send, {PgDn}
Sleep, 300
Send, {PgDn}
Sleep, 300
Click, 1285, 699  ; BIN 2 INPUT
Sleep, 300
Send, ^v
Sleep, 300
Send, !{Tab}
Sleep, 300
Click, 300, 306  ; DISCOUNT VALUE
Sleep, 100
Send, ^c
Sleep, 100
Send, !{Tab}
Sleep, 300
Click, 1601, 618  ; BOGO DISCOUNT VALUE TYPE
Sleep, 300
Click, 1582, 650  ; BOGO DISCOUNT DOLLAR TYPE
Sleep, 500
Click, 1758, 625  ; BOGO DISCOUNT VALUE
Sleep, 300
Send, ^v
Sleep, 300
Click, 251, 633  ; CLOSE DISCOUNT SCREEN
Sleep, 300
Send, !{Tab}
Sleep, 300
Click, 84, 981  ; PREP FOR NEXT
Sleep, 300
Send, {Down}
Sleep, 300
Send, {Left}
}

RunPercentOffSequence() {
Click, 1911, 1003  ; SLIDE RIGHT
Sleep, 300
Click, 380, 306  ; DEAL TITLE
Sleep, 100
Send, ^c
Sleep, 100
Send, !{Tab}
Sleep, 300
Click, 1445, 286  ; NEW DEAL BUTTON
Sleep, 700
Click, 914, 351  ; DISCOUNT TITLE
Sleep, 300
Send, ^v
Sleep, 300
Click, 917, 431  ; DISCOUNT METHOD
Sleep, 300
Click, 914, 421  ; PERCENT DISCOUNT
Sleep, 300
Send, !{Tab}
Sleep, 300
Click, 300, 306  ; DISCOUNT VALUE
Sleep, 100
Send, ^c
Sleep, 100
Send, !{Tab}
Sleep, 500
Click, 908, 549  ; PERCENT DISCOUNT VALUE
Sleep, 300
Send, ^v
Sleep, 300
Click, 251, 633  ; CLOSE DISCOUNT SCREEN
Sleep, 300
Send, !{Tab}
Sleep, 300
Click, 84, 981  ; PREP FOR NEXT
Sleep, 300
Send, {Down}
Sleep, 300
Send, {Left}
}

RunDollarOffSequence() {
Click, 1911, 1003  ; SLIDE RIGHT
Sleep, 300
Click, 380, 306  ; DEAL TITLE
Sleep, 100
Send, ^c
Sleep, 100
Send, !{Tab}
Sleep, 300
Click, 1445, 286  ; NEW DEAL BUTTON
Sleep, 700
Click, 914, 351  ; DISCOUNT TITLE
Sleep, 300
Send, ^v
Sleep, 300
Click, 917, 431  ; DISCOUNT METHOD
Sleep, 300
Click, 942, 451  ; DOLLAR DISCOUNT
Sleep, 300
Send, !{Tab}
Sleep, 300
Click, 300, 306  ; DISCOUNT VALUE
Sleep, 100
Send, ^c
Sleep, 100
Send, !{Tab}
Sleep, 500
Click, 908, 549  ; DOLLAR DISCOUNT VALUE
Sleep, 300
Send, ^v
Sleep, 300
Click, 251, 633  ; CLOSE DISCOUNT SCREEN
Sleep, 300
Send, !{Tab}
Sleep, 300
Click, 84, 981  ; PREP FOR NEXT
Sleep, 300
Send, {Down}
Sleep, 300
Send, {Left}
}