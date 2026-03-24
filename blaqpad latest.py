import sys
import os
import json
import time
import threading
import shutil
import zipfile
import tempfile
import wave
import datetime
import base64
import mido
import pygame
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QFileDialog, QGridLayout,
    QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QDialog,
    QLineEdit, QMessageBox, QTabWidget, QTextEdit, QCheckBox, QSplashScreen
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QPixmap

# --- Boot logo (base64 image provided by user) ---
SPLASH_BASE64 = "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"

def get_splash_pixmap():
    data = base64.b64decode(SPLASH_BASE64)
    pixmap = QPixmap()
    pixmap.loadFromData(data, "PNG")
    return pixmap

# --- Icon embedded (same as splash) ---
def get_icon():
    pixmap = get_splash_pixmap()
    if not pixmap.isNull():
        return QIcon(pixmap)
    return None
# --- Audio init ---
pygame.mixer.init(frequency=44100, channels=2, size=-16, buffer=512)
pygame.mixer.set_num_channels(64)   # Allocate enough channels for loops and one‑shot sounds
SAMPLE_RATE = 44100

# --- File handling ---
MAPPING_FILE = "mapping.json"
CONTROL_FILE = "controls.json"
LAST_SESSION_FILE = "last_session.txt"
SESSIONS_FOLDER = "sessions"
LAUNCHPAD_NAME = "Launchpad"
SETTINGS_FILE = "settings.json"

if not os.path.exists(SESSIONS_FOLDER):
    os.makedirs(SESSIONS_FOLDER)

# --- Load/save settings ---
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {}

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

# --- Help / About dialog ---
HELP_TEXT = """
<strong>blaqpad – Launchpad Looper</strong><br/><br/>

<strong>Assigning sounds</strong><br/>
• Click any pad → choose a WAV file. The pad lights up blue.<br/>
• Press a pad to play its sound.<br/><br/>

<strong>Loop channels (4 independent tracks)</strong><br/>
• Click Record on a channel → play pads → click Record again to stop.<br/>
• Play – loops what you recorded.<br/>
• Stop – stops playback.<br/>
• Clear – erases the loop.<br/>
• Mute – silences the channel’s loop.<br/><br/>

<strong>Global controls</strong><br/>
• Overlap – when OFF, stops previous sound before playing a new one.<br/>
• Volume / Pitch – controlled by assigned buttons (see Learn Control).<br/><br/>

<strong>Learn Control</strong><br/>
1. Click Learn Control.<br/>
2. Choose an action (stop, volume, pitch, stop recording, toggle session recording).<br/>
3. Press a Launchpad control button (the round buttons around the pads).<br/>
   – That button will now trigger the action.<br/><br/>

<strong>Session Recording</strong><br/>
• Click Session Rec → start playing. All pad hits and loop notes are recorded.<br/>
• Click Session Rec again → saves a session_record_YYYYMMDD_HHMMSS.wav file with your entire performance.<br/><br/>

<strong>Session Management (Sesh Options)</strong><br/>
• Export – saves all pad assignments, learned controls, and the WAV files into a .bqb file.<br/>
• Import – loads a previously saved session.<br/>
• New Session – clears everything and starts fresh.<br/>
• Load Last Session – reloads the last imported session.<br/><br/>

<strong>Tips</strong><br/>
• You can record loops while a session recording is active – everything will be captured.<br/>
• Muted channels still record their events, they just won't play back.<br/>
• Loops are stored per channel, independent of the main session recording.<br/>
"""

ABOUT_TEXT = """
<strong>blaqpad – Launchpad Looper</strong><br/>
Version 1.0.1 i guess...<br/><br/>
A "powerful" looper and sampler designed for Novation Launchpad controllers. (Specifically LP Mini)<br/>
Create loops, assign samples, record your sessions, and manage your projects.<br/><br/>
Created by blaqberry.<br/>
© 2026 – Built with PyQt6, pygame, and mido.<br/><br/>
For support, visit <a href="https://github.com/blaqberry/blaqpad">github.com/blaqberry/blaqpad</a><br/>
"""

