# Nebula Assault

**Nebula Assault** is a retro-style space shooter game developed using Python and Pygame. Players control a spaceship and must survive waves of enemy ships, shoot down enemies, and eventually defeat a boss with erratic movements and homing bullets.

![Game Screenshot](res/images/background.png)

## Features

- **Finger Tracking Integration**: Use finger tracking to control the spaceship and shoot. (Requires webcam)
- **Enemies and Boss**: Battle against waves of enemies and a powerful boss with unpredictable movement patterns.
- **Sound Effects**: Engaging sound effects for explosions, firing, and player damage.
- **Scoring System**: Track your score and lives during the game.
- **Challenging Gameplay**: Face enemies that shoot back, and watch out for the homing bullets from the boss.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Controls](#controls)
- [Dependencies](#dependencies)
- [Game Assets](#game-assets)
- [Credits](#credits)
- [License](#license)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Arya0077/Nebula-Assault.git
    ```

2. Navigate to the project directory:
    ```bash
    cd nebula-assault
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Ensure that you have a webcam for finger tracking.

## Usage

Run the game using the following command:

```bash
python main.py
```

# Controls
The game uses finger tracking for movement and shooting.

- **Move:** Use your index finger to move the spaceship horizontally.
- **Shoot:** Make a gun pose to shoot bullets.

# Dependencies
- **Pygame:** Used for game development.
- **OpenCV:** For finger tracking.
- **Mediapipe:** For hand detection and finger tracking.

## Install dependencies using:
```bash
pip install pygame opencv-python mediapipe
```
# Game Assets
- **Background Image:** Space-themed background.
- **Spaceship:** Player-controlled spaceship image.
- **Enemies:** Alien enemy images with random movement.
- **Boss:** Final boss with homing bullets.
- **Sound Effects:** Laser shots, explosions, and more for immersive gameplay

