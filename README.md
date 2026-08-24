## Eartrumpet: Rest for the eyes, enrichment for the ears.
Nothing too serious. It's a hackathon project!

### What it's for
Do you subscribe to newsletters that arrive only as text? Are your retinas overworked and your ears chronically bored?

Eartrumpet turns text items from a source RSS feed into audio items in a podcast feed. The whole setup is containerized and elf-hosted. No data is sent to a third party.

### Component services
- `config`: Manages source and destination feeds, per-feed settings, and global settings
- `intake`: Reads text items from RSS feeds
- `prepare`: Optimizes text items for improved TTS performance
- `tts`: Performs the actual TTS work
  - Currently using supertonic-3 (no longer officially supported, but yolo)
- `store`: Organizes the audio artifacts
- `serve`: Makes the destination feeds available to podcatchers
- `tidy`: Cleans up old audio artifacts


