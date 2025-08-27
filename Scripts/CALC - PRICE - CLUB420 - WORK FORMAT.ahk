; Auto-generated CALC - PRICE - CLUB420 - WORK FORMAT script - Created by Nick Robinson

; --- WINDOW SETUP ---
Gui, Margin, 10, 10
Gui, Font, s10, Verdana

; Define tax rates
FSD_C_TAXRATE := 1.3693625
FSD_H_TAXRATE := 1.0825
H80_C_TAXRATE := 1.296553125
H80_H_TAXRATE := 1.08375

; --- FSD SECTION ---
Gui, Font, cGreen s14 Bold
Gui, Add, GroupBox, x10 y10 w320 h530, -----FSD CALCULATORS-----
Gui, Font, cGreen s10, Verdana

; FSD Cannabis Reprice Calculator
Gui, Add, GroupBox, x20 y40 w300 h240
Gui, Font, cGreen s13 Bold
Gui, Add, Text, x30 y50, FSD Cannabis Price Calc.
Gui, Font, cGreen s10, Verdana
Gui, Add, Text, x30 y80, INSTORE Price:
Gui, Add, Edit, x30 y100 w80 vFSD_C_Reprice_Input
Gui, Add, Text, x150 y80, ONLINE Price:
Gui, Add, Edit, x150 y100 w80 vFSD_C_Online_Price_Input
Gui, Add, Text, x30 y130, CSTM PRCNT:      PRICE W CSTM PRCNT:
Gui, Add, Edit, x30 y150 w80 vFSD_C_Custom_Off_Input
Gui, Add, Edit, x150 y150 w80 vFSD_C_Custom_Price_Input
Gui, Add, Text, x30 y180, Pre-Tax Price Value:
Gui, Add, Edit, x30 y200 w150 vFSD_C_Reprice_Output ReadOnly
Gui, Add, Button, x30 y240 gCalculate_FSD_Cannabis_Reprice, CALCULATE
Gui, Font, cRed
Gui, Add, Button, x150 y240 w80 h25 gClear_FSD_Cannabis_Reprice, CLEAR
Gui, Font, cGreen

; FSD Hard Good Reprice Calculator
Gui, Add, GroupBox, x20 y290 w300 h240  ; Moved up 10 pixels below Cannabis GroupBox
Gui, Font, cGreen s13 Bold
Gui, Add, Text, x30 y300, FSD Hard Good Price Calc.
Gui, Font, cGreen s10, Verdana
Gui, Add, Text, x30 y330, INSTORE Price:
Gui, Add, Edit, x30 y350 w80 vFSD_H_Reprice_Input
Gui, Add, Text, x150 y330, ONLINE Price:
Gui, Add, Edit, x150 y350 w80 vFSD_H_Online_Price_Input
Gui, Add, Text, x30 y380, CSTM PRCNT:      PRICE W CSTM PRCNT:
Gui, Add, Edit, x30 y400 w80 vFSD_H_Custom_Off_Input
Gui, Add, Edit, x150 y400 w80 vFSD_H_Custom_Price_Input
Gui, Add, Text, x30 y430, Pre-Tax Price Value:
Gui, Add, Edit, x30 y450 w150 vFSD_H_Reprice_Output ReadOnly
Gui, Add, Button, x30 y490 gCalculate_FSD_HardGood_Reprice, CALCULATE
Gui, Font, cRed
Gui, Add, Button, x150 y490 w80 h25 gClear_FSD_HardGood_Reprice, CLEAR
Gui, Font, cGreen

; --- H80 SECTION ---
Gui, Font, c8B0000 s14 Bold
Gui, Add, GroupBox, x360 y10 w320 h530, -----H80 CALCULATORS-----
Gui, Font, c8B0000 s10, Verdana

