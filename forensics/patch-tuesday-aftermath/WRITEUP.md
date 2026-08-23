This challenge involves opening a Windows EVTX log file and looking for a custom-made Windows event.

1) Open the attached event viewer file with Windows Event Viewer and navigate to the [Applications] tab 

2) Sort by the event code and look for the most recent event with the code "42069" and the Source of "PatchTuesdaySurvivor"

3) Double-click this event and observe the base64 hint, cut-off fla- I mean message, and the proceeding Base64 encoded string

4) Under the event properties, select the [Details] tab and observe the (decoded base64) flag: Pecan{windows_is_just_a_noisy_vm_with_extra_steps}


***AI USAGE DISCLOSURE: AI was used within this challenge solely to generate the PowerShell script responsible for the noisy logs - not including the flag
