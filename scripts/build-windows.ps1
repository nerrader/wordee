# run this from the project root
# all the other configs are in the project root
uv run nuitka `
    --onefile `
    --windows-console-mode=disable `
    --windows-icon-from-ico=assets/wordee-icon.ico `
    src/wordee/main.py