; H80 Cannabis Reprice Calculator
Gui, Add, GroupBox, x370 y40 w300 h240
Gui, Font, c8B0000 s13 Bold
Gui, Add, Text, x380 y50, H80 Cannabis Price Calc.
Gui, Font, c8B0000 s10, Verdana
Gui, Add, Text, x380 y80, INSTORE Price:
Gui, Add, Edit, x380 y100 w80 vH80_C_Reprice_Input
Gui, Add, Text, x500 y80, ONLINE Price:
Gui, Add, Edit, x500 y100 w80 vH80_C_Online_Price_Input
Gui, Add, Text, x380 y130, CSTM PRCNT:      PRICE W CSTM PRCNT:
Gui, Add, Edit, x380 y150 w80 vH80_C_Custom_Off_Input
Gui, Add, Edit, x500 y150 w80 vH80_C_Custom_Price_Input
Gui, Add, Text, x380 y180, Pre-Tax Price Value:
Gui, Add, Edit, x380 y200 w150 vH80_C_Reprice_Output ReadOnly
Gui, Add, Button, x380 y240 gCalculate_H80_Cannabis_Reprice, CALCULATE
Gui, Font, cRed
Gui, Add, Button, x500 y240 w80 h25 gClear_H80_Cannabis_Reprice, CLEAR
Gui, Font, c8B0000

; H80 Hard Good Reprice Calculator
Gui, Add, GroupBox, x370 y290 w300 h240 ; Adjusted to match FSD
Gui, Font, c8B0000 s13 Bold
Gui, Add, Text, x380 y300, H80 Hard Good Price Calc.
Gui, Font, c8B0000 s10, Verdana
Gui, Add, Text, x380 y330, INSTORE Price:
Gui, Add, Edit, x380 y350 w80 vH80_H_Reprice_Input
Gui, Add, Text, x500 y330, ONLINE Price:
Gui, Add, Edit, x500 y350 w80 vH80_H_Online_Price_Input
Gui, Add, Text, x380 y380, CSTM PRCNT:      PRICE W CSTM PRCNT:
Gui, Add, Edit, x380 y400 w80 vH80_H_Custom_Off_Input
Gui, Add, Edit, x500 y400 w80 vH80_H_Custom_Price_Input
Gui, Add, Text, x380 y430, Pre-Tax Price Value:
Gui, Add, Edit, x380 y450 w150 vH80_H_Reprice_Output ReadOnly
Gui, Add, Button, x380 y490 gCalculate_H80_HardGood_Reprice, CALCULATE
Gui, Font, cRed
Gui, Add, Button, x500 y490 w80 h25 gClear_H80_HardGood_Reprice, CLEAR
Gui, Font, c8B0000

; Add Settings Button
Gui, Add, Button, x328 y20 w33 h33 gOpenSettingsWindow, *

; Show GUI
Gui, Show, w688 h550, CLUB420 PRICE CALCULATOR

; --- Calculation Functions ---

Calculate_FSD_Cannabis_Reprice:
    GuiControlGet, desiredPrice,, FSD_C_Reprice_Input
    GuiControlGet, onlinePrice,, FSD_C_Online_Price_Input
    GuiControlGet, customPercent,, FSD_C_Custom_Off_Input

    ; Ensure CSTM PRCNT is filled
    if customPercent = "" ; Skip calculation if CSTM PRCNT is not provided
    {
        GuiControl,, FSD_C_Custom_Price_Input  ; Clear the PRICE W CSTM PRCNT field
        return
    }
    customPercent := customPercent / 100 ; Convert percent to decimal

    if desiredPrice !=
    {
        preTax := desiredPrice / FSD_C_TAXRATE
        onlinePrice := desiredPrice * 0.75
        customPrice := desiredPrice * (1 - customPercent)
        GuiControl,, FSD_C_Reprice_Output, % Format("{:.4f}", preTax)
        GuiControl,, FSD_C_Online_Price_Input, % Format("{:.4f}", onlinePrice)
        GuiControl,, FSD_C_Custom_Price_Input, % Format("{:.4f}", customPrice)
    }
    else if onlinePrice !=
    {
        desiredPrice := onlinePrice / 0.75
        preTax := desiredPrice / FSD_C_TAXRATE
        customPrice := desiredPrice * (1 - customPercent)
        GuiControl,, FSD_C_Reprice_Input, % Format("{:.4f}", desiredPrice)
        GuiControl,, FSD_C_Reprice_Output, % Format("{:.4f}", preTax)
        GuiControl,, FSD_C_Custom_Price_Input, % Format("{:.4f}", customPrice)
    }
return

