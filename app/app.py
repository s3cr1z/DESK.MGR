import reflex as rx
from app.components.sidebar import navigation_bar
from app.components.organizer_view import organizer_view
from app.components.cleaner_view import cleaner_view
from app.components.settings_view import settings_view


def page_shell(content: rx.Component, current_page: str) -> rx.Component:
    return rx.el.div(
        navigation_bar(current_page=current_page),
        rx.el.main(
            rx.el.div(
                content,
                class_name="w-full max-w-5xl mx-auto bg-white rounded-[32px] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-gray-100 flex flex-col min-h-[calc(100vh-120px)] overflow-hidden",
            ),
            class_name="pt-24 pb-8 px-4 sm:px-6",
        ),
        class_name="min-h-screen w-full bg-[#f4f7fb] font-['Inter'] text-gray-900 antialiased",
    )


def index() -> rx.Component:
    return page_shell(organizer_view(), current_page="organizer")


def cleaner_page() -> rx.Component:
    return page_shell(cleaner_view(), current_page="cleaner")


def settings_page() -> rx.Component:
    return page_shell(settings_view(), current_page="settings")


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")
app.add_page(cleaner_page, route="/cleaner")
app.add_page(settings_page, route="/settings")