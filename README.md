# Tiny User Project

Template for submitting [TinyTapeout](https://tinytapeout.com) based projects to the [Open MPW shuttle](https://developers.google.com/silicon) program.

## Usage

1. [Generate](https://github.com/proppy/tiny_user_project/generate) a new project based on this template

1. [Set GitHub Pages](settings/pages) `Sources` as `GitHub Actions`.

1. Create a new [Wokwi](https://wokwi.com/projects/339800239192932947) project and update [`info.yaml`](info.yaml) with your `wokwi_id`.

1. Commit, push and check the [![user_project_ci](https://github.com/proppy/tiny_caravel_user_project/actions/workflows/user_project_ci.yml/badge.svg)](https://github.com/proppy/tiny_caravel_user_project/actions/workflows/user_project_ci.yml) workflow summary (if successful a new commit including the hardened files will be automatically created).

1. Submit your project github repository to the next [Open MPW shuttle](https://platform.efabless.com/shuttles/GFMPW-0).