Calculate_FSD_HardGood_Reprice:
    GuiControlGet, desiredPrice,, FSD_H_Reprice_Input
    GuiControlGet, onlinePrice,, FSD_H_Online_Price_Input
    GuiControlGet, customPercent,, FSD_H_Custom_Off_Input

    if customPercent = ""
    {
        GuiControl,, FSD_H_Custom_Price_Input
        return
    }
    customPercent := customPercent / 100

    if desiredPrice !=
    {
        preTax := desiredPrice / FSD_H_TAXRATE
        onlinePrice := desiredPrice * 0.75
        customPrice := desiredPrice * (1 - customPercent)
        GuiControl,, FSD_H_Reprice_Output, % Format("{:.4f}", preTax)
        GuiControl,, FSD_H_Online_Price_Input, % Format("{:.4f}", onlinePrice)
        GuiControl,, FSD_H_Custom_Price_Input, % Format("{:.4f}", customPrice)
    }
    else if onlinePrice !=
    {
        desiredPrice := onlinePrice / 0.75
        preTax := desiredPrice / FSD_H_TAXRATE
        customPrice := desiredPrice * (1 - customPercent)
        GuiControl,, FSD_H_Reprice_Input, % Format("{:.4f}", desiredPrice)
        GuiControl,, FSD_H_Reprice_Output, % Format("{:.4f}", preTax)
        GuiControl,, FSD_H_Custom_Price_Input, % Format("{:.4f}", customPrice)
    }
return

Calculate_H80_Cannabis_Reprice:
    GuiControlGet, desiredPrice,, H80_C_Reprice_Input
    GuiControlGet, onlinePrice,, H80_C_Online_Price_Input
    GuiControlGet, customPercent,, H80_C_Custom_Off_Input

    if customPercent = ""
    {
        GuiControl,, H80_C_Custom_Price_Input
        return
    }
    customPercent := customPercent / 100

    if desiredPrice !=
    {
        preTax := desiredPrice / H80_C_TAXRATE
        onlinePrice := desiredPrice * 0.75
        customPrice := desiredPrice * (1 - customPercent)
        GuiControl,, H80_C_Reprice_Output, % Format("{:.4f}", preTax)
        GuiControl,, H80_C_Online_Price_Input, % Format("{:.4f}", onlinePrice)
        GuiControl,, H80_C_Custom_Price_Input, % Format("{:.4f}", customPrice)
    }
    else if onlinePrice !=
    {
        desiredPrice := onlinePrice / 0.75
        preTax := desiredPrice / H80_C_TAXRATE
        customPrice := desiredPrice * (1 - customPercent)
        GuiControl,, H80_C_Reprice_Input, % Format("{:.4f}", desiredPrice)
        GuiControl,, H80_C_Reprice_Output, % Format("{:.4f}", preTax)
        GuiControl,, H80_C_Custom_Price_Input, % Format("{:.4f}", customPrice)
    }
return

Calculate_H80_HardGood_Reprice:
    GuiControlGet, desiredPrice,, H80_H_Reprice_Input
    GuiControlGet, onlinePrice,, H80_H_Online_Price_Input
    GuiControlGet, customPercent,, H80_H_Custom_Off_Input

    if customPercent = ""
    {
        GuiControl,, H80_H_Custom_Price_Input
        return
    }
    customPercent := customPercent / 100

    if desiredPrice !=
    {
        preTax := desiredPrice / H80_H_TAXRATE
        onlinePrice := desiredPrice * 0.75
        customPrice := desiredPrice * (1 - customPercent)
        GuiControl,, H80_H_Reprice_Output, % Format("{:.4f}", preTax)
        GuiControl,, H80_H_Online_Price_Input, % Format("{:.4f}", onlinePrice)
        GuiControl,, H80_H_Custom_Price_Input, % Format("{:.4f}", customPrice)
    }
    else if onlinePrice !=
    {
        desiredPrice := onlinePrice / 0.75
        preTax := desiredPrice / H80_H_TAXRATE
        customPrice := desiredPrice * (1 - customPercent)
        GuiControl,, H80_H_Reprice_Input, % Format("{:.4f}", desiredPrice)
        GuiControl,, H80_H_Reprice_Output, % Format("{:.4f}", preTax)
        GuiControl,, H80_H_Custom_Price_Input, % Format("{:.4f}", customPrice)
    }
