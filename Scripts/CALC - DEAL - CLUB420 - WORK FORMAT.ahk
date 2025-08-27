; Auto-generated CALC - DEAL - CLUB420 - WORK FORMAT script - Created by Nick Robinson

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

; FSD Cannabis Deal Calculator
Gui, Add, GroupBox, x20 y40 w300 h245
Gui, Font, cGreen s13 Bold
Gui, Add, Text, x30 y50, FSD Cannabis Deal Calc.
Gui, Font, cGreen s10, Verdana
Gui, Add, Text, x30 y80, Enter Pre-Tax Value:
Gui, Add, Edit, x30 y100 w150 vFSD_C_Pre_Tax_Value_Input
Gui, Add, Text, x30 y130, Enter Product Quantity:
Gui, Add, Edit, x30 y150 w150 vFSD_C_Product_Qty_Input
Gui, Add, Text, x30 y180, Enter Desired Price:
Gui, Add, Edit, x30 y200 w150 vFSD_C_Instore_Desired_Price_Input
Gui, Add, Text, x30 y230, Discount Value:
Gui, Add, Edit, x30 y250 w150 vFSD_C_Instore_Discount_Output ReadOnly
Gui, Add, Button, x190 y210 gCalculate_FSD_Cannabis_Deal, CALCULATE
Gui, Font, cRed
Gui, Add, Button, x190 y250 w80 h25 gClear_FSD_Cannabis_Deal, CLEAR
Gui, Font, cGreen

; FSD Hard Good Deal Calculator
Gui, Add, GroupBox, x20 y290 w300 h245
Gui, Font, cGreen s13 Bold
Gui, Add, Text, x30 y300, FSD Hard Good Deal Calc.
Gui, Font, cGreen s10, Verdana
Gui, Add, Text, x30 y330, Enter Pre-Tax Value:
Gui, Add, Edit, x30 y350 w150 vFSD_H_Pre_Tax_Value_Input
Gui, Add, Text, x30 y380, Enter Product Quantity:
Gui, Add, Edit, x30 y400 w150 vFSD_H_Product_Qty_Input
Gui, Add, Text, x30 y430, Enter Desired Price:
Gui, Add, Edit, x30 y450 w150 vFSD_H_Instore_Desired_Price_Input
Gui, Add, Text, x30 y480, Discount Value:
Gui, Add, Edit, x30 y500 w150 vFSD_H_Instore_Discount_Output ReadOnly
Gui, Add, Button, x190 y460 gCalculate_FSD_HardGood_Deal, CALCULATE
Gui, Font, cRed
Gui, Add, Button, x190 y500 w80 h25 gClear_FSD_HardGood_Deal, CLEAR
Gui, Font, cGreen

; --- H80 SECTION ---
Gui, Font, c8B0000 s14 Bold
Gui, Add, GroupBox, x360 y10 w320 h530, -----H80 CALCULATORS-----
Gui, Font, c8B0000 s10, Verdana

; H80 Cannabis Deal Calculator
Gui, Add, GroupBox, x370 y40 w300 h245
Gui, Font, c8B0000 s13 Bold
Gui, Add, Text, x380 y50, H80 Cannabis Deal Calc.
Gui, Font, c8B0000 s10, Verdana
Gui, Add, Text, x380 y80, Enter Pre-Tax Value:
Gui, Add, Edit, x380 y100 w150 vH80_C_Pre_Tax_Value_Input
Gui, Add, Text, x380 y130, Enter Product Quantity:
Gui, Add, Edit, x380 y150 w150 vH80_C_Product_Qty_Input
Gui, Add, Text, x380 y180, Enter Desired Price:
Gui, Add, Edit, x380 y200 w150 vH80_C_Instore_Desired_Price_Input
Gui, Add, Text, x380 y230, Discount Value:
Gui, Add, Edit, x380 y250 w150 vH80_C_Instore_Discount_Output ReadOnly
Gui, Add, Button, x540 y210 gCalculate_H80_Cannabis_Deal, CALCULATE
Gui, Font, cRed
Gui, Add, Button, x540 y250 w80 h25 gClear_H80_Cannabis_Deal, CLEAR
Gui, Font, c8B0000

