import reflex as rx
from app.states.organizer_state import OrganizerState, FolderItem
from app.components.file_table import file_table


def select_box(value: str, options: list[str], on_change) -> rx.Component:
    return rx.el.div(
        rx.el.select(
            rx.foreach(options, lambda opt: rx.el.option(opt, value=opt)),
            value=value,
            on_change=on_change,
            class_name="w-full appearance-none bg-[#f0f4f8] text-[#3b4b63] text-sm font-medium px-4 py-2.5 rounded-xl border border-transparent focus:border-blue-300 focus:ring-2 focus:ring-blue-100 transition-all cursor-pointer outline-none",
        ),
        rx.icon(
            "chevron-down",
            class_name="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#8ba3c7] pointer-events-none",
        ),
        class_name="relative w-full max-w-[240px]",
    )


def space_button(
    label: str, symbol: str, active: bool, on_click
) -> rx.Component:
    return rx.el.button(
        rx.el.span(label, class_name="text-xs text-gray-500 mr-2"),
        rx.el.span(
            symbol, class_name="font-mono text-sm font-bold text-gray-700"
        ),
        on_click=on_click,
        class_name=rx.cond(
            active,
            "flex items-center justify-between px-3 py-1.5 bg-white border-2 border-[#4b71ff] rounded-lg shadow-sm transition-all",
            "flex items-center justify-between px-3 py-1.5 bg-[#f0f4f8] border-2 border-transparent rounded-lg hover:bg-[#e4ebf3] transition-all",
        ),
    )


def folder_card(folder: FolderItem) -> rx.Component:
    is_active = OrganizerState.selected_folder_id == folder["id"]
    return rx.el.button(
        rx.el.div(
            rx.icon(
                folder["icon"],
                class_name=rx.cond(
                    is_active,
                    "w-5 h-5 text-[#4b71ff]",
                    "w-5 h-5 text-[#8ba3c7]",
                ),
            ),
            rx.el.span(
                folder["name"],
                class_name=rx.cond(
                    is_active,
                    "text-xs font-bold text-[#4b71ff]",
                    "text-xs font-semibold text-[#6b7b93]",
                ),
            ),
            class_name="flex items-center gap-3",
        ),
        on_click=lambda: OrganizerState.select_folder(folder["id"]),
        class_name=rx.cond(
            is_active,
            "flex items-center justify-between p-4 bg-white border-2 border-[#4b71ff] rounded-2xl shadow-[0_4px_12px_rgba(75,113,255,0.1)] transition-all transform scale-[1.02]",
            "flex items-center justify-between p-4 bg-[#f4f7fb] border border-[#e2e8f0] rounded-2xl hover:bg-white hover:border-[#d0d7e5] transition-all",
        ),
    )


