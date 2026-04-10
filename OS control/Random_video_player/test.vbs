Set WshShell = CreateObject("WScript.Shell")

Randomize
key = Int((5 * Rnd) + 1)   ' 1 to 5

WScript.Sleep 2000        ' 2 sec wait (tab tak YouTube focus me le aao)

WshShell.SendKeys key

' MsgBox "Random key pressed: " & key