; Auto-generated WORK TABS - WORK FORMAT script - Created by Nick Robinson

#SingleInstance Force
SetTimer, CheckWindowNames, 2000  ; Check window names every 2 seconds

; Path to Chrome executable
chromePath := "C:\Program Files\Google\Chrome\Application\chrome.exe"
; Profile path
profilePath := "C:\Users\Kinny\AppData\Local\Google\Chrome\User Data\Profile 7"

; Array to store window handles and their monitoring info
windowHandles := []

; Create the GUI
Gui, Add, Button, x10 y10 w200 h30 gOpenFStreet, F STREET
Gui, Add, Button, x10 y50 w200 h30 gOpenHighway80, HIGHWAY 80
Gui, Add, Button, x10 y90 w200 h30 gOpenDealCreate, DEAL CREATION
Gui, Add, Button, x10 y130 w200 h30 gOpenDemoScheduling, DEMO SCHEDULING
Gui, Add, Button, x10 y170 w200 h30 gOpenHappyCabbage, HAPPY CABBAGE
Gui, Add, Button, x10 y210 w200 h30 gOpenTextMessages, TEXT MESSAGES
Gui, +AlwaysOnTop  ; Make the GUI always on top
Gui, Show, w220 h250, Window Opener

; Add hotkey for ESC
#SingleInstance Force
#Persistent
Esc::ExitApp  ; ESC key will close the script

return  ; End of auto-execute section

; Function to open a new Chrome window with specified tabs
OpenChromeWindow(urlsArray, windowName) {
global chromePath, profilePath, windowHandles

; Concatenate URLs with spaces
urls := ""
for index, url in urlsArray {
urls .= url " "
}

; Run Chrome with the specified profile, new window, and URLs
Run, %chromePath% --profile-directory="Profile 7" --new-window %urls%

; Wait for the window to be active
WinWaitActive, ahk_class Chrome_WidgetWin_1

; Get the handle of the active window and store it with the associated name
WinGet, currentWindowHandle, ID, A
windowHandles.Push({Name: windowName, Handle: currentWindowHandle, CheckCount: 0})
}

; Function to check and rename windows
CheckWindowNames:
{
for index, windowInfo in windowHandles {
; Skip if we've already checked this window 5 times successfully
if (windowInfo.CheckCount >= 5) {
continue
}

; Check if the window still exists
if (!WinExist("ahk_id " windowInfo.Handle)) {
continue
}

; Get current window title
WinGetTitle, currentTitle, % "ahk_id " windowInfo.Handle

; If window title doesn't match desired name, rename it
if (currentTitle != windowInfo.Name) {
WinSetTitle, % "ahk_id " windowInfo.Handle,, % windowInfo.Name
} else {
; Increment check count if name matches
windowHandles[index].CheckCount += 1
}
}

; Clean up completed windows from the array
Loop, % windowHandles.Length() {
index := windowHandles.Length() - A_Index + 1
if (windowHandles[index].CheckCount >= 5) {
windowHandles.RemoveAt(index)
}
}
return
}

; Function to maximize the window
OpenMaximizedWindow(urlsArray, windowName) {
; Open the Chrome window
OpenChromeWindow(urlsArray, windowName)

; Maximize the window
WinMaximize, ahk_class Chrome_WidgetWin_1

; Initial rename
RenameWindow(windowHandles[windowHandles.Length()]["Handle"], windowName)

; Pause for 1000ms before the next window
Sleep, 1000
}

; Function to open, resize, and move the window
OpenResizeMoveWindow(urlsArray, x1, y1, width, height, windowName) {
; Open the Chrome window
OpenChromeWindow(urlsArray, windowName)

; Maximize the window initially
WinMaximize, ahk_class Chrome_WidgetWin_1

; Pause before resizing
Sleep, 1000

; Restore the window to normal state before resizing
WinRestore, ahk_class Chrome_WidgetWin_1

; Resize the window
WinMove, ahk_class Chrome_WidgetWin_1, , , , width, height

; Pause before moving
Sleep, 1000

; Move the window to the specified location
WinMove, ahk_class Chrome_WidgetWin_1, , x1, y1

; Initial rename
RenameWindow(windowHandles[windowHandles.Length()]["Handle"], windowName)

; Pause for 1000ms before the next window
Sleep, 1000
}

; Function to rename window
RenameWindow(windowHandle, windowName) {
Sleep, 3000  ; Wait for 3 seconds before renaming
WinSetTitle, % "ahk_id " windowHandle, , % windowName
}

; GUI Button handlers
OpenFStreet:
{
fStreetTabs := []
fStreetTabs.Push("https://club420.com/fstreet/deals/")
fStreetTabs.Push("https://club420.com/fstreet/secret-deals/")
fStreetTabs.Push("https://fstreet.treez.io/portalDispensary/portal/InventoryManagement/InventoryControl")
fStreetTabs.Push("https://fstreet.treez.io/portalDispensary/portal/ProductManagement")
fStreetTabs.Push("https://fstreet.treez.io/portalDispensary/portal/DiscountManagement/Discounts")
fStreetTabs.Push("https://fstreet.treez.io/SellTreez")
fStreetTabs.Push("https://club420.com/fstreet/wp-admin/edit.php?post_type=yith-wcbm-badge")
fStreetTabs.Push("https://club420.com/fstreet/wp-admin/edit.php?post_type=product")
fStreetTabs.Push("https://club420.com/menu/f-street/?order=-price")
OpenMaximizedWindow(fStreetTabs, "F STREET")
return
}

