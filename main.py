from nicegui import ui
from src.model import *

with ui.input('Fecha').props('readonly') as inp:
    with inp.add_slot('append'):
        ui.icon('event').classes('cursor-pointer').on('click', lambda: menu.open())
        with ui.menu() as menu:
            def show_time():
                date_input.set_visibility(False)
                time_input.set_visibility(True)
            def show_date():
                date_input.set_visibility(True)
                time_input.set_visibility(False)
                menu.close()
            with ui.date() as date_input:
                ui.button(icon='arrow_forward', on_click=show_time).props('round')
            with ui.time() as time_input:
                time_input.set_visibility(False)
                ui.button(icon='done', on_click=show_date).props('round')
            menu.on('hide', lambda e:inp.set_value(f"{date_input.value}T{time_input.value}"))
mapa = ui.leaflet(
    center=(5.0675, 500.71),
    zoom=1,
        options={
        'maxBounds': [[-85.051129, -180], [85.051129, 180]],
        'maxBoundsViscosity': 1.0,
    }).style('width: 800px; height: 500px;')
mapa.marker(latlng=Point(5.0675, 500.71))

ui.run()