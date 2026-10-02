from nicegui import ui
from nicegui.html import div
from ..app.state import global_state

@ui.page("/")
def home():
    with ui.element('hero').classes('bg-[#F59E0B] w-full h-200px'):
        ui.label('SismoLAB').classes('self-center text-6xl')
    with ui.column(align_items='center').classes('bg-blue-100'):
        ui.label('SismoLAB')
        mapa = ui.leaflet(
            center=(5.0675, 500.71),
            zoom=1,
            options={
                'maxBounds': [[-85.051129, -180], [85.051129, 180]],
                'maxBoundsViscosity': 1.0,
            }
        ).style('width: 800px; height: 500px;')