OpenHighway80:
{
highway80Tabs := []
highway80Tabs.Push("https://club420.com/highway80/deals/")
highway80Tabs.Push("https://club420.com/highway80/secret-deals/")
highway80Tabs.Push("https://h80d.treez.io/portalDispensary/portal/InventoryManagement/InventoryControl")
highway80Tabs.Push("https://h80d.treez.io/portalDispensary/portal/ProductManagement")
highway80Tabs.Push("https://h80d.treez.io/portalDispensary/portal/DiscountManagement/Discounts")
highway80Tabs.Push("https://h80d.treez.io/SellTreez")
highway80Tabs.Push("https://club420.com/highway80/wp-admin/edit.php?post_type=yith-wcbm-badge")
highway80Tabs.Push("https://club420.com/highway80/wp-admin/edit.php?post_type=product")
highway80Tabs.Push("https://club420.com/menu/highway-80/?order=-price")`
OpenMaximizedWindow(highway80Tabs, "HIGHWAY 80")
return
}

OpenDealCreate:
{
DealCreatePrepTabs := []
DealCreatePrepTabs.Push("https://mail.google.com/mail/u/0/#inbox")
DealCreatePrepTabs.Push("https://www.canva.com/design/DAGevZjxOxU/k1VQePkRxNJS78nYubvp1w/edit")
DealCreatePrepTabs.Push("https://images.google.com/")
DealCreatePrepTabs.Push("https://docs.google.com/spreadsheets/d/1cL_uv5Tkq-TQIvhsZnAfp-weMc4JGkys60r3efoB2DA/edit?gid=2117398109#gid=2117398109")
DealCreatePrepTabs.Push("https://script.google.com/home/projects/1FO_PSF_VMburu-OalNGVBFuCHI9veLUVDg5r1ezs3BZpgC3zdLhvOoEb/edit")
DealCreatePrepTabs.Push("https://docs.google.com/spreadsheets/d/1GJUZe4Srz199oGtMEqt1yspnhydNvFA90j9pGSOrURk/edit?gid=756092787#gid=756092787")
DealCreatePrepTabs.Push("https://script.google.com/home/projects/1Kd28zdW--YMbr7yJMiIz-ZRQQI3v7EW8y0ahuFwAY3BdFpXl3u7PdxzJ/edit")
DealCreatePrepTabs.Push("https://docs.google.com/spreadsheets/d/1DA1FjHQfK0a_1zpeRZh5GKpMTL6zRCyletGi5nsB33I/edit?gid=1949221251#gid=1949221251")
OpenMaximizedWindow(DealCreatePrepTabs, "DEAL CREATION")
return
}

OpenDemoScheduling:
{
demoSchedulingTabs := []
demoSchedulingTabs.Push("https://mail.google.com/mail/u/0/#inbox")
demoSchedulingTabs.Push("https://calendar.google.com/calendar/u/0/r")
demoSchedulingTabs.Push("https://docs.google.com/spreadsheets/d/1A0hSy6fw8n4uZ63J5vAGYMSG3KC3qPtavsE1Wt2JDBw/edit?gid=1131168423#gid=1131168423")
demoSchedulingTabs.Push("https://script.google.com/home/projects/17LCsrLZFX5Qi6Fw-UAHY7L4HPZdVWtWh59dkMPl9PSaF0exyFo_FF1wY/edit")
demoSchedulingTabs.Push("https://script.google.com/home/projects/1Kd28zdW--YMbr7yJMiIz-ZRQQI3v7EW8y0ahuFwAY3BdFpXl3u7PdxzJ/edit")
demoSchedulingTabs.Push("https://docs.google.com/spreadsheets/d/1oYOYtOFXkKaIFlw2p--5sOMjPbip7SnaFTykclN5x9M/edit?gid=1378786763#gid=1378786763")
OpenMaximizedWindow(demoSchedulingTabs, "DEMO SCHEDULING")
return
}

OpenHappyCabbage:
{
happyCabbageTabs := []
happyCabbageTabs.Push("https://happycabbage.app/connect/#/login?url=https:%2F%2Fhappycabbage.app%2Fconnect%2F%23%2Fcontent%2Flisting%3Ffilter%3Dmin_role:viewer%26filter%3Dcontent_type:all%26view_type%3Dexpanded")
happyCabbageTabs.Push("https://www.canva.com/folder/FAFqt_ZhDn4")
OpenResizeMoveWindow(happyCabbageTabs, -10, 0, 1004, 1047, "HAPPY CABBAGE")
return
}

OpenTextMessages:
{
textMessagesTabs := []
textMessagesTabs.Push("https://docs.google.com/spreadsheets/d/1DQXp9sGqDoVnBW0zybjFoS27oqcJhW4Y0KexhCgOLjI/edit?gid=27737098#gid=27737098")
textMessagesTabs.Push("https://wordcounter.net/character-count")
OpenResizeMoveWindow(textMessagesTabs, 977, 0, 952, 1047, "TEXT MESSAGES")
return
}

; Add GuiClose label to handle closing the GUI
GuiClose:
ExitApp