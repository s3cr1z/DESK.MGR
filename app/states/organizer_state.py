import reflex as rx
from typing import TypedDict
import asyncio
import random


class FileItem(TypedDict):
    id: str
    name: str
    ext: str
    size_mb: float
    modified: str
    path: str
    proposed_name: str
    proposed_folder: str
    status: str


class FolderItem(TypedDict):
    id: str
    name: str
    icon: str
    path: str


class HistoryItem(TypedDict):
    id: str
    description: str
    changes: list[dict[str, str]]


def generate_mock_files(folder_id: str) -> list[FileItem]:
    extensions = {
        "documents": [".pdf", ".docx", ".xlsx", ".txt"],
        "downloads": [".zip", ".dmg", ".exe", ".iso"],
        "pictures": [".jpg", ".png", ".raw"],
        "desktop": [".lnk", ".txt", ".ini"],
    }

    ext_list = extensions.get(folder_id, [".dat", ".tmp", ".log"])
    files: list[FileItem] = []

    for i in range(1, random.randint(10, 25)):
        ext = random.choice(ext_list)
        name = f"File_{random.randint(1000, 9999)}"
        proposed = f"Organized_{name}" if random.random() > 0.5 else ""

        files.append(
            {
                "id": f"{folder_id}_f{i}",
                "name": f"{name}{ext}",
                "ext": ext,
                "size_mb": round(random.uniform(0.1, 500.0), 2),
                "modified": f"2023-10-{random.randint(10, 28)}",
                "path": f"C:\\Users\\User\\{folder_id.title()}\\{name}{ext}",
                "proposed_name": proposed + ext if proposed else "",
                "proposed_folder": "",
                "status": "pending review" if proposed else "clean",
            }
        )
    return files


