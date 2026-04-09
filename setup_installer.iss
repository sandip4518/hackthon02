; ScreenZen Installer Script for Inno Setup
; To build:
; 1. Build the EXE using build_exe.bat
; 2. Open this file in Inno Setup and click Run

[Setup]
AppId={{D34D-BEEF-4848-8901-A180B48E4C48}
AppName=ScreenZen
AppVersion=1.0
AppPublisher=Vikky2810
AppPublisherURL=https://github.com/vikky2810/hackthon02
AppSupportURL=https://github.com/vikky2810/hackthon02
AppUpdatesURL=https://github.com/vikky2810/hackthon02
DefaultDirName={autopf}\ScreenZen
DisableProgramGroupPage=yes
LicenseFile=LICENSE
OutputBaseFilename=ScreenZen_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=assets\logo.ico

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\ScreenZen.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: The database and data folders are created by the app on first run

[Icons]
Name: "{autoprograms}\ScreenZen"; Filename: "{app}\ScreenZen.exe"
Name: "{autodesktop}\ScreenZen"; Filename: "{app}\ScreenZen.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\ScreenZen.exe"; Description: "{cm:LaunchProgram,ScreenZen}"; Flags: nowait postinstall skipfsredundant
