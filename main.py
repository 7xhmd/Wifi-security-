import os
from datetime import datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout

KV = r"""
<Root>:
    orientation: "vertical"
    padding: "18dp"
    spacing: "12dp"
    canvas.before:
        Color:
            rgba: (0.025, 0.04, 0.055, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        text: "[b]WIFI SECURITY[/b]"
        markup: True
        font_size: "25sp"
        color: (0.15, 1, 0.65, 1)
        size_hint_y: None
        height: "54dp"
    Label:
        text: "LOCAL DEVICE AUDIT  •  SAFE MODE"
        font_size: "11sp"
        color: (0.45, 0.85, 0.72, 1)
        size_hint_y: None
        height: "24dp"
    BoxLayout:
        orientation: "vertical"
        padding: "14dp"
        spacing: "8dp"
        canvas.before:
            Color:
                rgba: (0.055, 0.09, 0.105, 1)
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [12]
        Label:
            text: "AUDIT STATUS"
            color: (0.55, 0.85, 0.75, 1)
            size_hint_y: None
            height: "25dp"
        Label:
            text: root.status
            color: (0.2, 1, 0.65, 1)
            font_size: "18sp"
            halign: "left"
            text_size: self.width, None
        Label:
            text: root.result
            color: (0.85, 0.9, 0.9, 1)
            halign: "left"
            valign: "top"
            text_size: self.width, self.height
    Button:
        text: "START LOCAL AUDIT"
        size_hint_y: None
        height: "52dp"
        background_normal: ""
        background_color: (0.05, 0.55, 0.35, 1)
        on_release: root.start_audit()
    Button:
        text: "STOP"
        size_hint_y: None
        height: "46dp"
        background_normal: ""
        background_color: (0.45, 0.12, 0.16, 1)
        on_release: root.stop_audit()
    Label:
        text: "Privacy: counts filenames locally only. Nothing is uploaded."
        color: (0.55, 0.65, 0.67, 1)
        font_size: "11sp"
        halign: "center"
        text_size: self.width, None
    Widget:
"""

class Root(BoxLayout):
    status = StringProperty("READY")
    result = StringProperty("Press START to count supported files in Downloads.\\nNo files are opened, copied, or transmitted.")
    running = BooleanProperty(False)

    def start_audit(self):
        if self.running:
            return
        self.running = True
        self.status = "SCANNING…"
        self.result = "Counting file types locally.\\n"
        self._event = Clock.schedule_once(self._run_audit, 0.2)

    def stop_audit(self):
        self.running = False
        if hasattr(self, "_event"):
            self._event.cancel()
        self.status = "STOPPED"
        self.result += "\\nAudit stopped by user."

    def _run_audit(self, _dt):
        if not self.running:
            return
        roots = ["/storage/emulated/0/Download"] if os.path.isdir("/storage/emulated/0/Download") else [os.path.expanduser("~")]
        counts = {"Images": 0, "Videos": 0, "Documents": 0, "Other": 0}
        exts = {
            "Images": (".jpg", ".jpeg", ".png", ".webp", ".gif"),
            "Videos": (".mp4", ".mov", ".mkv", ".3gp", ".avi"),
            "Documents": (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".txt", ".csv")
        }
        visited = 0
        for root_dir in roots:
            for current, dirs, names in os.walk(root_dir):
                if not self.running:
                    return
                for name in names:
                    visited += 1
                    low = name.lower()
                    matched = False
                    for category, endings in exts.items():
                        if low.endswith(endings):
                            counts[category] += 1
                            matched = True
                            break
                    if not matched:
                        counts["Other"] += 1
                    if visited >= 5000:
                        break
                if visited >= 5000:
                    break
        if not self.running:
            return
        self.status = "COMPLETE"
        self.result = (
            f"Files checked: {visited}\\nImages: {counts['Images']}\\n"
            f"Videos: {counts['Videos']}\\nDocuments: {counts['Documents']}\\n"
            f"Other: {counts['Other']}\\n\\nCompleted: {datetime.now().strftime('%H:%M:%S')}\\n"
            "Local counts only — no content accessed or sent."
        )
        self.running = False

class WifiSecurityApp(App):
    def build(self):
        Builder.load_string(KV)
        return Root()

if __name__ == "__main__":
    WifiSecurityApp().run()