class OrganizerState(rx.State):
    folders: list[FolderItem] = [
        {
            "id": "desktop",
            "name": "Desktop",
            "icon": "monitor",
            "path": "C:\\Users\\User\\Desktop",
        },
        {
            "id": "documents",
            "name": "Documents",
            "icon": "file-text",
            "path": "C:\\Users\\User\\Documents",
        },
        {
            "id": "downloads",
            "name": "Downloads",
            "icon": "download",
            "path": "C:\\Users\\User\\Downloads",
        },
        {
            "id": "pictures",
            "name": "Pictures",
            "icon": "image",
            "path": "C:\\Users\\User\\Pictures",
        },
    ]

    selected_folder_id: str = ""
    sub_folders: dict[str, list[str]] = {
        "desktop": ["Shortcuts", "Temp", "Work"],
        "documents": ["Projects", "Invoices", "Personal"],
        "downloads": ["Installers", "Images", "PDFs"],
        "pictures": ["Screenshots", "Camera Roll", "Saved Pictures"],
    }
    selected_sub_folder: str = "All"
    is_scanning: bool = False
    scan_progress: int = 0

    files: list[FileItem] = []
    selected_file_ids: list[str] = []
    search_query: str = ""

    processing_mode: str = "local"
    cloud_api_key: str = ""

    # New Settings
    language: str = "English"
    date_format: str = "YYYY-MM-DD"
    text_format: str = "Title Case"
    space_char: str = "_"
    require_confirmation: bool = True
    move_files: bool = False

    action_history: list[HistoryItem] = []

    @rx.event
    def set_language(self, val: str):
        self.language = val

    @rx.event
    def set_date_format(self, val: str):
        self.date_format = val

    @rx.event
    def set_text_format(self, val: str):
        self.text_format = val

    @rx.event
    def set_space_char(self, val: str):
        self.space_char = val

    @rx.event
    def set_require_confirmation(self, val: bool):
        self.require_confirmation = val

    @rx.event
    def set_move_files(self, val: bool):
        self.move_files = val

    @rx.var
    def is_cloud_connected(self) -> bool:
        return len(self.cloud_api_key) > 8

    @rx.var
    def current_folder_name(self) -> str:
        for f in self.folders:
            if f["id"] == self.selected_folder_id:
                return f["name"]
        return "Select a folder"

    @rx.var
    def current_sub_folders(self) -> list[str]:
        if not self.selected_folder_id:
            return []
        return self.sub_folders.get(self.selected_folder_id, [])

    @rx.var
    def filtered_files(self) -> list[FileItem]:
        if not self.search_query:
            return self.files
        sq = self.search_query.lower()
        return [
            f
            for f in self.files
            if sq in f["name"].lower() or sq in f["ext"].lower()
        ]

    @rx.var
    def total_size_mb(self) -> float:
        return sum(f["size_mb"] for f in self.files)

    @rx.var
    def selected_count(self) -> int:
        return len(self.selected_file_ids)

    @rx.event
    def select_folder(self, folder_id: str):
        self.selected_folder_id = folder_id
        self.selected_sub_folder = "All"
        self.files = []
        self.selected_file_ids = []
        self.scan_progress = 0

    @rx.event
    def set_sub_folder(self, sf: str):
        self.selected_sub_folder = sf

    @rx.event(background=True)
    async def scan_current_folder(self):
        async with self:
            if not self.selected_folder_id or self.is_scanning:
                return
            self.is_scanning = True
            self.scan_progress = 0
            self.files = []

        for i in range(1, 11):
            await asyncio.sleep(0.1)
            async with self:
                self.scan_progress = i * 10

        async with self:
            self.files = generate_mock_files(self.selected_folder_id)
            self.is_scanning = False
            self.scan_progress = 100

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def toggle_file(self, file_id: str):
        if file_id in self.selected_file_ids:
            self.selected_file_ids.remove(file_id)
        else:
            self.selected_file_ids.append(file_id)

    @rx.event
    def toggle_all(self):
        if len(self.selected_file_ids) == len(self.filtered_files):
            self.selected_file_ids = []
        else:
            self.selected_file_ids = [f["id"] for f in self.filtered_files]

    @rx.event
    def set_processing_mode(self, mode: str):
        self.processing_mode = mode

    @rx.event
    def set_cloud_api_key(self, key: str):
        self.cloud_api_key = key

    @rx.event
    def generate_proposals(self):
        if self.processing_mode == "cloud" and not self.is_cloud_connected:
            return rx.toast(
                "Valid API Key required for cloud processing.",
                style={"background-color": "#ef4444", "color": "white"},
            )

        for f in self.files:
            if f["id"] in self.selected_file_ids:
                if not f["proposed_name"]:
                    cleaned_name = (
                        f["name"]
                        .replace(" ", self.space_char)
                        .replace("_", self.space_char)
                    )
                    f["proposed_name"] = f"{cleaned_name}"

                ext = f["ext"].lower()
                if ext in [".pdf", ".docx", ".txt"]:
                    f["proposed_folder"] = "Documents"
                elif ext in [".jpg", ".png"]:
                    f["proposed_folder"] = "Images"
                else:
                    f["proposed_folder"] = "Archives"

                f["status"] = "pending review"

    @rx.event
    def apply_simulated_changes(self):
        changes = []
        for f in self.files:
            if f["id"] in self.selected_file_ids and (
                f["proposed_name"] or f["proposed_folder"]
            ):
                changes.append(
                    {
                        "id": f["id"],
                        "old_name": f["name"],
                        "new_name": f["proposed_name"] or f["name"],
                        "old_path": f["path"],
                        "new_folder": f["proposed_folder"] or "",
                    }
                )
                if f["proposed_name"]:
                    f["name"] = f["proposed_name"]
                if f["proposed_folder"]:
                    parts = f["path"].split("\\")
                    parts[-2] = f["proposed_folder"]
                    f["path"] = "\\".join(parts)

                f["proposed_name"] = ""
                f["proposed_folder"] = ""
                f["status"] = "applied"

        if changes:
            import uuid

            self.action_history.insert(
                0,
                {
                    "id": str(uuid.uuid4()),
                    "description": f"Applied AI organization to {len(changes)} files",
                    "changes": changes,
                },
            )

        self.selected_file_ids = []
        return rx.toast(
            "Changes applied successfully!",
            style={"background-color": "#10b981", "color": "white"},
        )

    @rx.event
    def undo_action(self, action_id: str):
        record = next(
            (h for h in self.action_history if h["id"] == action_id), None
        )
        if not record:
            return rx.toast("History record not found.")

        for change in record["changes"]:
            for f in self.files:
                if f["id"] == change["id"]:
                    f["name"] = change["old_name"]
                    f["path"] = change["old_path"]
                    f["status"] = "clean"
                    break

        self.action_history = [
            h for h in self.action_history if h["id"] != action_id
        ]
        return rx.toast(
            "Action reverted.",
            style={"background-color": "#3b82f6", "color": "white"},
        )