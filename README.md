## GenshinSim Manager

### Overview
**GenshinSim Manager** is a standalone desktop application (distributed as a `.exe`) built for Genshin Impact players to streamline managing and running combat simulations with [gcsim](https://github.com/genshinsim/gcsim), a powerful Monte Carlo simulation tool. Featuring an intuitive Tkinter-based GUI, it simplifies using the substat optimizer for Genshin Impact Theorycrafters

### What It Does
- **Project Management**: Set up projects with dedicated `configs` and `outputs` folders, with settings saved for quick restarts across sessions.
- **File Management**: Create, edit, save, rename, delete, or duplicate `.txt` configuration files directly in an easy-to-use interface.
- **Simulation Execution**: Run all project configs sequentially or a single file on demand, with results automatically displayed in your default browser.
- **User-Friendly Design**: Includes a sidebar for fast file navigation, real-time logging of simulation progress, and a "Terminate" button to halt processes when needed.
- **NOTICE**: Currently, GenshinSim Manager only uses the KQMs Stat Solver, as its purpose is to make Theorycrafting with KQMs substats easier.

### Why It’s Useful
This app makes [gcsim](https://github.com/genshinsim/gcsim)—a tool for calculating detailed combat stats like team DPS—easier to use for Theorycrafters. GenshinSim Manager offers a compact, all-in-one solution packaged in a single `.exe`, eliminating the need to wrestle with command-line interfaces.

![image](https://github.com/user-attachments/assets/d097568b-d98b-42bb-81c0-2dc7bfa0c491)

### Instructions
- **Download**: Get the latest `GenshinSimManager.exe` from the [Releases]([https://github.com/yourusername/yourrepo/releases](https://github.com/EnigWa/gcsim-manager/releases/tag/0.1.0)) page.
- **Run**: Double-click `GenshinSimManager.exe` to launch.
- **First Use**:
  1. **Base Folder**: Click "Browse" next to "Base Dir:" and choose a folder (e.g., `C:\genshinsim`).
  2. **gcsim Path**: Click "Browse" next to "gcsim Path:" and select your `gcsim.exe` (e.g., `C:\Tools\gcsim.exe`).
  3. **Project**: Enter a project name (e.g., `Hydro Wheelchair Book Scamge Klee Calcs`) and click "Create" to set up the project structure.
- **Managing Files**:
  - Click **"New"** to create a config file, edit it in the text area, and hit **"Save"**.
  - Double-click a file in the sidebar to load it, or use **"Rename"**, **"Delete"**, or **"Duplicate"** to manage files.
- **Running Simulations**:
  - **"Run All"**: Processes all configs in the `configs` folder one-by-one, showing logs and opening results in your browser.
  - **"Run"**: Simulates the currently loaded file individually with browser output.
  - **"Terminate"**: Stops any running simulations if they’re taking too long or you need to cancel.
- **Notes**:
  - You’ll need a working `gcsim.exe` from [gcsim’s GitHub](https://github.com/genshinsim/gcsim)
  - If the `.exe` doesn’t start, check if your antivirus is blocking it or if it needs admin permissions.
