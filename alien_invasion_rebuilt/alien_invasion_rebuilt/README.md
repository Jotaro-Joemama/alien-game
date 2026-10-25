# Alien Invasion — rebuilt project

A small Pygame game using the images in `Assets/images`. It includes a movable ship, bullets, an alien fleet, fleet edge movement, bullet/alien collisions with `pygame.sprite.groupcollide()`, lives, and a restart screen.

## Run

Install Python 3.12 or another version compatible with Pygame 2.6.1, then install dependencies:

```text
python -m pip install -r requirements.txt
```

Run the game from this folder:

```text
python alien_invasion.py
```

## Controls

- Left/right arrows or A/D: move
- Space: fire
- R: restart after game over
- Q or Escape: quit

## Files

- `alien_invasion.py`: main game loop and game rules
- `settings.py`: screen and gameplay settings
- `ship.py`: player ship
- `bullet.py`: bullets
- `alien.py`: alien sprite
- `Assets/`: supplied images, fonts, sound files, and score data

This is a rebuilt foundation guided by the general Chapter 12–13 topics; the exact missing Blackboard Part 2 checklist was not available.
