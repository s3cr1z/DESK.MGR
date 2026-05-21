import reflex as rx
from typing import TypedDict
import asyncio
import random
import uuid


class CleanItem(TypedDict):
    id: str
    name: str
    category: str
    size_mb: float
    path: str
    risk_level: str
    protected: bool
    status: str


class CleanHistoryItem(TypedDict):
    id: str
    description: str
    recovered_mb: float
    items: list[dict[str, str]]
    reversible: bool


def generate_mock_clean_items() -> list[CleanItem]:
    categories = ["duplicates", "applications", "caches"]
    items: list[CleanItem] = []

    for i in range(15):
        cat = random.choice(categories)
        if cat == "duplicates":
            name = f"Document_Copy({random.randint(1, 10)}).pdf"
            path = f"C:\\Users\\User\\Documents\\{name}"
            risk = "low"
            protected = False
            size = round(random.uniform(1.0, 50.0), 2)
        elif cat == "applications":
            name = f"OldApp_{random.randint(2018, 2022)}.exe"
            path = (
                f"C:\\Program Files\\OldApp_{random.randint(100, 999)}\\{name}"
            )
            risk = "medium"
            protected = random.random() > 0.8
            size = round(random.uniform(50.0, 500.0), 2)
        else:
            name = f"cache_{random.randint(1000, 9999)}.tmp"
            path = f"C:\\Users\\User\\AppData\\Local\\Temp\\{name}"
            risk = "low"
            protected = False
            size = round(random.uniform(0.1, 10.0), 2)

        items.append(
            {
                "id": f"item_{i}_{uuid.uuid4().hex[:8]}",
                "name": name,
                "category": cat,
                "size_mb": size,
                "path": path,
                "risk_level": risk,
                "protected": protected,
                "status": "pending",
            }
        )

    # Add a high risk protected item for demonstration
    items.append(
        {
            "id": "sys_protected",
            "name": "ntoskrnl.exe",
            "category": "applications",
            "size_mb": 15.4,
            "path": "C:\\Windows\\System32\\ntoskrnl.exe",
            "risk_level": "high",
            "protected": True,
            "status": "pending",
        }
    )

    return items


class CleanerState(rx.State):
    is_scanning: bool = False
    scan_progress: int = 0
    items: list[CleanItem] = []
    selected_item_ids: list[str] = []
    category_filter: str = "all"
    history: list[CleanHistoryItem] = []

    @rx.var
    def filtered_items(self) -> list[CleanItem]:
        if self.category_filter == "all":
            return [i for i in self.items if i["status"] == "pending"]
        return [
            i
            for i in self.items
            if i["category"] == self.category_filter
            and i["status"] == "pending"
        ]

    @rx.var
    def total_selected_size_mb(self) -> float:
        selected_items = [
            i for i in self.items if i["id"] in self.selected_item_ids
        ]
        return sum([i["size_mb"] for i in selected_items])

    @rx.var
    def has_high_risk_selected(self) -> bool:
        selected_items = [
            i for i in self.items if i["id"] in self.selected_item_ids
        ]
        return any(i["risk_level"] == "high" for i in selected_items)

    @rx.event(background=True)
    async def scan_system(self):
        async with self:
            if self.is_scanning:
                return
            self.is_scanning = True
            self.scan_progress = 0
            self.items = []
            self.selected_item_ids = []

        for i in range(1, 11):
            await asyncio.sleep(0.15)
            async with self:
                self.scan_progress = i * 10

        async with self:
            self.items = generate_mock_clean_items()
            self.is_scanning = False
            self.scan_progress = 100

    @rx.event
    def set_category_filter(self, category: str):
        self.category_filter = category
        self.selected_item_ids = []

    @rx.event
    def toggle_item(self, item_id: str):
        if item_id in self.selected_item_ids:
            self.selected_item_ids.remove(item_id)
        else:
            item = next((i for i in self.items if i["id"] == item_id), None)
            if item and not item["protected"]:
                self.selected_item_ids.append(item_id)
            elif item and item["protected"]:
                return rx.toast(
                    "Cannot select protected system files.",
                    style={"background-color": "#ef4444", "color": "white"},
                )

    @rx.event
    def toggle_all(self):
        filtered = self.filtered_items
        selectable = [i["id"] for i in filtered if not i["protected"]]
        if len(self.selected_item_ids) == len(selectable):
            self.selected_item_ids = []
        else:
            self.selected_item_ids = selectable

    @rx.event
    def apply_cleanup(self):
        if not self.selected_item_ids:
            return

        cleaned_items = []
        recovered_size = 0.0

        for item in self.items:
            if item["id"] in self.selected_item_ids:
                cleaned_items.append(
                    {
                        "id": item["id"],
                        "name": item["name"],
                        "path": item["path"],
                    }
                )
                recovered_size += item["size_mb"]
                item["status"] = "cleaned"

        if cleaned_items:
            self.history.insert(
                0,
                {
                    "id": str(uuid.uuid4()),
                    "description": f"Cleaned {len(cleaned_items)} items",
                    "recovered_mb": recovered_size,
                    "items": cleaned_items,
                    "reversible": True,
                },
            )

        self.selected_item_ids = []
        return rx.toast(
            f"Cleanup complete! Recovered {recovered_size:.1f} MB.",
            style={"background-color": "#10b981", "color": "white"},
        )

    @rx.event
    def undo_cleanup(self, history_id: str):
        record = next((h for h in self.history if h["id"] == history_id), None)
        if not record or not record["reversible"]:
            return rx.toast(
                "Cannot undo this action.",
                style={"background-color": "#ef4444", "color": "white"},
            )

        for change in record["items"]:
            for item in self.items:
                if item["id"] == change["id"]:
                    item["status"] = "pending"
                    break

        self.history = [h for h in self.history if h["id"] != history_id]
        return rx.toast(
            "Cleanup undone. Items restored.",
            style={"background-color": "#3b82f6", "color": "white"},
        )