class HelpAboutDialog(QDialog):
    def __init__(self, parent=None, show_checkbox=True):
        super().__init__(parent)
        self.setWindowTitle("blaqpad Help & About")
        self.setMinimumSize(600, 500)
        layout = QVBoxLayout()

        tabs = QTabWidget()
        help_tab = QTextEdit()
        help_tab.setHtml(HELP_TEXT)
        help_tab.setReadOnly(True)
        about_tab = QTextEdit()
        about_tab.setHtml(ABOUT_TEXT)
        about_tab.setReadOnly(True)
        tabs.addTab(help_tab, "How to use")
        tabs.addTab(about_tab, "About")
        layout.addWidget(tabs)

        self.dont_show_checkbox = QCheckBox("Don't launch this on startup nomo")
        self.dont_show_checkbox.setChecked(False)
        layout.addWidget(self.dont_show_checkbox)

        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn)

        self.setLayout(layout)

    def should_skip_startup(self):
        return self.dont_show_checkbox.isChecked()

# --- Global state ---
sound_map = {}
control_map = {}
loaded_sounds = {}
raw_arrays = {}
current_volume = 1.0
current_pitch = 1.0

# --- Audio functions ---
def load_sound(note, path):
    try:
        snd = pygame.mixer.Sound(path)
        snd.set_volume(current_volume)
        loaded_sounds[note] = snd
        raw_arrays[note] = pygame.sndarray.array(snd).astype(np.int16)
    except Exception as e:
        print(f"Error loading {path}: {e}")

def reload_all_sounds():
    global loaded_sounds, raw_arrays
    loaded_sounds.clear()
    raw_arrays.clear()
    for note, path in sound_map.items():
        if path and os.path.exists(path):
            load_sound(note, path)

def play_sound_with_params(note, pitch, volume):
    """Play a note with given pitch and volume. Returns the mixer channel used."""
    if note not in raw_arrays:
        return None
    arr = raw_arrays[note]
    indices = np.arange(0, len(arr), 1 / pitch)
    indices = indices[indices < len(arr)].astype(int)
    resampled = arr[indices]
    snd = pygame.sndarray.make_sound(resampled)
    snd.set_volume(volume)
    channel = pygame.mixer.find_channel()
    if channel:
        channel.play(snd)
        return channel
    else:
        snd.play()
        return None

def play_sound_with_pitch(note, pitch=1.0):
    """Legacy: use current global volume."""
    return play_sound_with_params(note, pitch, current_volume)

# --- Session recording (internal) ---
session_recording = False
session_start_time = 0.0
session_events = []  # each event: (time_offset, note, pitch, volume)

def render_session_to_wav(events, filename=None):
    if not events:
        return None
    total_duration = 0
    for t, note, pitch, volume in events:
        if note in raw_arrays:
            arr = raw_arrays[note]
            indices = np.arange(0, len(arr), 1 / pitch)
            indices = indices[indices < len(arr)].astype(int)
            dur = len(indices) / SAMPLE_RATE
            end_time = t + dur
            if end_time > total_duration:
                total_duration = end_time
    total_samples = int(total_duration * SAMPLE_RATE)
    mix_buffer = np.zeros((total_samples, 2), dtype=np.int16)

    for t, note, pitch, volume in events:
        if note not in raw_arrays:
            continue
        arr = raw_arrays[note]
        indices = np.arange(0, len(arr), 1 / pitch)
        indices = indices[indices < len(arr)].astype(int)
        resampled = arr[indices] * volume  # apply volume
        start_sample = int(t * SAMPLE_RATE)
        end_sample = min(start_sample + len(resampled), total_samples)
        samples_to_mix = end_sample - start_sample
        if samples_to_mix > 0:
            mix_buffer[start_sample:end_sample] += resampled[:samples_to_mix]

    max_val = np.max(np.abs(mix_buffer))
    if max_val > 0:
        mix_buffer = (mix_buffer * (0.9 * 32767 / max_val)).astype(np.int16)

    if filename is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"session_record_{timestamp}.wav"
    wf = wave.open(filename, 'wb')
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(mix_buffer.tobytes())
    wf.close()
    return filename

