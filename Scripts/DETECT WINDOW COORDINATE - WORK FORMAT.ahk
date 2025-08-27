; Auto-generated DETECT WINDOW COORDINATE - WORK FORMAT script - Created by Nick Robinson

;#Persistent
SetTimer, ShowCoordinates, 10 ; Updates every 10 milliseconds
CoordMode, Mouse, Screen ; Use screen coordinates for MouseGetPos
CoordMode, Pixel, Screen ; Use screen coordinates for PixelGetColor

; Create the main GUI
Gui, TooltipGUI:+AlwaysOnTop -Caption +ToolWindow +Border

; Active Window Text
Gui, TooltipGUI:Font, s12 cBlack
Gui, TooltipGUI:Add, Text, vActiveWindowText w250 Center, Active Window:

; Mouse (Screen) Coordinates
Gui, TooltipGUI:Font, s10 cBlack
Gui, TooltipGUI:Add, Text, x18 y35 w50, Mouse
Gui, TooltipGUI:Add, Text, x70 y45 w1, :
Gui, TooltipGUI:Font, s7 cBlack
Gui, TooltipGUI:Add, Text, x180 y48 w141, (Mouse location on Screen)
Gui, TooltipGUI:Font, s10 cBlack
Gui, TooltipGUI:Add, Text, x12 y50 w50, (Screen)
Gui, TooltipGUI:Add, Button, vXScreenButton gCopyXScreen x80 y45 w48 h20, X:
Gui, TooltipGUI:Add, Button, vYScreenButton gCopyYScreen x130 y45 w48 h20, Y:

; Mouse (Window) Coordinates
Gui, TooltipGUI:Font, s10 cBlack
Gui, TooltipGUI:Add, Text, x18 y70 w50, Mouse
Gui, TooltipGUI:Add, Text, x70 y75 w1, :
Gui, TooltipGUI:Font, s7 cBlack
Gui, TooltipGUI:Add, Text, x180 y78 w141, (Mouse location in Window)
Gui, TooltipGUI:Font, s10 cBlack
Gui, TooltipGUI:Add, Text, x10 y85 w50, (Window)
Gui, TooltipGUI:Add, Button, vXWindowButton gCopyXWindow x80 y75 w48 h20, X:
Gui, TooltipGUI:Add, Button, vYWindowButton gCopyYWindow x130 y75 w48 h20, Y:

; Window Dimensions
Gui, TooltipGUI:Font, s10 cBlack
Gui, TooltipGUI:Add, Text, x18 y105 w60 h15, Window
Gui, TooltipGUI:Add, Text, x70 y110 w1, :
Gui, TooltipGUI:Font, s8 cBlack
Gui, TooltipGUI:Add, Text, x10 y120 w65 h12 w60, (Dimensions)
Gui, TooltipGUI:Font, s10 cBlack
Gui, TooltipGUI:Add, Button, vWinXButton gCopyWinX x80 y108 w50 h20, X1:
Gui, TooltipGUI:Add, Button, vWinYButton gCopyWinY x132 y108 w50 h20, Y1:
Gui, TooltipGUI:Add, Button, vWidthButton gCopyWidth x184 y108 w55 h20, W:
Gui, TooltipGUI:Add, Button, vHeightButton gCopyHeight x241 y108 w55 h20, H:

; RGB Hex Code as Buttons
Gui, TooltipGUI:Font, s10 cBlack
Gui, TooltipGUI:Add, Text, x24 y141 w60 h15, Color
Gui, TooltipGUI:Add, Text, x70 y146 w1, :
Gui, TooltipGUI:Font, s8 cBlack
Gui, TooltipGUI:Add, Text, x25 y156 w45 h12, (RGB)
Gui, TooltipGUI:Font, s10 cBlack
Gui, TooltipGUI:Add, Button, vHexCodeButton gCopyHexCode x80 y145 w100 h20, #000000
Gui, TooltipGUI:Add, Button, vHexButton gCopyHEX x185 y145 w100 h20, 0xFFFFFF
Gui, TooltipGUI:Font, s8 cBlack
Gui, TooltipGUI:Add, Text, x118 y132 w45 h12, (CSS)
Gui, TooltipGUI:Add, Text, x222 y132 w45 h12, (HEX)

