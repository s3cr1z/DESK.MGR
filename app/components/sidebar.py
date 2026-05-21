import reflex as rx


def nav_item(label: str, href: str = "#", active: bool = False) -> rx.Component:
    return rx.el.a(
        rx.el.span(
            label,
            class_name=rx.cond(
                active,
                "text-[13px] font-semibold text-gray-900",
                "text-[13px] font-medium text-gray-500",
            ),
        ),
        href=href,
        class_name=rx.cond(
            active,
            "px-5 py-2 rounded-full bg-white shadow-[0_2px_8px_rgba(0,0,0,0.04)] transition-all duration-200",
            "px-5 py-2 rounded-full hover:text-gray-900 transition-all duration-200",
        ),
    )


def navigation_bar(current_page: str = "organizer") -> rx.Component:
    return rx.el.header(
        rx.el.div(
            # Brand/Logo
            rx.el.div(
                rx.el.span(
                    "renamer",
                    class_name="font-bold text-gray-900 tracking-tight text-lg",
                ),
                rx.el.span(
                    ".ai", class_name="text-[#8ba3c7] font-bold text-lg"
                ),
                class_name="flex items-center",
            ),
            # Top Segmented Tabs
            rx.el.nav(
                rx.el.div(
                    nav_item(
                        "Rename files",
                        href="/",
                        active=current_page == "organizer",
                    ),
                    nav_item(
                        "Magic folders",
                        href="/cleaner",
                        active=current_page == "cleaner",
                    ),
                    class_name="flex items-center gap-1 bg-[#ebeef3] p-1 rounded-full",
                ),
                class_name="hidden md:flex justify-center flex-1 absolute left-1/2 -translate-x-1/2",
            ),
            # Right-side utility icon cluster
            rx.el.div(
                rx.el.div(
                    rx.el.a(
                        rx.icon(
                            "settings",
                            class_name="w-[18px] h-[18px] text-gray-600",
                        ),
                        href="/settings",
                        class_name="w-9 h-9 flex items-center justify-center bg-white rounded-full shadow-sm border border-gray-100 transition-colors hover:bg-gray-50",
                    ),
                    rx.el.button(
                        rx.icon(
                            "bell", class_name="w-[18px] h-[18px] text-gray-600"
                        ),
                        rx.el.span(
                            "2",
                            class_name="absolute -top-1 -right-1 bg-[#ff4a4a] text-white text-[10px] font-bold w-4 h-4 flex items-center justify-center rounded-full border border-white",
                        ),
                        class_name="w-9 h-9 flex items-center justify-center bg-white rounded-full shadow-sm border border-gray-100 transition-colors hover:bg-gray-50 relative",
                    ),
                    rx.el.button(
                        rx.icon(
                            "menu", class_name="w-[18px] h-[18px] text-gray-600"
                        ),
                        class_name="w-9 h-9 flex items-center justify-center bg-white rounded-full shadow-sm border border-gray-100 transition-colors hover:bg-gray-50",
                    ),
                    class_name="flex items-center gap-3",
                ),
                class_name="flex items-center justify-end z-10",
            ),
            class_name="flex items-center justify-between w-full px-6",
        ),
        class_name="fixed top-0 left-0 right-0 h-20 bg-transparent flex flex-col justify-center z-50",
    )