def organizer_view() -> rx.Component:
    return rx.el.div(
        # Top Prompt Section
        rx.el.div(
            rx.el.p(
                "Save your settings changes?",
                class_name="text-[15px] font-semibold text-[#3b4b63]",
            ),
            rx.el.div(
                rx.el.button(
                    "Cancel",
                    class_name="px-5 py-2.5 text-sm font-semibold text-[#6b7b93] hover:bg-gray-100 hover:text-gray-900 rounded-full transition-colors",
                ),
                rx.el.button(
                    "Apply settings",
                    on_click=OrganizerState.generate_proposals,
                    class_name="px-5 py-2.5 text-sm font-semibold text-white bg-[#4b71ff] hover:bg-[#3a5be0] rounded-full shadow-[0_2px_8px_rgba(75,113,255,0.3)] transition-colors disabled:opacity-50 disabled:cursor-not-allowed",
                    disabled=(OrganizerState.selected_count == 0)
                    | OrganizerState.is_scanning,
                ),
                class_name="flex gap-2",
            ),
            class_name="flex items-center justify-between mb-6 pb-6 border-b border-[#e2e8f0]",
        ),
        # Settings Card
        rx.el.div(
            # Header
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "sliders-horizontal",
                        class_name="w-5 h-5 text-[#8ba3c7]",
                    ),
                    class_name="w-8 h-8 rounded-full bg-[#f0f4f8] flex items-center justify-center mr-3",
                ),
                rx.el.h2(
                    "Adjust settings",
                    class_name="text-lg font-bold text-[#1e293b] tracking-tight",
                ),
                class_name="flex items-center mb-6",
            ),
            # Form Rows
            rx.el.div(
                # Language
                rx.el.div(
                    rx.el.label(
                        "File name language",
                        class_name="text-sm font-semibold text-[#475569] w-1/3",
                    ),
                    rx.el.div(
                        select_box(
                            OrganizerState.language,
                            ["English", "Spanish", "French", "German"],
                            OrganizerState.set_language,
                        ),
                        class_name="w-2/3 flex items-center",
                    ),
                    class_name="flex items-center py-4 border-b border-[#f4f7fb]",
                ),
                # Date format
                rx.el.div(
                    rx.el.label(
                        "Date format",
                        class_name="text-sm font-semibold text-[#475569] w-1/3",
                    ),
                    rx.el.div(
                        select_box(
                            OrganizerState.date_format,
                            ["YYYY-MM-DD", "MM-DD-YYYY", "DD-MM-YYYY"],
                            OrganizerState.set_date_format,
                        ),
                        class_name="w-2/3 flex items-center",
                    ),
                    class_name="flex items-center py-4 border-b border-[#f4f7fb]",
                ),
                # Text format
                rx.el.div(
                    rx.el.label(
                        "Text format",
                        class_name="text-sm font-semibold text-[#475569] w-1/3",
                    ),
                    rx.el.div(
                        select_box(
                            OrganizerState.text_format,
                            [
                                "Title Case",
                                "lowercase",
                                "UPPERCASE",
                                "camelCase",
                                "snake_case",
                            ],
                            OrganizerState.set_text_format,
                        ),
                        class_name="w-2/3 flex items-center",
                    ),
                    class_name="flex items-center py-4 border-b border-[#f4f7fb]",
                ),
                # Spacing
                rx.el.div(
                    rx.el.label(
                        "File name spaces",
                        class_name="text-sm font-semibold text-[#475569] w-1/3",
                    ),
                    rx.el.div(
                        rx.el.div(
                            space_button(
                                "Underscore",
                                "_",
                                OrganizerState.space_char == "_",
                                lambda: OrganizerState.set_space_char("_"),
                            ),
                            space_button(
                                "Dash",
                                "-",
                                OrganizerState.space_char == "-",
                                lambda: OrganizerState.set_space_char("-"),
                            ),
                            space_button(
                                "Space",
                                "[ ]",
                                OrganizerState.space_char == " ",
                                lambda: OrganizerState.set_space_char(" "),
                            ),
                            class_name="flex gap-3",
                        ),
                        class_name="w-2/3 flex items-center",
                    ),
                    class_name="flex items-center py-4 border-b border-[#f4f7fb]",
                ),
                # Confirm checkbox
                rx.el.div(
                    rx.el.div(class_name="w-1/3"),
                    rx.el.div(
                        rx.el.label(
                            rx.el.div(
                                rx.el.input(
                                    type="checkbox",
                                    checked=OrganizerState.require_confirmation,
                                    on_change=OrganizerState.set_require_confirmation,
                                    class_name="peer sr-only",
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "check",
                                        class_name="w-3 h-3 text-white opacity-0 peer-checked:opacity-100 transition-opacity",
                                    ),
                                    class_name="w-5 h-5 rounded-md border-2 border-[#d0d7e5] peer-checked:border-[#4b71ff] peer-checked:bg-[#4b71ff] flex items-center justify-center mr-3 transition-colors",
                                ),
                                "Require confirmation before renaming",
                                class_name="flex items-center cursor-pointer text-sm font-medium text-[#475569]",
                            )
                        ),
                        class_name="w-2/3 flex items-center",
                    ),
                    class_name="flex items-center py-4",
                ),
                # Move files checkbox
                rx.el.div(
                    rx.el.div(class_name="w-1/3"),
                    rx.el.div(
                        rx.el.label(
                            rx.el.div(
                                rx.el.input(
                                    type="checkbox",
                                    checked=OrganizerState.move_files,
                                    on_change=OrganizerState.set_move_files,
                                    class_name="peer sr-only",
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "check",
                                        class_name="w-3 h-3 text-white opacity-0 peer-checked:opacity-100 transition-opacity",
                                    ),
                                    class_name="w-5 h-5 rounded-md border-2 border-[#d0d7e5] peer-checked:border-[#4b71ff] peer-checked:bg-[#4b71ff] flex items-center justify-center mr-3 transition-colors",
                                ),
                                rx.el.span("Move files to organized folders"),
                                rx.icon(
                                    "circle_help",
                                    class_name="w-4 h-4 text-[#8ba3c7] ml-2 cursor-help",
                                ),
                                class_name="flex items-center cursor-pointer text-sm font-medium text-[#475569]",
                            )
                        ),
                        class_name="w-2/3 flex items-center",
                    ),
                    class_name="flex items-center py-2",
                ),
                class_name="flex flex-col",
            ),
            class_name="p-8 border border-[#e2e8f0] rounded-[24px] bg-white shadow-[0_4px_20px_rgba(0,0,0,0.02)] mb-8",
        ),
        # Top Controls
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "SCAN LOCATION",
                    class_name="text-[11px] font-bold text-gray-400 mb-4 tracking-widest font-mono",
                ),
                rx.el.div(
                    rx.foreach(OrganizerState.folders, folder_card),
                    class_name="grid grid-cols-2 sm:grid-cols-4 gap-4 flex-1",
                ),
            ),
            class_name="flex flex-col mb-8 bg-gray-50/50 p-8 rounded-3xl border-2 border-dashed border-gray-300 hover:border-blue-400 transition-colors",
        ),
        rx.cond(
            OrganizerState.selected_folder_id != "",
            rx.el.div(
                rx.el.label(
                    "Target Scope (Optional):",
                    class_name="text-sm font-medium text-gray-700 mr-3",
                ),
                rx.el.select(
                    rx.el.option("All contents", value="All"),
                    rx.foreach(
                        OrganizerState.current_sub_folders,
                        lambda sf: rx.el.option(sf, value=sf),
                    ),
                    value=OrganizerState.selected_sub_folder,
                    on_change=OrganizerState.set_sub_folder,
                    class_name="px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-blue-500 focus:border-blue-500 bg-white min-w-[200px] appearance-none",
                ),
                rx.el.p(
                    "Narrow down your scan to a specific sub-folder to save time.",
                    class_name="text-xs text-gray-500 ml-4",
                ),
                class_name="flex items-center mb-6 bg-white p-3 rounded-lg border border-gray-200 shadow-sm",
            ),
        ),
        # Action Bar & AI Settings
        rx.el.div(
            rx.el.div(
                rx.el.fieldset(
                    rx.el.legend("AI Processing Mode", class_name="sr-only"),
                    rx.el.div(
                        rx.el.button(
                            "Local AI",
                            on_click=lambda: OrganizerState.set_processing_mode(
                                "local"
                            ),
                            aria_pressed=OrganizerState.processing_mode
                            == "local",
                            class_name=rx.cond(
                                OrganizerState.processing_mode == "local",
                                "px-4 py-1.5 text-xs font-bold rounded bg-blue-600 text-white ring-2 ring-blue-600 ring-offset-1",
                                "px-4 py-1.5 text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-100 border border-gray-200",
                            ),
                        ),
                        rx.el.button(
                            "Cloud AI",
                            on_click=lambda: OrganizerState.set_processing_mode(
                                "cloud"
                            ),
                            aria_pressed=OrganizerState.processing_mode
                            == "cloud",
                            class_name=rx.cond(
                                OrganizerState.processing_mode == "cloud",
                                "px-4 py-1.5 text-xs font-bold rounded bg-blue-600 text-white ring-2 ring-blue-600 ring-offset-1",
                                "px-4 py-1.5 text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-100 border border-gray-200",
                            ),
                        ),
                        class_name="flex items-center gap-1 bg-gray-100 p-1 rounded-lg mr-4",
                    ),
                ),
                rx.cond(
                    OrganizerState.processing_mode == "cloud",
                    rx.el.div(
                        rx.el.input(
                            placeholder="Enter Cloud API Key",
                            type="password",
                            on_change=OrganizerState.set_cloud_api_key.debounce(
                                300
                            ),
                            class_name="w-48 px-3 py-1 text-xs border border-gray-300 rounded focus:ring-2 focus:ring-blue-500",
                        ),
                        rx.cond(
                            OrganizerState.is_cloud_connected,
                            rx.icon(
                                "message_circle_check",
                                class_name="w-4 h-4 text-green-500 ml-2",
                            ),
                            rx.icon(
                                "circle_alert",
                                class_name="w-4 h-4 text-red-500 ml-2",
                            ),
                        ),
                        class_name="flex items-center mr-4",
                    ),
                ),
                rx.el.div(
                    rx.el.button(
                        rx.cond(
                            OrganizerState.is_scanning,
                            rx.icon(
                                "loader", class_name="w-4 h-4 mr-2 animate-spin"
                            ),
                            rx.icon("search", class_name="w-4 h-4 mr-2"),
                        ),
                        "Scan Folder",
                        on_click=OrganizerState.scan_current_folder,
                        disabled=(OrganizerState.selected_folder_id == "")
                        | OrganizerState.is_scanning,
                        class_name="flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md shadow-sm hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors peer",
                    ),
                    rx.cond(
                        OrganizerState.selected_folder_id == "",
                        rx.el.span(
                            "Select a folder first",
                            class_name="absolute -top-8 left-1/2 -translate-x-1/2 whitespace-nowrap bg-gray-800 text-white text-xs px-2 py-1 rounded opacity-0 peer-hover:opacity-100 transition-opacity pointer-events-none",
                        ),
                    ),
                    class_name="relative",
                ),
                rx.cond(
                    OrganizerState.is_scanning,
                    rx.el.div(
                        rx.el.div(
                            class_name="h-2 bg-blue-600 rounded-full transition-all duration-300",
                            style={"width": f"{OrganizerState.scan_progress}%"},
                        ),
                        class_name="w-32 h-2 bg-gray-200 rounded-full overflow-hidden ml-4",
                    ),
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.el.label(
                    rx.icon("search", class_name="w-4 h-4 text-gray-400 mr-2"),
                    rx.el.span("Search files", class_name="sr-only"),
                    rx.el.input(
                        placeholder="Search files...",
                        aria_label="Search through files in current folder",
                        on_change=OrganizerState.set_search_query.debounce(500),
                        class_name="w-64 px-3 py-1.5 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900",
                    ),
                    class_name="flex items-center",
                ),
            ),
            class_name="flex items-center justify-between p-4 bg-white border border-gray-200 rounded-lg shadow-sm mb-6",
        ),
        # Main Workspace
        rx.el.div(
            rx.el.div(file_table(), class_name="flex-1"),
            # Metadata / Action Panel
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "AI Processing",
                        class_name="text-sm font-bold text-gray-900 mb-2 uppercase tracking-wider",
                    ),
                    rx.el.p(
                        rx.cond(
                            OrganizerState.processing_mode == "local",
                            "Local Mode: Fast & private. Runs completely on your device without sending data.",
                            "Cloud Mode: Slower but uses advanced models for better accuracy. Requires API Key.",
                        ),
                        class_name="text-xs text-gray-600 mb-4",
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.icon("plug_2", class_name="w-4 h-4 mr-2"),
                            "Generate Proposals",
                            on_click=OrganizerState.generate_proposals,
                            disabled=(OrganizerState.selected_count == 0)
                            | OrganizerState.is_scanning,
                            class_name="w-full flex justify-center items-center px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-md shadow-sm hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors peer",
                        ),
                        rx.cond(
                            OrganizerState.selected_count == 0,
                            rx.el.span(
                                "Select files to generate proposals",
                                class_name="text-xs text-red-500 mt-1 block",
                            ),
                        ),
                        class_name="mb-6",
                    ),
                ),
                rx.el.h3(
                    "Storage Impact",
                    class_name="text-sm font-bold text-gray-900 mb-4 uppercase tracking-wider",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            "Total Files", class_name="text-xs text-gray-500"
                        ),
                        rx.el.span(
                            OrganizerState.files.length().to_string(),
                            class_name="text-sm font-medium text-gray-900",
                        ),
                        class_name="flex justify-between py-2 border-b border-gray-100",
                    ),
                    rx.el.div(
                        rx.el.span(
                            "Total Size", class_name="text-xs text-gray-500"
                        ),
                        rx.el.span(
                            f"{OrganizerState.total_size_mb:.1f} MB",
                            class_name="text-sm font-medium text-gray-900",
                        ),
                        class_name="flex justify-between py-2 border-b border-gray-100",
                    ),
                    rx.el.div(
                        rx.el.span(
                            "Selected", class_name="text-xs text-gray-500"
                        ),
                        rx.el.span(
                            OrganizerState.selected_count.to_string(),
                            class_name="text-sm font-medium text-blue-600",
                        ),
                        class_name="flex justify-between py-2",
                    ),
                    class_name="bg-gray-50 rounded-md p-3 mb-6 border border-gray-200",
                ),
                rx.el.h3(
                    "Pending Actions",
                    class_name="text-sm font-bold text-gray-900 mb-4 uppercase tracking-wider",
                ),
                rx.cond(
                    OrganizerState.selected_count > 0,
                    rx.el.div(
                        rx.el.p(
                            f"Ready to apply changes to {OrganizerState.selected_count} files.",
                            class_name="text-xs text-gray-600 mb-4",
                        ),
                        rx.el.button(
                            "Approve Changes",
                            on_click=OrganizerState.apply_simulated_changes,
                            class_name="w-full flex justify-center items-center px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-md shadow-sm hover:bg-green-700 transition-colors",
                        ),
                    ),
                    rx.el.div(
                        rx.icon(
                            "info", class_name="w-5 h-5 text-gray-400 mb-2"
                        ),
                        rx.el.p(
                            "Select files from the table to review and approve organization changes.",
                            class_name="text-xs text-gray-500 text-center",
                        ),
                        class_name="flex flex-col items-center justify-center p-4 border border-dashed border-gray-300 rounded-md bg-white",
                    ),
                ),
                rx.cond(
                    OrganizerState.action_history.length() > 0,
                    rx.el.div(
                        rx.el.h3(
                            "Recent Actions",
                            class_name="text-sm font-bold text-gray-900 mt-6 mb-4 uppercase tracking-wider",
                        ),
                        rx.el.div(
                            rx.foreach(
                                OrganizerState.action_history,
                                lambda hist: rx.el.div(
                                    rx.el.div(
                                        rx.el.span(
                                            hist["description"],
                                            class_name="text-xs font-medium text-gray-700",
                                        ),
                                        rx.el.button(
                                            rx.icon(
                                                "undo-2", class_name="w-3 h-3"
                                            ),
                                            on_click=lambda: (
                                                OrganizerState.undo_action(
                                                    hist["id"]
                                                )
                                            ),
                                            class_name="p-1 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors",
                                        ),
                                        class_name="flex items-center justify-between",
                                    ),
                                    class_name="p-3 bg-gray-50 border border-gray-100 rounded-md mb-2",
                                ),
                            ),
                            class_name="max-h-40 overflow-y-auto",
                        ),
                    ),
                ),
                class_name="w-72 bg-white border border-gray-200 rounded-lg shadow-sm p-4 flex-shrink-0 h-fit sticky top-6",
            ),
            class_name="flex flex-col lg:flex-row gap-6",
        ),
        class_name="flex-1 p-8 overflow-y-auto",
    )