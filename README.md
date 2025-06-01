# cameraApertureFix for Autodesk Maya
This script sets a Maya camera’s aperture using presets for common cameras or custom values. It automatically adjusts the focal length to maintain your composition and preserve the correct field of view.

---
### [Watch how it works on YouTube](https://youtu.be/XZg9ECAe6HI)
[![Watch the video](https://img.youtube.com/vi/XZg9ECAe6HI/maxresdefault.jpg)](https://youtu.be/XZg9ECAe6HI)


---

## Features

-   **Unit Conversion:** Switch between **Inch** and **Millimeter** for aperture input and display.
-   **Aspect Ratio Control:**
    -   **Maintain Original Aspect Ratio:** Automatically calculates vertical aperture to preserve the camera's current aspect ratio when changing horizontal aperture.
    -   **Preset Aspect Ratio:** When a preset is selected and "Maintain Original Aspect Ratio" is off, uses the preset's defined horizontal and vertical apertures, potentially changing the aspect ratio.
    -   **Custom Aspect Ratio:** Manually define both horizontal and vertical apertures when "None" preset is selected and "Maintain Original Aspect Ratio" is off.
-   **FOV Preservation:**
    -   **Adjust Focal Length to Maintain FOV:** If checked, the script automatically adjusts the camera's focal length to compensate for changes in the horizontal film aperture, effectively maintaining the field of view.
    -   Supports animated focal length.

## Why it's Useful

CameraApertureFix helps make sure your Maya camera matches real-world film back sizes. It adjusts the focal length to keep the composition framing accurate. Getting the film back right is important not only for realistic shots but also for clear communication during matchmove, previs, layout, and animation.

For example, if the director requests a shot with a specific lens, matching the camera settings allows you to use the real lens size and makes it easier to communicate using the same visual language as in the real world. For a matchmoved camera, correct settings also help during QC by making it easier to spot issues when the real values differ too much. This tool allows you to convert a mismatched filmback and view the adjusted lens size.

## How to Use

1.  **Open Maya Script Editor:** In Autodesk Maya, open the Script Editor (**Windows → General Editors → Script Editor**).
2.  **Open Script:** In the Script Editor, go to **File → Open Script...** and navigate to select the downloaded `.py` file.
3.  **Set to Python:** Ensure the tab in the Script Editor is set to "Python".
4.  **Execute:** Execute the script by clicking the "Execute All" button (looks like a double play icon) or by pressing **Ctrl + Enter** (Windows/Linux) or **Cmd + Enter** (macOS) in the script editor's input pane.

The "CameraApertureFix" UI window will appear. Select a camera in your scene and click "Refresh" in the script's UI to load its data.
