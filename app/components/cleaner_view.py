import reflex as rx
from app.states.cleaner_state import CleanerState, CleanItem


def item_row(item: CleanItem) -> rx.Component:
    is_selected = CleanerState.selected_item_ids.contains(item["id"])

    return rx.el.tr(
        rx.el.td(
            rx.el.label(
                rx.el.div(
                    rx.el.input(
                        type="checkbox",
                        checked=is_selected,
                        on_change=lambda: CleanerState.toggle_item(item["id"]),
                        disabled=item["protected"],
                        class_name="peer sr-only",
                    ),
                    rx.el.div(
                        rx.icon(
                            "check",
                            class_name="w-3 h-3 text-white opacity-0 peer-checked:opacity-100 transition-opacity",
                        ),
                        class_name=rx.cond(
                            item["protected"],
                            "w-5 h-5 rounded-md border-2 border-[#e2e8f0] bg-gray-100 flex items-center justify-center",
                            "w-5 h-5 rounded-md border-2 border-[#d0d7e5] peer-checked:border-[#4b71ff] peer-checked:bg-[#4b71ff] flex items-center justify-center transition-colors cursor-pointer",
                        ),
                    ),
                )
            ),
            class_name="px-4 py-3 whitespace-nowrap w-10",
        ),
        rx.el.td(
            rx.el.div(
                rx.icon(
                    rx.match(
                        item["category"],
                        ("duplicates", "copy"),
                        ("applications", "app-window"),
                        ("caches", "database"),
                        "file",
                    ),
                    class_name="w-4 h-4 text-[#8ba3c7] mr-3",
                ),
                rx.el.div(
                    rx.el.span(
                        item["name"],
                        class_name="text-sm font-semibold text-[#1e293b] block",
                    ),
                    rx.el.span(
                        item["path"],
                        class_name="text-[11px] font-mono text-[#8ba3c7] truncate max-w-xs block mt-0.5",
                    ),
                ),
                class_name="flex items-center",
            ),
            class_name="px-4 py-4",
        ),
        rx.el.td(
            rx.el.span(
                f"{item['size_mb']:.1f} MB",
                class_name="text-xs font-mono font-medium text-[#6b7b93]",
            ),
            class_name="px-4 py-3 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.cond(
                    item["risk_level"] == "low",
                    rx.el.span(
                        "Low Risk",
                        class_name="px-2.5 py-1 text-[10px] font-bold tracking-widest uppercase text-[#059669] bg-[#d1fae5] rounded-md",
                    ),
                    rx.cond(
                        item["risk_level"] == "medium",
                        rx.el.span(
                            "Medium Risk",
                            class_name="px-2.5 py-1 text-[10px] font-bold tracking-widest uppercase text-[#d97706] bg-[#fef3c7] rounded-md",
                        ),
                        rx.el.span(
                            "High Risk",
                            class_name="px-2.5 py-1 text-[10px] font-bold tracking-widest uppercase text-[#dc2626] bg-[#fee2e2] rounded-md",
                        ),
                    ),
                ),
                rx.cond(
                    item["protected"],
                    rx.el.span(
                        rx.icon(
                            "shield-alert",
                            class_name="w-3 h-3 mr-1.5 inline-block",
                        ),
                        "Protected",
                        class_name="ml-2 px-2.5 py-1 text-[10px] font-bold tracking-widest uppercase bg-[#f0f4f8] text-[#6b7b93] rounded-md flex items-center w-fit",
                    ),
                ),
                class_name="flex items-center",
            ),
            class_name="px-4 py-3 whitespace-nowrap",
        ),
        class_name=rx.cond(
            item["protected"],
            "bg-[#f8fafc] border-b border-[#e2e8f0] opacity-75",
            rx.cond(
                is_selected,
                "bg-[#f0f4ff] hover:bg-[#e4ebff] transition-colors border-b border-[#e2e8f0]",
                "bg-white hover:bg-[#f4f7fb] transition-colors border-b border-[#e2e8f0]",
            ),
        ),
    )


