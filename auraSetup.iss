; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

;CHANGE MY APP VERSION ON COMPILEEEEEEEEEEEE        |
;CHANGE MY APP VERSION ON COMPILEEEEEEEEEEEE        |
;CHANGE MY APP VERSION ON COMPILEEEEEEEEEEEE        |
;CHANGE MY APP VERSION ON COMPILEEEEEEEEEEEE        |
;CHANGE MY APP VERSION ON COMPILEEEEEEEEEEEE        |
;CHANGE MY APP VERSION ON COMPILEEEEEEEEEEEE        ||
;CHANGE MY APP VERSION ON COMPILEEEEEEEEEEEE      \\\///
 
#define MyAppName "Aura Buddy"
#define MyAppVersion "1.0" ;CHANGE MEMMEMEMEMEMEM
#define MyAppPublisher "AuraCLE"
#define MyAppURL "https://aurabuddy.my.canva.site"
#define MyAppExeName "AuraBuddy.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{F1C58EA3-7E35-4ADB-8A4D-E821BE9C25F8}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
InfoBeforeFile=C:\Users\Kp101\Desktop\aura\Read Me Install.txt
InfoAfterFile=C:\Users\Kp101\Desktop\aura\Read Me.txt
; Remove the following line to run in administrative install mode (install for all users.)
PrivilegesRequired=lowest
OutputBaseFilename=Aura Buddy Setup
OutputDir=C:\Users\Kp101\Desktop\aura
SetupIconFile=C:\Users\Kp101\OneDrive\C0d1ng\Windows 11 Icons\Downloads.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\Kp101\Desktop\aura\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Kp101\Desktop\aura\AuraBuddy\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

