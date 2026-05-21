import reflex as rx
from app.states.organizer_state import OrganizerState, FileItem


def file_row(file: FileItem) -> rx.Component:
    is_selected = OrganizerState.selected_file_ids.contains(file["id"])
    has_proposal = (file["proposed_name"] != "") | (
        file["proposed_folder"] != ""
    )

    return rx.el.tr(
        rx.el.td(
            rx.el.input(
                type="checkbox",
                checked=is_selected,
                on_change=lambda: OrganizerState.toggle_file(file["id"]),
                class_name="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 cursor-pointer",
            ),
            class_name="px-4 py-3 whitespace-nowrap w-10",
        ),
        rx.el.td(
            rx.el.div(
                rx.icon("file", class_name="w-4 h-4 text-gray-400 mr-2"),
                rx.el.span(
                    file["name"], class_name="text-sm font-medium text-gray-900"
                ),
                class_name="flex items-center",
            ),
            class_name="px-4 py-3 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                file["ext"].upper(),
                class_name="px-2 py-1 text-[10px] font-bold tracking-wider text-blue-600 bg-blue-50 rounded-full border border-blue-100",
            ),
            class_name="px-4 py-3 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                f"{file['size_mb']:.1f} MB",
                class_name="text-xs font-mono text-gray-500",
            ),
            class_name="px-4 py-3 whitespace-nowrap",
        ),
        rx.el.td(
            rx.cond(
                has_proposal,
                rx.el.div(
                    rx.el.span(
                        file["name"],
                        class_name="text-xs text-gray-400 line-through mr-2 truncate max-w-[100px]",
                    ),
                    rx.icon(
                        "arrow-right",
                        class_name="w-3 h-3 text-blue-500 shrink-0 mx-1",
                    ),
                    rx.el.span(
                        rx.cond(
                            file["proposed_folder"] != "",
                            file["proposed_folder"] + "/",
                            "",
                        )
                        + rx.cond(
                            file["proposed_name"] != "",
                            file["proposed_name"],
                            file["name"],
                        ),
                        class_name="text-xs text-blue-700 font-medium truncate max-w-[150px]",
                    ),
                    class_name="flex items-center bg-blue-50/50 border border-blue-100/50 px-3 py-1.5 rounded-xl w-fit shadow-sm",
                ),
                rx.el.span(
                    file["status"].title(),
                    class_name="px-2 py-1 text-[10px] font-bold tracking-widest uppercase text-gray-500 bg-gray-100 rounded-md",
                ),
            ),
            class_name="px-4 py-3 whitespace-nowrap",
        ),
        class_name=rx.cond(
            is_selected,
            "bg-blue-50 hover:bg-blue-100 transition-colors border-b border-gray-100",
            "bg-white hover:bg-gray-50 transition-colors border-b border-gray-100",
        ),
    )


def file_table() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            rx.el.input(
                                type="checkbox",
                                checked=OrganizerState.selected_count > 0,
                                on_change=OrganizerState.toggle_all,
                                aria_label="Select all files for organization",
                                class_name="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 cursor-pointer",
                            ),
                            class_name="px-4 py-3 text-left w-10 bg-gray-50 border-b border-gray-200",
                        ),
                        rx.el.th(
                            rx.el.div(
                                rx.icon("file-text", class_name="w-4 h-4 mr-2"),
                                "Name",
                                class_name="flex items-center",
                            ),
                            class_name="px-4 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider bg-gray-50 border-b border-gray-200",
                        ),
                        rx.el.th(
                            "Extension",
                            class_name="px-4 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider bg-gray-50 border-b border-gray-200",
                        ),
                        rx.el.th(
                            "File Size",
                            class_name="px-4 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider bg-gray-50 border-b border-gray-200",
                        ),
                        rx.el.th(
                            "Automated Target",
                            class_name="px-4 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider bg-gray-50 border-b border-gray-200",
                        ),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(OrganizerState.filtered_files, file_row)
                ),
                class_name="min-w-full table-auto",
            ),
            class_name="overflow-auto max-h-[600px] border border-gray-200 rounded-lg bg-white shadow-sm",
        ),
        rx.cond(
            OrganizerState.filtered_files.length() == 0,
            rx.el.div(
                rx.icon(
                    "folder-open", class_name="w-12 h-12 text-gray-300 mb-3"
                ),
                rx.el.p(
                    "No files to display",
                    class_name="text-sm text-gray-500 font-medium",
                ),
                rx.el.p(
                    "Select a folder and scan to view contents.",
                    class_name="text-xs text-gray-400 mt-1",
                ),
                class_name="flex flex-col items-center justify-center py-20 border border-dashed border-gray-300 rounded-lg bg-gray-50 mt-4",
            ),
        ),
    )