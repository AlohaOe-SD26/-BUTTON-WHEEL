; Auto-generated TEST TREEZ LOGIN - WORK FORMAT script - Created by Nick Robinson

#SingleInstance Force
SetWorkingDir %A_ScriptDir%
SetWorkingDir, ..\

CoordMode, Mouse, Screen
CoordMode, Pixel, Screen
CoordMode, Click, Screen
CoordMode, ImageSearch, Screen

; Read image paths from INI file
IniRead, NO_CUSTOMER_IMAGE, IMAGE_PATHS.ini, ImagePaths, NoCustomer
IniRead, NICK_ROBINSON_IMAGE, IMAGE_PATHS.ini, ImagePaths, NickRobinson
IniRead, PURCHASE_LIMITS_IMAGE, IMAGE_PATHS.ini, ImagePaths, PurchaseLimits
IniRead, NO_THANKS_IMAGE, IMAGE_PATHS.ini, ImagePaths, NoThanks
IniRead, SEARCH_CUSTOMERS_IMAGE, IMAGE_PATHS.ini, ImagePaths, SearchCustomers
IniRead, TEST_PROFILE_IMAGE, IMAGE_PATHS.ini, ImagePaths, TestProfile

; Add variance to image paths
NO_CUSTOMER_IMAGE := "*30 " . NO_CUSTOMER_IMAGE
NICK_ROBINSON_IMAGE := "*30 " . NICK_ROBINSON_IMAGE
PURCHASE_LIMITS_IMAGE := "*30 " . PURCHASE_LIMITS_IMAGE
NO_THANKS_IMAGE := "*30 " . NO_THANKS_IMAGE
SEARCH_CUSTOMERS_IMAGE := "*30 " . SEARCH_CUSTOMERS_IMAGE
TEST_PROFILE_IMAGE := "*30 " . TEST_PROFILE_IMAGE

; Search Areas
NEW_CUSTOMER_AREA_X1 := 976
NEW_CUSTOMER_AREA_Y1 := 227
NEW_CUSTOMER_AREA_X2 := 1405
NEW_CUSTOMER_AREA_Y2 := 297

SELECT_USER_AREA_X1 := 564
SELECT_USER_AREA_Y1 := 209
SELECT_USER_AREA_X2 := 1358
SELECT_USER_AREA_Y2 := 1035

CHECK_SCREEN_AREA_X1 := 962
CHECK_SCREEN_AREA_Y1 := 194
CHECK_SCREEN_AREA_X2 := 1118
CHECK_SCREEN_AREA_Y2 := 231

CLOSE_POPUP_AREA_X1 := 1639
CLOSE_POPUP_AREA_Y1 := 355
CLOSE_POPUP_AREA_X2 := 1734
CLOSE_POPUP_AREA_Y2 := 388

SEARCH_CUSTOMER_AREA_X1 := 285
SEARCH_CUSTOMER_AREA_Y1 := 200
SEARCH_CUSTOMER_AREA_X2 := 538
SEARCH_CUSTOMER_AREA_Y2 := 233

SEARCH_TEST_AREA_X1 := 346
SEARCH_TEST_AREA_Y1 := 57
SEARCH_TEST_AREA_X2 := 389
SEARCH_TEST_AREA_Y2 := 280

SearchAndClick(imagePath, x1, y1, x2, y2, waitTime := 10, clickAfterFound := true) {
imageW := 0
imageH := 0

if (InStr(imagePath, "*")) {
realPath := SubStr(imagePath, InStr(imagePath, " ") + 1)
} else {
realPath := imagePath
}

Loop {
ImageSearch, foundX, foundY, x1, y1, x2, y2, %imagePath%
if (!ErrorLevel) {
GetImageDimensions(realPath, imageW, imageH)
centerX := foundX + (imageW // 2)
centerY := foundY + (imageH // 2)

if (clickAfterFound) {
MouseMove, %centerX%, %centerY%, 0
Sleep, 50
Click
}
Sleep, %waitTime%
return true
}
Sleep, 50
}
}

GetImageDimensions(imagePath, ByRef width, ByRef height) {
Gui, Add, Picture, hwndPic, %imagePath%
ControlGetPos,,, width, height,, ahk_id %Pic%
Gui, Destroy
}


Sleep, 100
SearchAndClick(NO_CUSTOMER_IMAGE, NEW_CUSTOMER_AREA_X1, NEW_CUSTOMER_AREA_Y1, NEW_CUSTOMER_AREA_X2, NEW_CUSTOMER_AREA_Y2,, true)
Sleep, 100

Send, ^f
Sleep, 10
SendInput, Nick Robinson
Sleep, 10

SearchAndClick(NICK_ROBINSON_IMAGE, SELECT_USER_AREA_X1, SELECT_USER_AREA_Y1, SELECT_USER_AREA_X2, SELECT_USER_AREA_Y2,, true)
Sleep, 10

Send, 9252{Enter}
Sleep, 10

SearchAndClick(PURCHASE_LIMITS_IMAGE, CHECK_SCREEN_AREA_X1, CHECK_SCREEN_AREA_Y1, CHECK_SCREEN_AREA_X2, CHECK_SCREEN_AREA_Y2, 100, false)
Sleep, 10

SearchAndClick(NO_THANKS_IMAGE, CLOSE_POPUP_AREA_X1, CLOSE_POPUP_AREA_Y1, CLOSE_POPUP_AREA_X2, CLOSE_POPUP_AREA_Y2,, true)
Sleep, 10

SearchAndClick(SEARCH_CUSTOMERS_IMAGE, SEARCH_CUSTOMER_AREA_X1, SEARCH_CUSTOMER_AREA_Y1, SEARCH_CUSTOMER_AREA_X2, SEARCH_CUSTOMER_AREA_Y2, 500, true)

SendInput, Testttt{Enter}
Sleep, 10

SearchAndClick(TEST_PROFILE_IMAGE, SEARCH_TEST_AREA_X1, SEARCH_TEST_AREA_Y1, SEARCH_TEST_AREA_X2, SEARCH_TEST_AREA_Y2,, true)
Sleep, 10

Sleep, 10
ExitApp

Esc::ExitApp