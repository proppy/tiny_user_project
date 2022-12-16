# Tiny User Project

Template for submitting [TinyTapeout](https://tinytapeout.com) based projects to the [Open MPW shuttle](https://developers.google.com/silicon) program.

## Usage

1. [Generate](https://github.com/proppy/tiny_user_project/generate) a new project based on this template.

1. [Set GitHub Pages](https://tinytapeout.com/faq/#my-github-action-is-failing-on-the-pages-part) `Sources` as `GitHub Actions`.

1. If using [Wokwi](https://wokwi.com/):

   - Reuse or create a new [Wokwi](https://wokwi.com/projects/339800239192932947) project.
   - Edit [`info.yaml`](info.yaml):
     - In `project`:
       - Update `wokwi_id` with the last component of the Wokwi URL.
     - In `documentation`:
       - Update `inputs` to document the input wire of your project.
       - Update `outputs` to document the output wire of your project.


1. If using Verilog:

   - Add your HDL code in [`verilog/rtl/`](verilog/rtl/).
   - Edit [`info.yaml`](info.yaml):
     - In `project`:
       - Set `wokwi_id` to `0`.
       - Uncomment and update `top_module` to match your top-level module.
       - Uncomment and list your Verilog sources in `src_files` (paths relative to the root of the repository).
     - In `documentation`:
       - Update `inputs` to document the input wire of your top-level module.
       - Update `outputs` to document the output wire of your top-level module.

1. Commit, push and check the [![user_project_ci](https://github.com/proppy/tiny_caravel_user_project/actions/workflows/user_project_ci.yml/badge.svg)](https://github.com/proppy/tiny_caravel_user_project/actions/workflows/user_project_ci.yml) workflow summary (if successful a new commit including the hardened files will be automatically created).

1. [Submit](https://platform.efabless.com/projects/create?project_definition=Open+MPW&shuttle=MPW-8) your project github repository to the next [Open MPW shuttle](https://platform.efabless.com/shuttles/MPW-8).
