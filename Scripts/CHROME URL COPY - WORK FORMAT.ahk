; Auto-generated CHROME URL COPY - WORK FORMAT script - Created by Nick Robinson

SetTitleMatchMode, 2 ; Ensure Chrome windows are detected by their title.

F1::
{
; Check if the active window is a Google Chrome browser window
WinGet, activeWindowProcess, ProcessName, A
if (activeWindowProcess = "chrome.exe") {
; Get the URL from the active Chrome window
Clipboard := "" ; Clear the clipboard
Send, ^l ; Focus the address bar
Sleep, 100 ; Wait for the address bar to be focused
Send, ^c ; Copy the URL
ClipWait, 2 ; Wait for the clipboard to update

fullURL := Clipboard
extractedURL := "" ; Initialize extractedURL
; Extract the part of the URL after "highway-80/" or "f-street/"
if (InStr(fullURL, "highway-80/")) {
pos := InStr(fullURL, "highway-80/") + StrLen("highway-80/")
extractedURL := SubStr(fullURL, pos)
} else if (InStr(fullURL, "f-street/")) {
pos := InStr(fullURL, "f-street/") + StrLen("f-street/")
extractedURL := SubStr(fullURL, pos)
}

; Only proceed if extractedURL is not empty
if (extractedURL != "") {
Clipboard := extractedURL

; Check for specific admin URLs and handle accordingly
if (InStr(fullURL, "https://club420.com/highway80/wp-admin/post.php")) {
if (InStr(fullURL, "highway-80/")) {
; Scan the page for "href=\"/menu/highway-80/\""
Send, ^f ; Open find dialog
Sleep, 100
Send, href="/menu/highway-80/"
Sleep, 500 ; Wait for the find dialog to focus on the match
Send, {Esc} ; Close the find dialog

; Paste the partial URL in front of the matched phrase
Send, ^a ; Select all text in the field
Send, {Left} ; Move cursor to the start of the match
Send, %extractedURL% ; Paste the partial URL
} else {
MsgBox, 48, Error, THIS LINK IS FOR F STREET, YOU ARE ON HIGHWAY 80's PAGE.
return
}
} else if (InStr(fullURL, "https://club420.com/fstreet/wp-admin/post.php")) {
if (InStr(fullURL, "f-street/")) {
; Scan the page for "href=\"/menu/f-street/\""
Send, ^f ; Open find dialog
Sleep, 100
Send, href="/menu/f-street/"
Sleep, 500 ; Wait for the find dialog to focus on the match
Send, {Esc} ; Close the find dialog

; Paste the partial URL in front of the matched phrase
Send, ^a ; Select all text in the field
Send, {Left} ; Move cursor to the start of the match
Send, %extractedURL% ; Paste the partial URL
} else {
MsgBox, 48, Error, THIS LINK IS FOR HIGHWAY 80, YOU ARE ON F STREET'S PAGE.
return
}
}
} else {
Clipboard := "" ; Clear clipboard to ensure nothing is copied
ToolTip, Could not find the key part of the URL ("highway-80/" or "f-street/"), 10, 10
Sleep, 1000
ToolTip  ; Clear the tooltip
}
} else {
ToolTip, The active window is not a Google Chrome window., 10, 10
Sleep, 1000
ToolTip  ; Clear the tooltip
}
}

return
Esc::ExitApp