# --- Channel data ---
NUM_CHANNELS = 4
channels = []
for _ in range(NUM_CHANNELS):
    channels.append({
        "events": [],          # each event: (time_offset, note, pitch, volume)
        "duration": 0.0,
        "recording": False,
        "playing": False,
        "stop_event": threading.Event(),
        "thread": None,
        "mute": False,
        "active_channels": [],
    })

# --- Save mapping ---
def save_mapping():
    with open(MAPPING_FILE, "w") as f:
        json.dump(sound_map, f)
    with open(CONTROL_FILE, "w") as f:
        json.dump(control_map, f)

# --- Session Options Dialog ---
class SessionOptionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Session Options")
        self.setFixedSize(350, 250)
        layout = QVBoxLayout()

        new_btn = QPushButton("New Session (Clear All)")
        new_btn.clicked.connect(self.new_session)
        layout.addWidget(new_btn)

        load_last_btn = QPushButton("Load Last Session")
        load_last_btn.clicked.connect(self.load_last_session)
        layout.addWidget(load_last_btn)

        export_layout = QHBoxLayout()
        export_layout.addWidget(QLabel("Session name:"))
        self.session_name_edit = QLineEdit()
        export_layout.addWidget(self.session_name_edit)
        self.export_btn = QPushButton("Export")
        self.export_btn.clicked.connect(self.export_session)
        export_layout.addWidget(self.export_btn)
        layout.addLayout(export_layout)

        # Connect Enter key to export
        self.session_name_edit.returnPressed.connect(self.export_btn.click)

        import_btn = QPushButton("Import Session (.bqb)")
        import_btn.clicked.connect(self.import_session)
        layout.addWidget(import_btn)

        self.setLayout(layout)

    def new_session(self):
        global sound_map, control_map
        sound_map.clear()
        control_map.clear()
        save_mapping()
        reload_all_sounds()
        for ch in channels:
            ch["events"] = []
            ch["duration"] = 0.0
            ch["recording"] = False
            ch["playing"] = False
            ch["stop_event"].set()
            ch["stop_event"].clear()
            if ch["thread"] and ch["thread"].is_alive():
                ch["stop_event"].set()
                ch["thread"].join(timeout=0.1)
            ch["thread"] = None
            ch["mute"] = False
            for c in ch["active_channels"]:
                if c:
                    c.stop()
            ch["active_channels"].clear()
        parent = self.parent()
        if parent and hasattr(parent, 'reset_ui'):
            parent.reset_ui()
        QMessageBox.information(self, "Success", "New session created. All data cleared.")

    def load_last_session(self):
        if not os.path.exists(LAST_SESSION_FILE):
            QMessageBox.warning(self, "Warning", "No last session found.")
            return
        with open(LAST_SESSION_FILE, 'r') as f:
            last_path = f.read().strip()
        if not last_path or not os.path.exists(last_path):
            QMessageBox.warning(self, "Warning", "Last session file not found.")
            return
        self.load_session_from_path(last_path)

    def load_session_from_path(self, filepath):
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                with zipfile.ZipFile(filepath, 'r') as zipf:
                    zipf.extractall(tmpdir)
                mapping_path = os.path.join(tmpdir, 'mapping.json')
                controls_path = os.path.join(tmpdir, 'controls.json')
                if not os.path.exists(mapping_path) or not os.path.exists(controls_path):
                    QMessageBox.critical(self, "Error", "Invalid session file: missing mapping.json or controls.json")
                    return
                with open(mapping_path, 'r') as f:
                    new_mapping = json.load(f)
                new_sound_map = {int(k): v for k, v in new_mapping.items()}
                session_folder = os.path.join(SESSIONS_FOLDER, os.path.splitext(os.path.basename(filepath))[0])
                if os.path.exists(session_folder):
                    shutil.rmtree(session_folder)
                os.makedirs(session_folder)
                new_sound_map_abs = {}
                for note, rel_path in new_sound_map.items():
                    src = os.path.join(tmpdir, os.path.basename(rel_path))
                    if os.path.exists(src):
                        dst = os.path.join(session_folder, os.path.basename(rel_path))
                        shutil.copy2(src, dst)
                        new_sound_map_abs[note] = dst
                    else:
                        print(f"Warning: sound file {rel_path} not found in zip")
                        new_sound_map_abs[note] = ""
                with open(controls_path, 'r') as f:
                    new_control_map = {int(k): v for k, v in json.load(f).items()}
                global sound_map, control_map
                sound_map.clear()
                sound_map.update(new_sound_map_abs)
                control_map.clear()
                control_map.update(new_control_map)
                save_mapping()
                reload_all_sounds()
                with open(LAST_SESSION_FILE, 'w') as f:
                    f.write(filepath)
                parent = self.parent()
                if parent and hasattr(parent, 'update_button_styles'):
                    parent.update_button_styles()
                    parent.reset_ui()
                QMessageBox.information(self, "Success", "Session imported successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Import failed: {str(e)}")

    def export_session(self):
        name = self.session_name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Warning", "Please enter a session name.")
            return
        filename = f"{name}.bqb"
        filepath = os.path.join(os.getcwd(), filename)
        try:
            with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
                with open(MAPPING_FILE, 'r') as f:
                    zipf.writestr('mapping.json', f.read())
                with open(CONTROL_FILE, 'r') as f:
                    zipf.writestr('controls.json', f.read())
                added = set()
                for note, path in sound_map.items():
                    if path not in added and os.path.exists(path):
                        zipf.write(path, os.path.basename(path))
                        added.add(path)
            QMessageBox.information(self, "Success", f"Session exported to {filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")

    def import_session(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Import Session", "", "BQB Files (*.bqb)")
        if not filepath:
            return
        self.load_session_from_path(filepath)

# --- Main GUI ---
class LaunchpadGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("blaqpad")
        # Set window icon from embedded data
        icon = get_icon()
        if icon is not None:
            self.setWindowIcon(icon)

        self.setFixedSize(1200, 900)
        self.allow_overlap = True
        self.learn_mode = False
        self.recording_channel = None
        self.record_start_time = 0.0
        self.oneshot_channels = []  # track one‑shot playback channels for overlap

        main_layout = QVBoxLayout()

        # Top control row
        top_controls = QHBoxLayout()
        self.overlap_btn = QPushButton("Overlap: ON")
        self.overlap_btn.clicked.connect(self.toggle_overlap)
        top_controls.addWidget(self.overlap_btn)

        self.learn_btn = QPushButton("Learn Control")
        self.learn_btn.clicked.connect(self.toggle_learn)
        top_controls.addWidget(self.learn_btn)

        self.action_dropdown = QComboBox()
        self.action_dropdown.addItems(["stop", "vol_up", "vol_down", "pitch_up", "pitch_down", "stop_recording", "toggle_session_recording"])
        top_controls.addWidget(self.action_dropdown)

        self.status_label = QLabel("")
        top_controls.addWidget(self.status_label)

        self.session_rec_btn = QPushButton("Session Rec")
        self.session_rec_btn.setCheckable(True)
        self.session_rec_btn.clicked.connect(self.toggle_session_recording)
        top_controls.addWidget(self.session_rec_btn)

        self.sesh_btn = QPushButton("Sesh Options")
        self.sesh_btn.clicked.connect(self.open_session_dialog)
        top_controls.addWidget(self.sesh_btn)

        self.help_btn = QPushButton("Help")
        self.help_btn.clicked.connect(self.open_help_dialog)
        top_controls.addWidget(self.help_btn)

        main_layout.addLayout(top_controls)

        # Pad grid
        grid = QGridLayout()
        grid.setSpacing(8)
        self.buttons = {}
        for row in range(8):
            for col in range(8):
                note = row * 16 + col
                btn = QPushButton("")
                btn.setFixedSize(60, 60)
                btn.setStyleSheet(self.default_style())
                btn.pressed.connect(self.make_press_handler(note))
                btn.released.connect(self.make_release_handler(note))
                btn.clicked.connect(self.make_assign_handler(note))
                grid.addWidget(btn, row, col)
                self.buttons[note] = btn
        main_layout.addLayout(grid)

        # Channel controls
        channel_layout = QHBoxLayout()
        self.channel_widgets = []
        for i in range(NUM_CHANNELS):
            vbox = QVBoxLayout()
            vbox.setAlignment(Qt.AlignmentFlag.AlignTop)

            lbl = QLabel(f"Channel {i+1}")
            vbox.addWidget(lbl)

            rec_btn = QPushButton("Record")
            rec_btn.setCheckable(True)
            rec_btn.clicked.connect(lambda checked, ch=i: self.record_channel(ch, checked))
            vbox.addWidget(rec_btn)

            play_btn = QPushButton("Play")
            play_btn.clicked.connect(lambda _, ch=i: self.start_loop(ch))
            vbox.addWidget(play_btn)

            stop_btn = QPushButton("Stop")
            stop_btn.clicked.connect(lambda _, ch=i: self.stop_loop(ch))
            vbox.addWidget(stop_btn)

            clear_btn = QPushButton("Clear")
            clear_btn.clicked.connect(lambda _, ch=i: self.clear_loop(ch))
            vbox.addWidget(clear_btn)

            mute_btn = QPushButton("Mute")
            mute_btn.setCheckable(True)
            mute_btn.clicked.connect(lambda checked, ch=i: self.toggle_mute(ch, checked))
            vbox.addWidget(mute_btn)

            time_label = QLabel("0.0 s")
            vbox.addWidget(time_label)

            channel_layout.addLayout(vbox)
            self.channel_widgets.append({
                "record_btn": rec_btn,
                "play_btn": play_btn,
                "stop_btn": stop_btn,
                "clear_btn": clear_btn,
                "mute_btn": mute_btn,
                "time_label": time_label,
            })

        main_layout.addLayout(channel_layout)

        # Status bar
        status_bar = QHBoxLayout()
        self.volume_label = QLabel(f"Volume: {current_volume:.1f}")
        self.pitch_label = QLabel(f"Pitch: {current_pitch:.1f}")
        self.session_rec_status = QLabel("")
        status_bar.addWidget(self.volume_label)
        status_bar.addWidget(self.pitch_label)
        status_bar.addWidget(self.session_rec_status)
        main_layout.addLayout(status_bar)

        self.setLayout(main_layout)

        # MIDI out
        self.midi_out = None
        for name in mido.get_output_names():
            if LAUNCHPAD_NAME.lower() in name.lower():
                self.midi_out = mido.open_output(name)
                break

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(100)

        # Show help on first launch if not skipped
        self.check_show_help()

    # --- UI styles ---
    def default_style(self):
        return "background-color: #1a1a1a; border-radius: 12px;"

    def active_style(self):
        return "background-color: #00ff88; border-radius: 12px;"

    def assigned_style(self):
        return "background-color: #3a66ff; border-radius: 12px;"

    def update_button_styles(self):
        for note, btn in self.buttons.items():
            if note in sound_map:
                btn.setStyleSheet(self.assigned_style())
            else:
                btn.setStyleSheet(self.default_style())

    def reset_ui(self):
        for w in self.channel_widgets:
            if w["record_btn"].isChecked():
                w["record_btn"].setChecked(False)
        self.status_label.setText("")
        for i in range(NUM_CHANNELS):
            self.channel_widgets[i]["time_label"].setText("0.0 s")
        self.update_button_styles()

    # --- Help dialog handling ---
    def check_show_help(self):
        settings = load_settings()
        if not settings.get("skip_startup_help", False):
            self.open_help_dialog(show_checkbox=True)

    def open_help_dialog(self, show_checkbox=False):
        dlg = HelpAboutDialog(self, show_checkbox=show_checkbox)
        if dlg.exec():
            if show_checkbox and dlg.should_skip_startup():
                settings = load_settings()
                settings["skip_startup_help"] = True
                save_settings(settings)

    # --- Button handlers ---
    def make_assign_handler(self, note):
        def handler():
            file_path, _ = QFileDialog.getOpenFileName(self, "Select WAV file", "", "WAV Files (*.wav)")
            if file_path:
                sound_map[note] = file_path
                load_sound(note, file_path)
                self.buttons[note].setStyleSheet(self.assigned_style())
                save_mapping()
        return handler

    def make_press_handler(self, note):
        def handler():
            self.buttons[note].setStyleSheet(self.active_style())
            if not self.allow_overlap:
                # Stop only one‑shot channels, not loops
                for ch in self.oneshot_channels:
                    ch.stop()
                self.oneshot_channels.clear()
            if note in loaded_sounds:
                channel = play_sound_with_params(note, current_pitch, current_volume)
                if channel and not self.allow_overlap:
                    # Remember this channel for later overlap‑off stopping
                    self.oneshot_channels.append(channel)

            if self.recording_channel is not None:
                ch = channels[self.recording_channel]
                if ch["recording"]:
                    t = time.time() - self.record_start_time
                    ch["events"].append((t, note, current_pitch, current_volume))

            global session_recording, session_start_time, session_events
            if session_recording:
                t = time.time() - session_start_time
                session_events.append((t, note, current_pitch, current_volume))
        return handler

    def make_release_handler(self, note):
        def handler():
            if note in sound_map:
                self.buttons[note].setStyleSheet(self.assigned_style())
            else:
                self.buttons[note].setStyleSheet(self.default_style())
        return handler

    def flash_button(self, note):
        if note in self.buttons:
            self.buttons[note].setStyleSheet(self.active_style())
            QApplication.processEvents()

    # --- Channel control methods ---
    def record_channel(self, channel_id, armed):
        if armed:
            if self.recording_channel is not None:
                self.stop_recording()
            ch = channels[channel_id]
            ch["recording"] = True
            ch["events"] = []
            ch["duration"] = 0.0
            self.recording_channel = channel_id
            self.record_start_time = time.time()
            self.status_label.setText(f"Recording on Channel {channel_id+1}")
        else:
            self.stop_recording()

    def stop_recording(self):
        if self.recording_channel is not None:
            ch = channels[self.recording_channel]
            if ch["recording"]:
                ch["duration"] = time.time() - self.record_start_time
                ch["recording"] = False
            self.recording_channel = None
            self.status_label.setText("Recording stopped")
            # No pygame.mixer.stop() – loops continue
            for w in self.channel_widgets:
                if w["record_btn"].isChecked():
                    w["record_btn"].setChecked(False)

    def start_loop(self, channel_id):
        ch = channels[channel_id]
        if not ch["events"]:
            self.status_label.setText(f"Channel {channel_id+1}: no loop to play")
            return
        self.stop_loop(channel_id)
        ch["stop_event"].clear()
        ch["playing"] = True
        ch["thread"] = threading.Thread(target=self.loop_thread, args=(channel_id,), daemon=True)
        ch["thread"].start()
        self.status_label.setText(f"Playing loop on Channel {channel_id+1}")

    def stop_loop(self, channel_id):
        ch = channels[channel_id]
        if ch["playing"]:
            ch["stop_event"].set()
            while ch["thread"] and ch["thread"].is_alive():
                QApplication.processEvents()
                time.sleep(0.01)
            ch["thread"] = None
            ch["playing"] = False
            for c in ch["active_channels"]:
                if c:
                    c.stop()
            ch["active_channels"].clear()
            self.status_label.setText(f"Stopped loop on Channel {channel_id+1}")

    def clear_loop(self, channel_id):
        self.stop_loop(channel_id)
        ch = channels[channel_id]
        ch["events"] = []
        ch["duration"] = 0.0
        self.status_label.setText(f"Cleared loop on Channel {channel_id+1}")

    def toggle_mute(self, channel_id, muted):
        ch = channels[channel_id]
        ch["mute"] = muted
        self.channel_widgets[channel_id]["mute_btn"].setText("Muted" if muted else "Mute")
        self.status_label.setText(f"Channel {channel_id+1} {'muted' if muted else 'unmuted'}")
        if muted:
            for c in ch["active_channels"]:
                if c:
                    c.stop()
            ch["active_channels"].clear()

    def loop_thread(self, channel_id):
        ch = channels[channel_id]
        while not ch["stop_event"].is_set():
            events = ch["events"]
            duration = ch["duration"]
            if not events or duration <= 0:
                break

            for c in ch["active_channels"]:
                if c:
                    c.stop()
            ch["active_channels"].clear()

            start_time = time.time()
            for t, note, pitch, volume in events:
                if ch["stop_event"].is_set():
                    return
                while (time.time() - start_time) < t:
                    if ch["stop_event"].is_set():
                        return
                    time.sleep(0.001)
                if not ch["mute"] and note in loaded_sounds:
                    c = play_sound_with_params(note, pitch, volume)
                    if c:
                        ch["active_channels"].append(c)
                    global session_recording, session_start_time, session_events
                    if session_recording:
                        global_time = time.time() - session_start_time
                        session_events.append((global_time, note, pitch, volume))

            if not ch["stop_event"].is_set():
                elapsed = time.time() - start_time
                remaining = duration - elapsed
                if remaining > 0:
                    while remaining > 0 and not ch["stop_event"].is_set():
                        sleep_time = min(0.01, remaining)
                        time.sleep(sleep_time)
                        remaining -= sleep_time

    # --- Control actions ---
    def apply_control(self, action):
        global current_volume, current_pitch
        if action == "stop":
            # Stop only one‑shot channels, not loops
            for ch in self.oneshot_channels:
                ch.stop()
            self.oneshot_channels.clear()
        elif action == "vol_up":
            current_volume = min(1.0, current_volume + 0.1)
            for s in loaded_sounds.values():
                s.set_volume(current_volume)
        elif action == "vol_down":
            current_volume = max(0.0, current_volume - 0.1)
            for s in loaded_sounds.values():
                s.set_volume(current_volume)
        elif action == "pitch_up":
            current_pitch += 0.1
        elif action == "pitch_down":
            current_pitch = max(0.5, current_pitch - 0.1)
        elif action == "stop_recording":
            self.stop_recording()
        elif action == "toggle_session_recording":
            self.toggle_session_recording()

    def toggle_session_recording(self):
        global session_recording, session_start_time, session_events
        if session_recording:
            session_recording = False
            self.session_rec_btn.setChecked(False)
            self.session_rec_status.setText("")
            self.status_label.setText("Session recording stopped")
            if session_events:
                try:
                    filename = render_session_to_wav(session_events)
                    self.status_label.setText(f"Session saved to {filename}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not render session: {e}")
            else:
                self.status_label.setText("No events recorded.")
        else:
            session_events = []
            session_start_time = time.time()
            session_recording = True
            self.session_rec_btn.setChecked(True)
            self.session_rec_status.setText("RECORDING")
            self.status_label.setText("Session recording started")

    # --- UI updates ---
    def update_status(self):
        self.volume_label.setText(f"Volume: {current_volume:.1f}")
        self.pitch_label.setText(f"Pitch: {current_pitch:.1f}")

        for i in range(NUM_CHANNELS):
            if self.recording_channel == i:
                elapsed = time.time() - self.record_start_time
                self.channel_widgets[i]["time_label"].setText(f"{elapsed:.1f} s")
            else:
                ev_count = len(channels[i]["events"])
                self.channel_widgets[i]["time_label"].setText(f"{ev_count} ev")

    # --- Other controls ---
    def toggle_overlap(self):
        self.allow_overlap = not self.allow_overlap
        self.overlap_btn.setText(f"Overlap: {'ON' if self.allow_overlap else 'OFF'}")

    def toggle_learn(self):
        self.learn_mode = not self.learn_mode
        self.status_label.setText("Press a control button on Launchpad...")

    def open_session_dialog(self):
        dialog = SessionOptionsDialog(self)
        dialog.exec()

    def closeEvent(self, event):
        if session_recording and session_events:
            reply = QMessageBox.question(self, "Save Session Recording?",
                                         "Session recording is active. Do you want to save it before quitting?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    filename = render_session_to_wav(session_events)
                    self.status_label.setText(f"Session saved to {filename}")
                except Exception as e:
                    print(f"Could not render session: {e}")
        event.accept()

# --- MIDI listener ---
def find_launchpad():
    for name in mido.get_input_names():
        if LAUNCHPAD_NAME.lower() in name.lower():
            return name
    return None

def midi_listener(gui):
    device = find_launchpad()
    if not device:
        print("Launchpad not found")
        return
    with mido.open_input(device) as port:
        for msg in port:
            if msg.type == "note_on":
                note = msg.note
                if msg.velocity > 0:
                    if not gui.allow_overlap:
                        # Stop only one‑shot channels, not loops
                        for ch in gui.oneshot_channels:
                            ch.stop()
                        gui.oneshot_channels.clear()
                    if note in loaded_sounds:
                        channel = play_sound_with_params(note, current_pitch, current_volume)
                        if channel and not gui.allow_overlap:
                            gui.oneshot_channels.append(channel)

                    if gui.recording_channel is not None:
                        ch = channels[gui.recording_channel]
                        if ch["recording"]:
                            t = time.time() - gui.record_start_time
                            ch["events"].append((t, note, current_pitch, current_volume))

                    global session_recording, session_start_time, session_events
                    if session_recording:
                        t = time.time() - session_start_time
                        session_events.append((t, note, current_pitch, current_volume))

                    gui.flash_button(note)
                    if gui.midi_out:
                        gui.midi_out.send(mido.Message('note_on', note=note, velocity=60))
                else:
                    if note in gui.buttons:
                        if note in sound_map:
                            gui.buttons[note].setStyleSheet(gui.assigned_style())
                        else:
                            gui.buttons[note].setStyleSheet(gui.default_style())
                    if gui.midi_out:
                        gui.midi_out.send(mido.Message('note_on', note=note, velocity=0))
            elif msg.type == "control_change" and msg.value == 127:
                ctrl = msg.control
                if gui.learn_mode:
                    action = gui.action_dropdown.currentText()
                    control_map[ctrl] = action
                    save_mapping()
                    gui.learn_mode = False
                    gui.status_label.setText(f"Mapped {ctrl} -> {action}")
                else:
                    if ctrl in control_map:
                        gui.apply_control(control_map[ctrl])

# --- Run ---
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Show boot logo splash screen
    splash_pixmap = get_splash_pixmap()
    if not splash_pixmap.isNull():
        splash = QSplashScreen(splash_pixmap, Qt.WindowType.WindowStaysOnTopHint)
        splash.show()
        app.processEvents()  # let it appear

    # Create main window
    gui = LaunchpadGUI()
    gui.show()

    # Close splash screen after main window is shown or after a short delay
    if 'splash' in locals():
        QTimer.singleShot(2000, splash.close)  # close after 2 seconds

    t = threading.Thread(target=midi_listener, args=(gui,), daemon=True)
    t.start()
    sys.exit(app.exec())