def cleaner_view() -> rx.Component:
    return rx.el.div(
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "System Cleaner",
                        class_name="text-2xl font-bold text-[#1e293b] tracking-tight",
                    ),
                    rx.el.p(
                        "Safe recovery of disk space from redundant system items.",
                        class_name="text-sm text-[#6b7b93] font-medium mt-1",
                    ),
                    class_name="flex-1",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            "POTENTIAL RECOVERY",
                            class_name="text-[10px] font-bold text-[#8ba3c7] tracking-wider",
                        ),
                        rx.el.span(
                            f"{CleanerState.total_selected_size_mb:.1f}MB",
                            class_name="text-xl font-mono font-bold text-[#ef4444]",
                        ),
                        class_name="flex flex-col items-end bg-white px-5 py-2.5 rounded-[16px] border border-[#e2e8f0] shadow-sm",
                    ),
                    class_name="flex gap-4",
                ),
                class_name="flex items-center justify-between mb-8 pb-6 border-b border-[#e2e8f0]",
            ),
            aria_labelledby="cleaner-title",
            id="cleaner-title",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.button(
                    "All",
                    on_click=lambda: CleanerState.set_category_filter("all"),
                    class_name=rx.cond(
                        CleanerState.category_filter == "all",
                        "px-4 py-1.5 text-xs font-bold bg-[#4b71ff] text-white rounded-full shadow-sm",
                        "px-4 py-1.5 text-xs font-semibold text-[#6b7b93] hover:text-[#1e293b] hover:bg-[#e2e8f0] rounded-full transition-colors",
                    ),
                ),
                rx.el.button(
                    "Duplicates",
                    on_click=lambda: CleanerState.set_category_filter(
                        "duplicates"
                    ),
                    class_name=rx.cond(
                        CleanerState.category_filter == "duplicates",
                        "px-4 py-1.5 text-xs font-bold bg-[#4b71ff] text-white rounded-full shadow-sm",
                        "px-4 py-1.5 text-xs font-semibold text-[#6b7b93] hover:text-[#1e293b] hover:bg-[#e2e8f0] rounded-full transition-colors",
                    ),
                ),
                rx.el.button(
                    "Applications",
                    on_click=lambda: CleanerState.set_category_filter(
                        "applications"
                    ),
                    class_name=rx.cond(
                        CleanerState.category_filter == "applications",
                        "px-4 py-1.5 text-xs font-bold bg-[#4b71ff] text-white rounded-full shadow-sm",
                        "px-4 py-1.5 text-xs font-semibold text-[#6b7b93] hover:text-[#1e293b] hover:bg-[#e2e8f0] rounded-full transition-colors",
                    ),
                ),
                rx.el.button(
                    "Caches",
                    on_click=lambda: CleanerState.set_category_filter("caches"),
                    class_name=rx.cond(
                        CleanerState.category_filter == "caches",
                        "px-4 py-1.5 text-xs font-bold bg-[#4b71ff] text-white rounded-full shadow-sm",
                        "px-4 py-1.5 text-xs font-semibold text-[#6b7b93] hover:text-[#1e293b] hover:bg-[#e2e8f0] rounded-full transition-colors",
                    ),
                ),
                class_name="flex items-center gap-1 bg-[#f0f4f8] p-1 rounded-full",
            ),
            rx.el.div(
                rx.el.button(
                    rx.cond(
                        CleanerState.is_scanning,
                        rx.icon(
                            "loader", class_name="w-4 h-4 mr-2 animate-spin"
                        ),
                        rx.icon("search", class_name="w-4 h-4 mr-2"),
                    ),
                    "Scan System",
                    on_click=CleanerState.scan_system,
                    disabled=CleanerState.is_scanning,
                    class_name="flex items-center px-5 py-2.5 bg-[#4b71ff] hover:bg-[#3a5be0] text-white text-sm font-semibold rounded-full shadow-[0_2px_8px_rgba(75,113,255,0.3)] disabled:opacity-50 transition-colors",
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="flex items-center justify-between mb-6",
        ),
        rx.cond(
            CleanerState.is_scanning,
            rx.el.div(
                rx.el.div(
                    class_name="h-1.5 bg-[#4b71ff] rounded-full transition-all duration-300",
                    style={"width": f"{CleanerState.scan_progress}%"},
                ),
                class_name="w-full h-1.5 bg-[#f0f4f8] rounded-full overflow-hidden mb-6",
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    rx.el.label(
                                        rx.el.div(
                                            rx.el.input(
                                                type="checkbox",
                                                checked=CleanerState.selected_item_ids.length()
                                                > 0,
                                                on_change=CleanerState.toggle_all,
                                                class_name="peer sr-only",
                                            ),
                                            rx.el.div(
                                                rx.icon(
                                                    "check",
                                                    class_name="w-3 h-3 text-white opacity-0 peer-checked:opacity-100 transition-opacity",
                                                ),
                                                class_name="w-5 h-5 rounded-md border-2 border-[#d0d7e5] peer-checked:border-[#4b71ff] peer-checked:bg-[#4b71ff] flex items-center justify-center transition-colors cursor-pointer",
                                            ),
                                        )
                                    ),
                                    class_name="px-4 py-3 text-left w-10 bg-[#f4f7fb] border-b border-[#e2e8f0]",
                                ),
                                rx.el.th(
                                    rx.el.div(
                                        rx.icon(
                                            "file-search",
                                            class_name="w-4 h-4 mr-2",
                                        ),
                                        "System Item",
                                        class_name="flex items-center text-[#8ba3c7]",
                                    ),
                                    class_name="px-4 py-3 text-left text-[11px] font-bold uppercase tracking-widest bg-[#f4f7fb] border-b border-[#e2e8f0]",
                                ),
                                rx.el.th(
                                    "Disk Size",
                                    class_name="px-4 py-3 text-left text-[11px] font-bold text-[#8ba3c7] uppercase tracking-widest bg-[#f4f7fb] border-b border-[#e2e8f0]",
                                ),
                                rx.el.th(
                                    "Safety Level",
                                    class_name="px-4 py-3 text-left text-[11px] font-bold text-[#8ba3c7] uppercase tracking-widest bg-[#f4f7fb] border-b border-[#e2e8f0]",
                                ),
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(CleanerState.filtered_items, item_row)
                        ),
                        class_name="min-w-full table-auto",
                    ),
                    class_name="overflow-auto max-h-[600px] border border-[#e2e8f0] rounded-[24px] bg-white shadow-[0_4px_20px_rgba(0,0,0,0.02)]",
                ),
                rx.cond(
                    CleanerState.filtered_items.length() == 0,
                    rx.el.div(
                        rx.icon(
                            "shield-check",
                            class_name="w-12 h-12 text-[#8ba3c7] mb-3 opacity-50",
                        ),
                        rx.el.p(
                            "System looks clean!",
                            class_name="text-sm text-[#3b4b63] font-semibold",
                        ),
                        rx.el.p(
                            "Scan the system to find unused files and caches.",
                            class_name="text-xs text-[#8ba3c7] mt-1",
                        ),
                        class_name="flex flex-col items-center justify-center py-20 border-2 border-dashed border-[#e2e8f0] rounded-[24px] bg-[#f8fafc] mt-4",
                    ),
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.h3(
                    "STORAGE IMPACT",
                    class_name="text-[11px] font-bold text-[#8ba3c7] mb-4 uppercase tracking-widest font-mono",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            "Selected Items",
                            class_name="text-xs font-semibold text-[#6b7b93]",
                        ),
                        rx.el.span(
                            f"{CleanerState.selected_item_ids.length()}",
                            class_name="text-sm font-bold text-[#1e293b]",
                        ),
                        class_name="flex justify-between py-3 border-b border-[#e2e8f0]",
                    ),
                    rx.el.div(
                        rx.el.span(
                            "Recoverable Space",
                            class_name="text-xs font-semibold text-[#6b7b93]",
                        ),
                        rx.el.span(
                            f"{CleanerState.total_selected_size_mb:.1f} MB",
                            class_name="text-sm font-bold text-[#4b71ff]",
                        ),
                        class_name="flex justify-between py-3",
                    ),
                    class_name="bg-[#f4f7fb] rounded-2xl p-4 mb-6 border border-[#e2e8f0]",
                ),
                rx.cond(
                    CleanerState.has_high_risk_selected,
                    rx.el.div(
                        rx.icon(
                            "triangle_alert",
                            class_name="w-5 h-5 text-[#ef4444] mb-2",
                        ),
                        rx.el.p(
                            "High risk items selected. Verify before proceeding.",
                            class_name="text-[11px] text-[#b91c1c] font-bold text-center uppercase tracking-wide",
                        ),
                        class_name="flex flex-col items-center justify-center p-4 mb-6 bg-[#fef2f2] border border-[#fca5a5] rounded-2xl",
                    ),
                ),
                rx.el.h3(
                    "CLEANUP ACTIONS",
                    class_name="text-[11px] font-bold text-[#8ba3c7] mb-4 uppercase tracking-widest font-mono",
                ),
                rx.el.button(
                    "Delete Selected",
                    on_click=CleanerState.apply_cleanup,
                    disabled=CleanerState.selected_item_ids.length() == 0,
                    class_name="w-full flex justify-center items-center px-5 py-2.5 bg-[#ef4444] hover:bg-[#dc2626] text-white text-sm font-semibold rounded-full shadow-[0_2px_8px_rgba(239,68,68,0.3)] disabled:opacity-50 disabled:cursor-not-allowed transition-colors",
                ),
                rx.cond(
                    CleanerState.history.length() > 0,
                    rx.el.div(
                        rx.el.h3(
                            "RECENT CLEANUPS",
                            class_name="text-[11px] font-bold text-[#8ba3c7] mt-8 mb-4 uppercase tracking-widest font-mono",
                        ),
                        rx.el.div(
                            rx.foreach(
                                CleanerState.history,
                                lambda h: rx.el.div(
                                    rx.el.div(
                                        rx.el.span(
                                            h["description"],
                                            class_name="text-xs font-semibold text-[#3b4b63]",
                                        ),
                                        rx.cond(
                                            h["reversible"],
                                            rx.el.button(
                                                rx.icon(
                                                    "undo-2",
                                                    class_name="w-3.5 h-3.5",
                                                ),
                                                on_click=lambda: (
                                                    CleanerState.undo_cleanup(
                                                        h["id"]
                                                    )
                                                ),
                                                class_name="p-1.5 text-[#8ba3c7] hover:text-[#4b71ff] hover:bg-[#e4ebff] rounded-lg transition-colors",
                                            ),
                                        ),
                                        class_name="flex items-center justify-between",
                                    ),
                                    rx.el.p(
                                        f"Recovered {h['recovered_mb']:.1f} MB",
                                        class_name="text-[11px] font-mono text-[#8ba3c7] mt-1",
                                    ),
                                    class_name="p-3.5 bg-white border border-[#e2e8f0] rounded-xl mb-2 shadow-sm",
                                ),
                            ),
                            class_name="max-h-48 overflow-y-auto pr-1",
                        ),
                    ),
                ),
                class_name="w-[320px] bg-white border border-[#e2e8f0] rounded-[24px] shadow-[0_4px_20px_rgba(0,0,0,0.02)] p-6 flex-shrink-0 h-fit sticky top-6",
            ),
            class_name="flex flex-col lg:flex-row gap-8",
        ),
        class_name="flex-1 p-8 overflow-y-auto",
    )