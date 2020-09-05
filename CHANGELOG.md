# Changelog
All notable changes to this project will be documented in this file

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [Unreleased]

### Added
- Quit button to remove robot from the simulation

## [Release 7] - TBC

### Fixed
- Fixed bugs in 9 new sample worlds provided
- Fixed bugs in the world generator
- Fixed bugs regarding misidentification scoring
- Exit bonus scoring bonus now follows the correct rules
- Fixed a bug in the tutorial 2 sample code

### Added
- Added downward-facing light to the robot to prevent the colour sensor value from being affected by the shadows of objects and the red light of the heated victim

### Changed
- Simulation controls now automatically display on start up
- Changed the silver tile to CorrodedMetal
- Added shadow effects back to the swamp time
- Colour specification sample program updated

## [Release 6] - 2020-08-18

### Fixed
- Fixed error messages on startup

### Added
- Added front facing camera labelled `camera_centre`.

## [Release 5] - 2020-08-13

### Fixed
- Fixed bug with specific distance sensors only reading 0
- Fixed bug where heat sensors weren't reading correct values

## [Release 4] - 2020-08-13

### Added
- Robots are now placed into the world by the supervisor
- Export log of events after each game
- Positions of tiles, humans and obstacles randomly generated and automatically calculated based on tile scale
- Added an extra camera on the front of the robot. The cameras are labelled `camera_left` and `camera_right`.
- Start tile changes from green to white when the robots move off it and doesn't change back.

### Changed
- There is now no need to specify robot type when sending data for estimated victim detection and exit messages.   
For example from `struct.pack('i i i c', data, data1, data2, data3)` to `struct.pack('i i c', data, data1, data2)`
- Thermal victims radius decreased
- Tiles are now much smaller
- Victims are now much smaller
- Increased distance sensor range
- Moved colour camera to a less obstructive position to avoid shadows
- Moved starting tile to within the maze
- Removed automatic object recognition from the camera
- Heated victims are now only a point light. Removed white box.
- Changed robot sensor configuration internally however it shouldn't affect anything.
- Distance sensor values are now linear ranging from 0 to 0.8, with a max range of around 2x tile size.

### Removed
- Start 'bay' on outside of maze removed
- Robots not in generated world file
- Obstacles are not placed into the map due to smaller tile size

### Fixed
- Attempting to relocate with no robot no longer causes a crash

[Unreleased]: https://github.com/Shadow149/RescueMaze  
[Release 7]: 
[Release 6]: https://github.com/Shadow149/RescueMaze/releases/tag/v1.2.2
[Release 5]: https://github.com/Shadow149/RescueMaze/releases/tag/v1.2.1
[Release 4]: https://github.com/Shadow149/RescueMaze/releases/tag/v1.2
[Release 3]: https://github.com/Shadow149/RescueMaze/releases/tag/v1.1.1  
[Release 2]: https://github.com/Shadow149/RescueMaze/releases/tag/v1.1  
[Release 1]: https://github.com/Shadow149/RescueMaze/releases/tag/v1.0  
