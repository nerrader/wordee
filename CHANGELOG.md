# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0]

- Change version number to v1.0.0 in the actual game.
- Change the windows `.exe` to a standalone `.zip` containing the `.exe`, this is to reduce the possibility of false positives from Windows Defender.
- Improve binary filenames by explicitly adding the OS name.
- Fix QRC resources test in CI.

## [1.0.0-beta.1]

- The core features of the app, including the GUI and game loop.
- A game stats board to view your overall state for your current game.
- The game-over pop up dialog window.
- The help menu to guide players.
- The give up button.
- Two different game modes you can play in: daily and unlimited.
- Logging through verbose mode and the locally stored .log file.
- Persistent daily game state across application sessions.

[1.0.0-beta.1]:<https://github.com/nerrader/wordee/releases/tag/v1.0.0-beta.1>
[1.0.0]: <https://github.com/nerrader/wordee/compare/v1.0.0-beta.1...v1.0.0>
