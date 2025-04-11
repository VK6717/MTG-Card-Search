[Setup]
AppName=MTG Search Tool
AppVersion=0.1.1
DefaultDirName={commonpf}\MTG Search Tool
DefaultGroupName=MTG Search Tool
OutputDir=out
OutputBaseFilename=mtg_search_setup
Compression=lzma
SolidCompression=yes
SetupIconFile=mtg_icon.ico
VersionInfoVersion=0.1.1
VersionInfoDescription=Magic the Gathering card search tool
VersionInfoCompany=Vlada

[Files]
Source: "dist\mtg_search.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "cards.csv"; DestDir: "{app}"; Flags: ignoreversion
Source: "driver\msedgedriver.exe"; DestDir: "{app}\driver"; Flags: ignoreversion

[Icons]
Name: "{group}\MTG Search Tool"; Filename: "{app}\mtg_search.exe"
Name: "{group}\Uninstall MTG Search Tool"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\mtg_search.exe"; Description: "Spustit MTG Search Tool"; Flags: nowait postinstall skipifsilent

[Code]
var
  WorkingDirPage: TInputDirWizardPage;

procedure InitializeWizard;
begin
  WorkingDirPage := CreateInputDirPage(wpSelectDir,
    'Výstupní složka', 'Zadejte složku pro definici karet a ukládání výsledků.',
    'Zvolte nebo vytvořte pracovní složku programu. V této složce budete definovat karty k vyhledání a v této složce budou uloženy výsledky vyhledávání', False, '');
  WorkingDirPage.Add('');
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  IniPath: string;
begin
  if CurStep = ssPostInstall then
  begin
    IniPath := ExpandConstant('{app}\config.ini');
    SaveStringToFile(IniPath, '[DEFAULT]' + #13#10 + 'working_dir=' + WorkingDirPage.Values[0], False);
  end;
end;