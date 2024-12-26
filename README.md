# Blender Rigging Scripts

## Overview

This project contains a collection of Blender scripts designed to facilitate the rigging and animation process for 3D models, particularly focusing on skateboards and related animations. The scripts automate various tasks such as scene preparation, animation cleaning, and object management, making the rigging workflow more efficient.

## Features

- **Prep Scene**: Prepares the Blender scene by checking if the file is saved, grouping selected skateboard models, and setting up the armature.
- **Clean Animation**: Cleans up animations by removing unnecessary keyframes and exporting the final rigged model.
- **Add Board**: Imports skateboard rigs, applies constraints, and bakes animations for selected objects.
- **Remove Vertical Translation**: Adjusts the Z-location of selected objects to remove unwanted vertical movements.
- **User-Friendly Interface**: A custom panel in the Blender UI allows users to easily run scripts from a dedicated sidebar.

## Installation

1. Clone the repository or download the scripts folder.
2. Open Blender and navigate to `Edit > Preferences > Add-ons`.
3. Click on `Install...` and select the `__init__.py` file from the cloned/downloaded folder.
4. Enable the addon by checking the box next to its name in the Add-ons list.

## Usage

1. Open a Blender project and ensure your 3D models are ready for rigging.
2. Select the objects you want to work with.
3. Open the Scripts panel from the sidebar in the 3D Viewport.
4. Choose the desired script from the list and click to execute it.

### Available Scripts

- **Prep Scene**: Prepares the scene for rigging.
- **Clean Animation**: Cleans up the animation data.
- **Add Board**: Adds and rigs the skateboard model.
- **Remove Vertical Translation**: Adjusts the Z-axis position of selected objects.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or support, please contact the author at johann9616@gmail.com.