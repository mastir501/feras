#define MyAppName "Adwaa ERP"
#define MyAppVersion "0.3.0"
[Setup]
AppId={{9C6F66BD-7778-4C19-9C73-4E3C1AD26E2B}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\Adwaa ERP
DefaultGroupName={#MyAppName}
OutputDir=installer_output
OutputBaseFilename=AdwaaERP_Setup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
[Files]
Source: "dist\AdwaaERP\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
[Icons]
Name: "{autoprograms}\Adwaa ERP"; Filename: "{app}\AdwaaERP.exe"
Name: "{autodesktop}\Adwaa ERP"; Filename: "{app}\AdwaaERP.exe"
[Run]
Filename: "{app}\AdwaaERP.exe"; Description: "Launch Adwaa ERP"; Flags: nowait postinstall skipifsilent
