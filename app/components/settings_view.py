import reflex as rx
from app.states.settings_state import SettingsState


def settings_view() -> rx.Component:
    return rx.el.div(
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Application Settings",
                        class_name="text-2xl font-bold text-[#1e293b] tracking-tight",
                    ),
                    rx.el.p(
                        "Configure file management preferences, exclusions, and cloud integrations.",
                        class_name="text-sm text-[#6b7b93] font-medium mt-1",
                    ),
                    class_name="flex-1",
                ),
                class_name="flex items-center justify-between mb-8 pb-6 border-b border-[#e2e8f0]",
            ),
            aria_labelledby="settings-title",
            id="settings-title",
        ),
        rx.el.div(
            # Contextual framing
            rx.el.div(
                rx.el.h3(
                    "PROCESSING PREFERENCES",
                    class_name="text-[11px] font-bold text-[#8ba3c7] mb-4 tracking-widest font-mono",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "AI Processing Mode",
                            class_name="block text-xs font-bold text-[#3b4b63] mb-2 uppercase tracking-wide",
                        ),
                        rx.el.div(
                            rx.el.select(
                                rx.el.option(
                                    "Local (Fast, Private)", value="local"
                                ),
                                rx.el.option(
                                    "Cloud (Advanced, requires API Key)",
                                    value="cloud",
                                ),
                                value=SettingsState.settings.processing_mode,
                                on_change=SettingsState.update_processing_mode,
                                class_name="w-full max-w-md appearance-none bg-[#f0f4f8] text-[#3b4b63] text-sm font-medium px-4 py-3 rounded-[16px] border border-transparent focus:border-blue-300 focus:ring-2 focus:ring-blue-100 transition-all cursor-pointer outline-none",
                            ),
                            rx.icon(
                                "chevron-down",
                                class_name="absolute right-4 top-1/2 -translate-y-1/2 h-4 w-4 text-[#8ba3c7] pointer-events-none",
                            ),
                            class_name="relative max-w-md",
                        ),
                        class_name="mb-6",
                    ),
                    rx.cond(
                        SettingsState.settings.processing_mode == "cloud",
                        rx.el.div(
                            rx.el.label(
                                "Cloud API Key",
                                class_name="block text-xs font-bold text-[#3b4b63] mb-2 uppercase tracking-wide",
                            ),
                            rx.el.input(
                                type="password",
                                on_change=SettingsState.update_cloud_api_key.debounce(
                                    300
                                ),
                                placeholder="Enter your provider API key",
                                default_value=SettingsState.settings.cloud_api_key,
                                class_name="w-full max-w-md bg-[#f0f4f8] text-[#3b4b63] text-sm font-mono px-4 py-3 rounded-[16px] border border-transparent focus:border-blue-300 focus:ring-2 focus:ring-blue-100 transition-all outline-none",
                            ),
                            class_name="mb-6",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Scan Behavior",
                            class_name="block text-xs font-bold text-[#3b4b63] mb-2 uppercase tracking-wide",
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Fast (Surface level)",
                                on_click=lambda: (
                                    SettingsState.update_scan_behavior("fast")
                                ),
                                class_name=rx.cond(
                                    SettingsState.settings.scan_behavior
                                    == "fast",
                                    "px-5 py-2.5 text-xs font-bold rounded-full bg-[#4b71ff] text-white shadow-sm",
                                    "px-5 py-2.5 text-xs font-semibold rounded-full text-[#6b7b93] bg-[#f0f4f8] hover:bg-[#e4ebf3] transition-colors",
                                ),
                            ),
                            rx.el.button(
                                "Deep (Thorough)",
                                on_click=lambda: (
                                    SettingsState.update_scan_behavior("deep")
                                ),
                                class_name=rx.cond(
                                    SettingsState.settings.scan_behavior
                                    == "deep",
                                    "px-5 py-2.5 text-xs font-bold rounded-full bg-[#4b71ff] text-white shadow-sm",
                                    "px-5 py-2.5 text-xs font-semibold rounded-full text-[#6b7b93] bg-[#f0f4f8] hover:bg-[#e4ebf3] transition-colors",
                                ),
                            ),
                            class_name="flex items-center gap-2 bg-white p-1 rounded-full w-fit border border-[#e2e8f0]",
                        ),
                    ),
                    class_name="bg-white p-8 rounded-[24px] border border-[#e2e8f0] shadow-[0_4px_20px_rgba(0,0,0,0.02)] mb-10",
                ),
                rx.el.h3(
                    "PATH EXCLUSIONS",
                    class_name="text-[11px] font-bold text-[#8ba3c7] mb-4 tracking-widest font-mono",
                ),
                rx.el.div(
                    rx.el.p(
                        "Files in these paths will be completely ignored by both the Organizer and System Cleaner (simulated).",
                        class_name="text-sm text-[#6b7b93] mb-6",
                    ),
                    rx.el.form(
                        rx.el.div(
                            rx.el.input(
                                name="new_path",
                                placeholder="e.g. C:\\Development\\Projects",
                                class_name="flex-1 bg-[#f0f4f8] text-[#3b4b63] text-sm font-mono px-4 py-3 rounded-[16px] border border-transparent focus:border-blue-300 focus:ring-2 focus:ring-blue-100 transition-all outline-none",
                            ),
                            rx.el.button(
                                rx.icon(
                                    "folder-plus", class_name="w-4 h-4 mr-2"
                                ),
                                "Add Exclusion",
                                type="submit",
                                class_name="inline-flex items-center px-6 py-3 border border-transparent text-sm font-bold rounded-full shadow-[0_2px_8px_rgba(30,41,59,0.2)] text-white bg-[#1e293b] hover:bg-black transition-colors",
                            ),
                            class_name="flex gap-3 mb-6 max-w-xl",
                        ),
                        on_submit=SettingsState.add_excluded_path,
                        reset_on_submit=True,
                    ),
                    rx.el.div(
                        rx.cond(
                            SettingsState.settings.excluded_paths.length() > 0,
                            rx.el.ul(
                                rx.foreach(
                                    SettingsState.settings.excluded_paths,
                                    lambda p: rx.el.li(
                                        rx.el.span(
                                            p,
                                            class_name="text-xs text-[#3b4b63] font-mono bg-[#f4f7fb] px-3 py-1.5 rounded-[8px] border border-[#e2e8f0]",
                                        ),
                                        rx.el.button(
                                            rx.icon("x", class_name="w-4 h-4"),
                                            on_click=lambda: (
                                                SettingsState.remove_excluded_path(
                                                    p
                                                )
                                            ),
                                            class_name="text-[#8ba3c7] hover:text-[#ef4444] p-1.5 rounded-lg hover:bg-[#fef2f2] transition-colors ml-2",
                                        ),
                                        class_name="flex justify-between items-center py-3 border-b border-[#f4f7fb] last:border-0",
                                    ),
                                ),
                                class_name="divide-y divide-[#f4f7fb]",
                            ),
                            rx.el.div(
                                rx.icon(
                                    "shield",
                                    class_name="w-8 h-8 text-[#8ba3c7] opacity-50 mb-2",
                                ),
                                rx.el.p(
                                    "No paths excluded. All files will be scanned.",
                                    class_name="text-sm text-[#6b7b93] font-medium text-center",
                                ),
                                class_name="flex flex-col items-center justify-center py-8 border-2 border-dashed border-[#e2e8f0] rounded-[16px] bg-[#f8fafc]",
                            ),
                        ),
                    ),
                    class_name="bg-white p-8 rounded-[24px] border border-[#e2e8f0] shadow-[0_4px_20px_rgba(0,0,0,0.02)]",
                ),
                class_name="flex flex-col mb-8 bg-[#f8fafc] p-8 rounded-3xl border-2 border-dashed border-[#e2e8f0]",
            ),
            # Save / Cancel Action Bar Placeholder (visual only, settings auto-save)
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "circle_check",
                        class_name="w-4 h-4 text-[#10b981] mr-2",
                    ),
                    rx.el.span(
                        "Settings automatically saved",
                        class_name="text-sm text-[#6b7b93] font-medium",
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex justify-between items-center bg-white p-4 rounded-[16px] border border-[#e2e8f0] shadow-sm mt-8 max-w-4xl mx-auto",
            ),
            class_name="max-w-4xl mx-auto w-full",
        ),
        class_name="flex-1 p-8 overflow-y-auto w-full",
    )