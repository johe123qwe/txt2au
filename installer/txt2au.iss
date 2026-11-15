; 文字转音频 Windows 安装程序（Inno Setup 6）
; 通常由 build_windows.ps1 调用：
;   ISCC.exe /DAppVersion=1.2.2 /DSourceDir=<dist\文字转音频> /DOutputDir=<dist\release> installer\txt2au.iss
; 注意：本文件需保存为 UTF-8 with BOM，否则中文会乱码。

#define AppName "文字转音频"
#define AppExeName "文字转音频.exe"
#define AppPublisher "txt2au"

#ifndef AppVersion
  #define AppVersion "0.0.0"
#endif
#ifndef SourceDir
  #define SourceDir AddBackslash(SourcePath) + "..\dist\" + AppName
#endif
#ifndef OutputDir
  #define OutputDir AddBackslash(SourcePath) + "..\dist\release"
#endif

[Setup]
; AppId 用于识别同一程序（升级/卸载），不要修改
AppId={{62573FFD-8382-42B9-BF39-545B7B58E1D3}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher={#AppPublisher}
VersionInfoVersion={#AppVersion}
DefaultDirName={autopf}\txt2au
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
OutputDir={#OutputDir}
OutputBaseFilename=txt2au-{#AppVersion}-windows-setup
SetupIconFile=..\src\logo.ico
UninstallDisplayIcon={app}\{#AppExeName}
UninstallDisplayName={#AppName}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
; 默认装到 Program Files（需管理员），也允许用户选择仅为自己安装
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog
CloseApplications=yes

[Languages]
#if FileExists(AddBackslash(CompilerPath) + "Languages\ChineseSimplified.isl")
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"
#endif
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "{#SourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{autoprograms}\{cm:UninstallProgram,{#AppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#AppName}}"; Flags: nowait postinstall skipifsilent