; RGB Individual Values (Below "Color")
Gui, TooltipGUI:Font, s7 cRed
Gui, TooltipGUI:Add, Text, vRedValueText x144 y165 w35, R:00
Gui, TooltipGUI:Font, s7 cGreen
Gui, TooltipGUI:Add, Text, vGreenValueText x174 y165 w35, G:00
Gui, TooltipGUI:Font, s7 cBlue
Gui, TooltipGUI:Add, Text, vBlueValueText x204 y165 w35, B:00

; Create the Color Box as a separate GUI
Gui, ColorBoxGUI:+AlwaysOnTop -Caption +ToolWindow -Border
Gui, ColorBoxGUI:Show, w338 h10 x1 y188, ColorBox ; Static position in TooltipGUI

Gui, TooltipGUI:Show, NoActivate x0 y0, Live Values
global FreezeValues := false
return

ShowCoordinates:
if (FreezeValues) ; Skip updating when frozen
return

; Get the mouse position
MouseGetPos, xpos, ypos

; Retrieve the active window position, size, and title
WinGetPos, WinX, WinY, WinWidth, WinHeight, A ; Correct command syntax
if (ErrorLevel) ; Handle cases where there is no active window
{
ActiveWindowName := "No Active Window"
WinX := 0, WinY := 0, WinWidth := 0, WinHeight := 0
}
else
{
WinGetTitle, ActiveWindowName, A
}

; Calculate mouse position relative to the active window
if (WinWidth > 0 && WinHeight > 0)
{
WindowX := xpos - WinX
WindowY := ypos - WinY
}
else
{
WindowX := "N/A", WindowY := "N/A"
}

; Get the color of the pixel under the mouse
PixelGetColor, pixelColor, xpos, ypos, RGB
StringTrimLeft, pixelColor, pixelColor, 2 ; Remove "0x" prefix
Red := SubStr(pixelColor, 1, 2)
Green := SubStr(pixelColor, 3, 2)
Blue := SubStr(pixelColor, 5, 2)
HexWithPrefix := "0x" . pixelColor ; Prepare 0x prefixed HEX format

; Update the TooltipGUI content
GuiControl, TooltipGUI:, ActiveWindowText, Active Window: %ActiveWindowName%
GuiControl, TooltipGUI:, XScreenButton, X: %xpos%
GuiControl, TooltipGUI:, YScreenButton, Y: %ypos%
GuiControl, TooltipGUI:, XWindowButton, X: %WindowX%
GuiControl, TooltipGUI:, YWindowButton, Y: %WindowY%
GuiControl, TooltipGUI:, HexCodeButton, #%pixelColor%
GuiControl, TooltipGUI:, HexButton, %HexWithPrefix%
GuiControl, TooltipGUI:, RedValueText, R: %Red%
GuiControl, TooltipGUI:, GreenValueText, G: %Green%
GuiControl, TooltipGUI:, BlueValueText, B: %Blue%
GuiControl, TooltipGUI:, WinXButton, X1: %WinX%
GuiControl, TooltipGUI:, WinYButton, Y1: %WinY%
GuiControl, TooltipGUI:, WidthButton, W: %WinWidth%
GuiControl, TooltipGUI:, HeightButton, H: %WinHeight%

; Update Color Box GUI
Gui, ColorBoxGUI:Color, %pixelColor%
return

F8::
FreezeValues := !FreezeValues ; Toggle freeze mode
return

CopyXScreen:
Clipboard := xpos
return

CopyYScreen:
Clipboard := ypos
return

CopyXWindow:
Clipboard := WindowX
return

CopyYWindow:
Clipboard := WindowY
return

CopyHexCode:
Clipboard := "#" pixelColor
return

CopyHEX:
Clipboard := HexWithPrefix
return

CopyWinX:
Clipboard := WinX
return

CopyWinY:
Clipboard := WinY
return

CopyWidth:
Clipboard := WinWidth
return

CopyHeight:
Clipboard := WinHeight
return

Esc::ExitApp ; Press ESC to exit the script