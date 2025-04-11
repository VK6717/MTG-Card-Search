[Setup]
AppName=MTG Search Tool
AppVersion=1.0
DefaultDirName={pf}\MTG Search Tool
DefaultGroupName=MTG Search Tool
OutputDir=out
OutputBaseFilename=mtg_search_setup
Compression=lzma
SolidCompression=yes
SetupIconFile=icon.ico ; (volitelně - pokud máš .ico soubor)
VersionInfoVersion=1.0.0
VersionInfoDescription=Magic the Gathering card search tool
VersionInfoCompany=YourNameOrCompany

[Files]
Source: "dist\mtg_search.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "cards.csv"; DestDir: "{app}"; Flags: ignoreversion
Source: "driver\msedgedriver.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "out\*"; DestDir: "{app}\out"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\MTG Search Tool"; Filename: "{app}\mtg_search.exe"
Name: "{group}\Uninstall MTG Search Tool"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\mtg_search.exe"; Description: "Spustit MTG Search Tool"; Flags: nowait postinstall skipifsilent
