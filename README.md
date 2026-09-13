BACKUP DOODLE 2022 ASSETS/GAMEDATA/SCRIPTS
This repository uses original servers (still avaible)
For the future, if Google turn off game-servers.

The IA give the next information for the future 
(For change WebSocket,Server replacement):

# Google Doodle Halloween 2022 - WebSocket Preservation
Preservation project for the original Google Doodle Halloween 2022 / The Great Ghoul Duel 2, version v81123.
The original game client has been preserved and currently runs from GitHub Pages while still connecting to Google's original WebSocket infrastructure.

## Current architecture
Client
→ Google Matchmaker
→ Game Server

The client uses WebSockets (`wss://`) and binary messages.

## Known endpoints

Matchmaker:
wss://matchmaker.prod.h22.cloud.doodles.goog
Example game server observed during testing:
wss://gs.h22-usc-uc1.h22.cloud.doodles.goog/h22-usc-uc1-dgs-vspk2-g7xh9
The game client successfully connected to the original servers and completed the handshake from our own hosting.

## WebSocket implementation
The original client contains:

- MatchmakerClient
- MatchmakerClientMessage
- MatchmakerServerMessage
- MatchmakerServerError
- MatchmakerDisconnectedError
- MatchmakerWebSocketError

The protocol uses binary WebSocket messages with ArrayBuffer / Uint8Array.

The Matchmaker receives game mode information such as:

GAME_MODE:<name>

and returns information including an address for the game server.

The client also implements ping/pong, connection timeouts and disconnect handling.

## Future goal

If Google's original servers are eventually shut down, replace only the WebSocket infrastructure while keeping the original game client intact.

Target architecture:

Client
→ Custom Matchmaker
→ Custom Game Server

The graphics, maps, sprites, audio and game logic should remain unchanged.

## Reverse engineering plan

Before replacing the Google servers, capture a complete real session while the original infrastructure is still available:

- Matchmaker connection
- Handshake
- GAME_MODE
- Match found
- Game server address
- Game server connection
- Game server handshake
- Gameplay messages
- End of match
- Results
- Disconnect

Record every WebSocket message with:

- timestamp
- direction
- WebSocket endpoint
- message size
- raw hexadecimal data
- raw Base64 data

The first step should be decoding the real binary protocol, not immediately writing a replacement server.
