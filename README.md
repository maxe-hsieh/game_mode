# Game Mode

## Introduction

When you are playing games (especially action games), you often need to hold down keys, such as holding down the arrow keys to move, etc. At this time, you will find that NVDA is silent, because NVDA's principle is that when any key is pressed, it will instantly interrupt the current reading, and holding down the key is like telling NVDA to interrupt any reading at any time. This results in a keyboard event that interrupts the moment a new message is about to be read.

For these reasons, it was time to add a new mode for playing games, and so the NVDA game mode was born.

## Features

You can freely switch the game mode on or off.

When Game Mode is turned on, the NVDA reading principle changes as follows:

1. When a key is pressed, the voice is not interrupted, but only recorded that the key has been pressed.
2. When there is a new message to be read aloud: If a key has been pressed, the current voice will be interrupted before the new content is read aloud, otherwise the new content will be queued up and read aloud after the current content has been read aloud.

Other changes related to any game or add-on are listed below:

1. Fixed the bug that when World Voice uses SAPI5, the speech will always be interrupted when pressing any keys.
2. Fixed a bug in the game 《俠行天下》 where pressing tab would say blank.

## Operation

You can switch the game mode on/off by pressing NVDA+SHIFT+G. This gesture can also be changed during the input gestures.

---
