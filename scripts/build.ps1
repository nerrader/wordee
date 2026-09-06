# run this from the project root
uv run nuitka `
    --onefile `
    --enable-plugin=pyside6 `
    --windows-console-mode=disable `
    --windows-icon-from-ico=assets/wordee-icon.ico `
    src/wordee/main.py