; H80 Hard Good Deal Calculator
Gui, Add, GroupBox, x370 y290 w300 h245
Gui, Font, c8B0000 s13 Bold
Gui, Add, Text, x380 y300, H80 Hard Good Deal Calc.
Gui, Font, c8B0000 s10, Verdana
Gui, Add, Text, x380 y330, Enter Pre-Tax Value:
Gui, Add, Edit, x380 y350 w150 vH80_H_Pre_Tax_Value_Input
Gui, Add, Text, x380 y380, Enter Product Quantity:
Gui, Add, Edit, x380 y400 w150 vH80_H_Product_Qty_Input
Gui, Add, Text, x380 y430, Enter Desired Price:
Gui, Add, Edit, x380 y450 w150 vH80_H_Instore_Desired_Price_Input
Gui, Add, Text, x380 y480, Discount Value:
Gui, Add, Edit, x380 y500 w150 vH80_H_Instore_Discount_Output ReadOnly
Gui, Add, Button, x540 y450 gCalculate_H80_HardGood_Deal, CALCULATE
Gui, Font, cRed
Gui, Add, Button, x540 y490 w80 h25 gClear_H80_HardGood_Deal, CLEAR
Gui, Font, c8B0000

; Add Settings Button
Gui, Add, Button, x328 y20 w33 h33 gOpenSettingsWindow, *

; Show GUI
Gui, Show, w688 h550, CLUB420 DEAL CALCULATOR

; --- Calculation Functions ---
Calculate_FSD_Cannabis_Deal:
    GuiControlGet, preTax,, FSD_C_Pre_Tax_Value_Input
    GuiControlGet, qty,, FSD_C_Product_Qty_Input
    GuiControlGet, desiredPrice,, FSD_C_Instore_Desired_Price_Input
    discount := ((preTax * qty) * FSD_C_TAXRATE - desiredPrice) / FSD_C_TAXRATE
    GuiControl,, FSD_C_Instore_Discount_Output, % Format("{:.4f}", discount)
return

Calculate_FSD_HardGood_Deal:
    GuiControlGet, preTax,, FSD_H_Pre_Tax_Value_Input
    GuiControlGet, qty,, FSD_H_Product_Qty_Input
    GuiControlGet, desiredPrice,, FSD_H_Instore_Desired_Price_Input
    discount := ((preTax * qty) * FSD_H_TAXRATE - desiredPrice) / FSD_H_TAXRATE
    GuiControl,, FSD_H_Instore_Discount_Output, % Format("{:.4f}", discount)
return

Calculate_H80_Cannabis_Deal:
    GuiControlGet, preTax,, H80_C_Pre_Tax_Value_Input
    GuiControlGet, qty,, H80_C_Product_Qty_Input
    GuiControlGet, desiredPrice,, H80_C_Instore_Desired_Price_Input
    discount := ((preTax * qty) * H80_C_TAXRATE - desiredPrice) / H80_C_TAXRATE
    GuiControl,, H80_C_Instore_Discount_Output, % Format("{:.4f}", discount)
return

Calculate_H80_HardGood_Deal:
    GuiControlGet, preTax,, H80_H_Pre_Tax_Value_Input
    GuiControlGet, qty,, H80_H_Product_Qty_Input
    GuiControlGet, desiredPrice,, H80_H_Instore_Desired_Price_Input
    discount := ((preTax * qty) * H80_H_TAXRATE - desiredPrice) / H80_H_TAXRATE
    GuiControl,, H80_H_Instore_Discount_Output, % Format("{:.4f}", discount)
return

; --- Clear Functions ---
Clear_FSD_Cannabis_Deal:
    GuiControl,, FSD_C_Pre_Tax_Value_Input
    GuiControl,, FSD_C_Product_Qty_Input
    GuiControl,, FSD_C_Instore_Desired_Price_Input
    GuiControl,, FSD_C_Instore_Discount_Output
return

Clear_FSD_HardGood_Deal:
    GuiControl,, FSD_H_Pre_Tax_Value_Input
    GuiControl,, FSD_H_Product_Qty_Input
    GuiControl,, FSD_H_Instore_Desired_Price_Input
    GuiControl,, FSD_H_Instore_Discount_Output
return

Clear_H80_Cannabis_Deal:
    GuiControl,, H80_C_Pre_Tax_Value_Input
    GuiControl,, H80_C_Product_Qty_Input
    GuiControl,, H80_C_Instore_Desired_Price_Input
    GuiControl,, H80_C_Instore_Discount_Output
return

Clear_H80_HardGood_Deal:
    GuiControl,, H80_H_Pre_Tax_Value_Input
    GuiControl,, H80_H_Product_Qty_Input
    GuiControl,, H80_H_Instore_Desired_Price_Input
    GuiControl,, H80_H_Instore_Discount_Output
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