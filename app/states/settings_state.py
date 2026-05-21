import reflex as rx
from pydantic import BaseModel
import logging
import json


class AppSettings(BaseModel):
    excluded_paths: list[str] = ["C:\\Windows\\System32"]
    processing_mode: str = "local"
    cloud_api_key: str = ""
    scan_behavior: str = "fast"


class SettingsState(rx.State):
    settings_json: str = rx.LocalStorage(name="deskmanager_settings", sync=True)

    @rx.var
    def settings(self) -> AppSettings:
        if self.settings_json:
            try:
                return AppSettings.model_validate_json(self.settings_json)
            except Exception:
                logging.exception("Failed to parse user settings JSON")
                return AppSettings()
        return AppSettings()

    @rx.event
    def update_processing_mode(self, mode: str):
        s = self.settings
        s.processing_mode = mode
        self.settings_json = s.model_dump_json()

    @rx.event
    def update_cloud_api_key(self, key: str):
        s = self.settings
        s.cloud_api_key = key
        self.settings_json = s.model_dump_json()

    @rx.event
    def update_scan_behavior(self, behavior: str):
        s = self.settings
        s.scan_behavior = behavior
        self.settings_json = s.model_dump_json()

    @rx.event
    def add_excluded_path(self, form_data: dict):
        path = form_data.get("new_path", "").strip()
        if path:
            s = self.settings
            if path not in s.excluded_paths:
                s.excluded_paths.append(path)
                self.settings_json = s.model_dump_json()

    @rx.event
    def remove_excluded_path(self, path: str):
        s = self.settings
        if path in s.excluded_paths:
            s.excluded_paths.remove(path)
            self.settings_json = s.model_dump_json()