# blaqpad

<img width="1204" height="932" alt="image" src="https://github.com/user-attachments/assets/a0bc1c4b-0f70-4229-bb17-6d59f43ed7d3" />

A "powerful" looper and sampler designed for Novation Launchpad controllers. Create loops, assign samples, record your sessions, and manage your projects.

THIS HAS BEEN TESTED WITH A NOVATION LAUNCHPAD MINI ON MANJARO, FEEDBACK IS APPRECIATED!
---

## Features

- **Assign sounds** – click any pad, choose a WAV file, and play it with a touch.
- **4 loop channels** – each channel can record, play, stop, clear, and mute its own loop.
- **Global controls** – toggle overlap mode, control master volume and pitch (can be mapped to Launchpad buttons).
- **Learn Control** – map any Launchpad control button to an action: stop, volume up/down, pitch up/down, stop loop recording, toggle session recording.
- **Session Recording** – record everything you play (pads + loops) to a high‑quality WAV file, no external drivers needed.
- **Session Management** – export/import your entire setup (sounds, mappings, learned controls) as a `.bqb` file. Create new sessions or reload the last used one.

---

## How to use

### Assigning sounds
- Click any pad → choose a WAV file. The pad turns blue.
- Press the pad to play its sound.

### Loop channels (4 independent tracks)
- **Record** – press Record on a channel, play pads, then press Record again to stop recording.
- **Play** – starts looping the recorded pattern.
- **Stop** – stops playback.
- **Clear** – erases the loop.
- **Mute** – silences the channel’s loop (but it still records if you’re recording the session).

### Global controls
- **Overlap** – when OFF, stops the previous sound before playing a new one (monophonic). When ON, sounds can overlap.
- **Volume / Pitch** – can be controlled by assigned buttons (see **Learn Control** below).

### Learn Control
1. Click **Learn Control**.
2. Choose an action from the dropdown (stop, volume up/down, pitch up/down, stop recording, toggle session recording).
3. Press a Launchpad control button (the round buttons around the pads).  
   That button will now trigger the chosen action.

### Session Recording
- Click **Session Rec** to start recording. Every pad hit and every loop note is captured.
- Click **Session Rec** again to stop. The recording is rendered to a WAV file named `session_record_YYYYMMDD_HHMMSS.wav` in the current directory.

### Session Management (Sesh Options)
- **Export** – saves all pad assignments, learned controls, and the WAV files into a `.bqb` file. You’ll be prompted for a session name.
- **Import** – loads a previously saved `.bqb` session.
- **New Session** – clears all mappings and loops, starting fresh.
- **Load Last Session** – restores the most recently imported session.

### Tips
- You can record loops **while** a global session recording is active – everything is captured in the final WAV.
- Muted channels still record their events if you are recording the session; they just won’t be heard during playback.
- Loops are stored per channel, independent of the main session recording, so you can change session recordings without losing your loop patterns.

---

## Credits

Created by **blaqberry**.  
Built with PyQt6, pygame, mido, and NumPy.

---

## License

This software is created by **blaqberry**.  


You are free to do with this software what you want, as long as the credit requirement is respected.
If not you will personally owe 20 bucks which i will use to spend on pot money for more projects like this /j
