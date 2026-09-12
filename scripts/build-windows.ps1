# run this from the project root
# all the other configs are in the project root
uv run nuitka `
    --mode=app `
    --windows-console-mode=disable `
    --windows-icon-from-ico=assets/wordee-icon.ico `
    src/wordee/main.py

# rename the .exe
Rename-Item `
    "dist/WORDEE.exe" `
    "WORDEE-x86_64.exe"

# remove all useless build junk
Remove-Item "dist/main.build" -Recurse -Force
Remove-Item "dist/main.onefile-build" -Recurse -Force

Copy-Item `
    "assets/README-windows.txt" `
    "dist/README.md"

# zip the WORDEE-x86_64
Compress-Archive `
    -Path "dist/*" `
    -DestinationPath "WORDEE-x86_64.zip" `
    -Force

# remove all items in dist/
Remove-Item -Path "dist/*" -Recurse -Force

# then move the .zip there
Move-Item `
    "WORDEE-x86_64.zip" `
    "dist/WORDEE-x86_64.zip"