return

; --- Clear Functions ---
Clear_FSD_Cannabis_Reprice:
    GuiControl,, FSD_C_Reprice_Input
    GuiControl,, FSD_C_Reprice_Output
    GuiControl,, FSD_C_Online_Price_Input
    GuiControl,, FSD_C_Custom_Off_Input
    GuiControl,, FSD_C_Custom_Price_Input
return

Clear_FSD_HardGood_Reprice:
    GuiControl,, FSD_H_Reprice_Input
    GuiControl,, FSD_H_Reprice_Output
    GuiControl,, FSD_H_Online_Price_Input
    GuiControl,, FSD_H_Custom_Off_Input
    GuiControl,, FSD_H_Custom_Price_Input
return

Clear_H80_Cannabis_Reprice:
    GuiControl,, H80_C_Reprice_Input
    GuiControl,, H80_C_Reprice_Output
    GuiControl,, H80_C_Online_Price_Input
    GuiControl,, H80_C_Custom_Off_Input
    GuiControl,, H80_C_Custom_Price_Input
return

Clear_H80_HardGood_Reprice:
    GuiControl,, H80_H_Reprice_Input
    GuiControl,, H80_H_Reprice_Output
    GuiControl,, H80_H_Online_Price_Input
    GuiControl,, H80_H_Custom_Off_Input
    GuiControl,, H80_H_Custom_Price_Input
return

; --- Settings Window ---
OpenSettingsWindow:
    ; Create a new settings GUI (only when button is clicked)
    Gui, New, +AlwaysOnTop +Owner +LabelSettingsWindow, SETTINGS_WINDOW
    Gui, Font, s10, Verdana

    ; FSD SETTINGS
    Gui, Font, cGreen s13.5 Bold
    Gui, Add, GroupBox, x10 y10 w300 h120, -------FSD SETTINGS-------
    Gui, Font, cGreen s9
    Gui, Add, Text, x20 y40, Cannabis Tax Rate:
    Gui, Add, Edit, x160 y40 w120 vFSD_C_TaxRateInput, % FSD_C_TAXRATE
    Gui, Add, Text, x20 y80, Hard Good Tax Rate:
    Gui, Add, Edit, x160 y80 w120 vFSD_H_TaxRateInput, % FSD_H_TAXRATE

    ; H80 SETTINGS
    Gui, Font, c8B0000 s13.5 Bold
    Gui, Add, GroupBox, x10 y130 w300 h120, -------H80 SETTINGS-------
    Gui, Font, c8B0000 s9
    Gui, Add, Text, x20 y160, Cannabis Tax Rate:
    Gui, Add, Edit, x160 y160 w120 vH80_C_TaxRateInput, % H80_C_TAXRATE
    Gui, Add, Text, x20 y200, Hard Good Tax Rate:
    Gui, Add, Edit, x160 y200 w120 vH80_H_TaxRateInput, % H80_H_TAXRATE

    ; Buttons
    Gui, Add, Button, x65 y260 w80 h30 gSaveSettings, SAVE
    Gui, Add, Button, X165 y260 w80 h30 gResetToDefault, RESET

    ; Show the Settings GUI
    Gui, Show, w330 h310, SETTINGS
return

; Reset to Default
ResetToDefault:
    GuiControl,, FSD_C_TaxRateInput, % 1.3693625
    GuiControl,, FSD_H_TaxRateInput, % 1.0825
    GuiControl,, H80_C_TaxRateInput, % 1.296553125
    GuiControl,, H80_H_TaxRateInput, % 1.08375
return

SaveSettings:
    GuiControlGet, FSD_C_TAXRATE,, FSD_C_TaxRateInput
    GuiControlGet, FSD_H_TAXRATE,, FSD_H_TaxRateInput
    GuiControlGet, H80_C_TAXRATE,, H80_C_TaxRateInput
    GuiControlGet, H80_H_TAXRATE,, H80_H_TaxRateInput
    Gui, SettingsWindow: Destroy ; Close the settings window
return

; Close Settings Window
CloseSettingsWindow:
    Gui, SettingsWindow: Destroy
return

Esc::ExitApp

GuiClose:
    ExitApp