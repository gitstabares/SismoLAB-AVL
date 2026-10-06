import json
from nicegui import ui
from nicegui.events import ValueChangeEventArguments
from src.model import *
from src.utils import *
import datetime as dt


reports = [
    Report(1001, 4.5, 15.0, 120.5, 340.2, "2026-10-01T08:30:00", "Station-Alpha", True, 2),
    Report(1002, 5.2, 30.5, 450.0, 512.1, "2026-10-01T14:15:00", "Station-Beta", False, 2),
    Report(1003, 3.1, 10.2, 890.1, 120.4, "2026-10-02T01:05:00", "Station-Gamma", True, 1),
    Report(1004, 6.8, 110.0, 320.4, 780.9, "2026-10-02T09:45:00", "Station-Delta", True, 3),
    Report(1005, 2.4, 5.0, 50.0, 50.0, "2026-10-02T16:20:00", "Station-Alpha", False, 1),
    Report(1006, 4.9, 45.3, 670.2, 300.8, "2026-10-03T03:10:00", "Station-Epsilon", True, 2),
    Report(1007, 7.1, 220.5, 910.0, 920.0, "2026-10-03T06:50:00", "Station-Beta", False, 4),
    Report(1008, 3.5, 18.2, 150.3, 430.6, "2026-10-03T09:12:00", "Station-Gamma", True, 1),
    Report(1009, 5.6, 85.4, 540.8, 620.1, "2026-10-03T10:30:00", "Station-Delta", True, 2),
    Report(1010, 1.8, 2.1, 200.0, 200.0, "2026-10-03T11:00:00", "Station-Epsilon", False, 1),
]

global_state = Scenario()
serializer = Serializer()
for _type in (Circle,EventTree,Event,Key,Node,Point,PopulatedZones,Report,Scenario,Tree,IntensityColorMapper):
    serializer.register(_type)

for report in reports:
    global_state.add_report(report)

ui.add_head_html('''
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,100..900;1,9..144,100..900&family=IBM+Plex+Mono:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;1,100;1,200;1,300;1,400;1,500;1,600;1,700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css?family=IBM+Plex+Mono&effect=fire-animation" rel="stylesheet">
''')
ui.add_css('''
    body {
        font-family: "IBM Plex Mono", monospace;
        font-weight: 400;
        font-style: normal;
        color: white;
    }
    .title {
        font-family: "Fraunces", serif;
        font-weight: 600;
        font-size: 20px;
        font-optical-sizing: auto;
        font-style: normal;
        font-variation-settings:
            "SOFT" 0,
            "WONK" 0;
        color: white;
    }
    .dashboard-card {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 0.5rem;
        padding: 1em;
    }
    .neon-cyan {
        color: #22d3ee;
    }
    .neon-orange {
        color: #fb923c;
    }
    .neon-green {
        color: #4ade80;
    }
    .border-cyan {
        border-color: #22d3ee !important;
    }
    .border-orange {
        border-color: #fb923c !important;
    }
    .border-green {
        border-color: #4ade80 !important;
    }
''')

def header():
    with ui.header(wrap=False).classes('items-center dashboard-card').style('border-radius:0px'):
        ui.image('assets/icon.svg').classes('w-10 h-auto')
        ui.label('SismoLab AVL').classes('title font-semibold text-3xl')
        ui.separator().props('vertical')

        date_picker = ui.date_input(value=global_state.get_current_time().date()).props('readonly borderless dark').style('width:140px').picker.on_value_change(lambda e:update_datetime())
        time_picker = ui.time_input(value=global_state.get_current_time().time()).props('readonly borderless dark mask=time').style('width:100px').picker.on_value_change(lambda e:update_datetime())

        def update_datetime():
            if not date_picker.value or not time_picker.value:
                date_picker.set_value(global_state.get_current_time().date())
                time_picker.set_value(global_state.get_current_time().time())
                return
            new_datetime = dt.datetime.fromisoformat(str(date_picker.value)+'T'+str(time_picker.value))
            if new_datetime < global_state.get_current_time():
                date_picker.value = global_state.get_current_time().date()
                time_picker.value = global_state.get_current_time().time()
                ui.notify('Invalid date or time, they just can go foward',position='top')
                return
            global_state.set_current_time(new_datetime)

        ui.checkbox('Stress mode',on_change=lambda e:update_stressmode(e)).props('unchecked-icon=local_fire_department checked-icon=local_fire_department keep_color=false').style('--q-primary: transparent;')
        ui.checkbox('Burst mode',on_change=lambda e:global_state.set_burst_mode(e.value)).props('unchecked-icon=burst_mode checked-icon=burst_mode color=red')
        
        def update_stressmode(e:ValueChangeEventArguments):
            if e.value:
                e.sender.classes('font-effect-fire-animation')
            else:
                e.sender._classes.clear()
            global_state.set_stress_mode(e.value)

        async def upload(e):
            content = await e.file.text()
            loaded = serializer.deserialize(json.loads(content))

            if isinstance(loaded, list):
                # Validate all items before modifying the current scenario.
                if not all(isinstance(report, Report) for report in loaded):
                    ui.notify(
                        "The list must contain only reports.",
                        type="negative",
                    )
                    return

                processed = 0
                issues = []

                # Insert into the existing scenario without clearing its trees.
                for report in loaded:
                    try:
                        global_state.insert_report(report)
                        processed += 1
                    except Exception as error:
                        # Continue processing the remaining reports.
                        issues.append(
                            f"ID {report.get_identifier()}: {error}"
                        )

                global_state.refresh()
                ui.notify(
                    f"Processed without exceptions: {processed}/{len(loaded)}"
                )

                for issue in issues:
                    ui.notify(issue, type="warning")

            elif isinstance(loaded, Scenario):
                # Only a topology load replaces the current scenario.
                global_state.__dict__.update(loaded.__dict__)
                global_state.refresh()
                ui.notify("Scenario topology loaded successfully")

            else:
                ui.notify(
                    "Expected a report list or a Scenario.",
                    type="negative",
                )

        ui.number(prefix='W : ',min=0,value=48,validation={'W must be a positive number':lambda v:v is not None and v >= 0},on_change=lambda e:global_state.set_W(e.value)).classes('w-50').tooltip('Temporal margin for aftershocks')
        ui.number(prefix='R : ',min=0,value=40,validation={'R must be a positive number':lambda v:v is not None and v >= 0},on_change=lambda e:global_state.set_R(e.value)).classes('w-50').tooltip('Spatial margin for aftershocks')
        ui.number(prefix='L : ',min=0,value=3,validation={'L must be a positive number':lambda v:v is not None and v >= 0},on_change=lambda e:global_state.set_L(e.value)).classes('w-50').tooltip('Costly access limit')
        ui.button(icon='undo',on_click=lambda: global_state.undo()).props('round').tooltip('Undo').bind_enabled_from(global_state,'can_undo')
        ui.button(icon='redo',on_click=lambda: global_state.redo()).props('round').tooltip('Redo').bind_enabled_from(global_state,'can_redo')
        ui.button(icon='save',on_click=lambda: ui.download.content(json.dumps(serializer.serialize(global_state),indent=4),'savestate.json')).props('round').tooltip('Save state')
        ui.upload(on_upload=lambda e:upload(e),on_rejected=lambda:ui.notify("The file couldn't be uploaded"),auto_upload=True)

def show_event(e):

    identifier = e.name[4:]
    nodo = global_state.get_event_AVL(int(identifier))
    with ui.dialog() as dialog,ui.card(align_items='end'):
        with ui.list().props('dense separator'):
            for k,v in nodo.__dict__.items():
                ui.item(f'{k[1:].capitalize()}:{str(v)}')
        def delete_and_close(node:Node):
            global_state.delete_event(node.get_key())
            dialog.close()
        ui.button(icon='delete',on_click=lambda e:delete_and_close(nodo)).props('round')
    dialog.open()

def AVL_tree():

    with ui.column().classes('dashboard-card col-span-5 h-full'):
        with ui.row().classes('items-center'):
            ui.icon('account_tree', size='sm').classes('text-cyan-400')
            ui.label('AVL Tree').classes('title')
        with ui.card().classes('w-full bg-white h-full'):
            avl_graph = ui.echart(global_state.get_AVL_JSON()).classes('w-full h-full').on_click(show_event)

    @OnEvent(Scenario.refresh)
    def update_AVL_tree():
        avl_graph._props['options'] = global_state.get_AVL_JSON()
        avl_graph.update()

def BST_tree():
    with ui.column().classes('dashboard-card col-span-5 h-full'):
        with ui.row().classes('items-center'):
            ui.icon('account_tree', size='sm').classes('text-cyan-400')
            ui.label('BST Tree').classes('title')
        with ui.card().classes('w-full bg-white h-full'):
            bst_graph = ui.echart(global_state.get_BST_JSON()).classes('w-full h-full').on_click(show_event).on('mouseover',lambda:ui.notify('Pinga'))

    @OnEvent(Scenario.refresh)
    def update_BST_tree():
        bst_graph._props['options'] = global_state.get_BST_JSON()
        bst_graph.update()

def reports_queue():
    with ui.column().classes('dashboard-card col-span-2 h-full'):
        with ui.row().classes('w-full items-center'):
            ui.icon('queue', size='sm').classes('text-cyan-400')
            ui.label('Reports queue').classes('title')
            ui.button(icon='send',on_click=lambda e:send_report_from_queue()).classes('ml-auto').props('round').tooltip('Send next report')
        with ui.scroll_area().classes('h-full').props('visible=false'):
            queue = ui.list().props('dense separator')

    def send_report_from_queue():
        try:
            global_state.insert_report(global_state.reports_queue.popleft())
        except Exception as e:
            ui.notify(e)
        global_state.refresh()

    @OnEvent(Scenario.refresh)
    def update_reports_queue():
        try:
            with queue:
                queue.clear()
                for report in global_state.reports_queue:
                    ui.item(str(report))
        except Exception as e:
            ui.notify(e)

def add_event_form():
    with ui.row().classes('dashboard-card col-span-4 grid grid-cols-3 h-full'):
        with ui.row().classes('items-center col-span-3'):
            ui.icon('checklist', size='sm').classes('text-cyan-400')
            ui.label('New report form').classes('title')
            ui.button(icon='add',on_click=lambda e:add_event()).classes('ml-auto').props('round').tooltip('Add report')
        with ui.column():
            identifier = ui.number('Identifier',prefix='SIS-',validation={'The identifier must be bigger than zero':lambda v:v is not None and v > 0}).classes('w-full')
            magnitude = ui.number('Magnitude',min=-2,max=10,precision=1,validation={'The magnitude must be between -2.0 and 10.0':lambda v:v is not None and -2 <= v <= 10}).classes('w-full')
            deepness = ui.number('Deepness',min=0,precision=1,validation={'The deepness must be bigger or equal than zero':lambda v:v is not None and v >= 0}).classes('w-full')
        with ui.column():
            station = ui.input('Origin Station').classes('w-full')
            ui.label('Datetime')
            date = ui.date_input(value=global_state.get_current_time().date()).props('readonly borderless dark').classes('w-full').picker
            time = ui.time_input(value=global_state.get_current_time().time()).props('readonly borderless dark mask=time').classes('w-full').picker
        with ui.column():
            version = ui.number('Version',value=1,min=1,validation={'The version must be bigger than zero':lambda v:v is not None and v > 0}).classes('w-full')
            ui.label('Epicenter')
            with ui.row().classes('w-full no-wrap'):
                x = ui.number('X',min=0,max=1000,precision=1,validation={'The x coordinate of epicenter must be between 0 and 1000':lambda v:v is not None and 0 <= v <= 1000}).classes('w-1/2')
                y = ui.number('Y',min=0,max=1000,precision=1,validation={'The y coordinate of epicenter must be between 0 and 1000':lambda v:v is not None and 0 <= v <= 1000}).classes('w-1/2')

    def add_event():
        try:
            epicenter = Point(x.value,y.value)
            report = Report(identifier.value,
                            magnitude.value,
                            deepness.value,
                            x.value,
                            y.value,
                            str(date.value)+'T'+str(time.value),
                            station.value,
                            epicenter in global_state.get_populated_zones(),
                            version.value)
            global_state.add_report(report)
            ui.notify(f'The report {report} was succesfully created')
        except Exception as e:
            ui.notify(e)

def events_map():
    with ui.column().classes('dashboard-card col-span-4 h-full'):
        with ui.row().classes('items-center'):
            ui.icon('map', size='sm').classes('text-cyan-400')
            ui.label('Realtime events map').classes('title text-2xl')
        lat_min, lat_max = -85.051129, 85.051129
        lng_min, lng_max = -170.0, 190.0
        global_map = ui.leaflet(
            center=(0,0),
            zoom=1,
            options={
                'maxBounds': [[lat_min, lng_min], [lat_max, lng_max]],
                'maxBoundsViscosity': 1.0,
                'minZoom':1
            }
        ).classes('w-full h-full')

    @OnEvent(Scenario.refresh)
    def update_map():
        global_map.clear_layers()
        global_map.tile_layer(
            url_template='https://{s}.tile.osm.org/{z}/{x}/{y}.png',
            options={
                'attribution': '&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
            }
        )
        color_mapper = IntensityColorMapper(-2,10)
        for seism in global_state.get_AVL().get_levelorder_traverse():
            lng = lng_min + (seism.get_epicenter().get_x() / 1000) * (lng_max - lng_min)
            lat = lat_max - (seism.get_epicenter().get_y() / 1000) * (lat_max - lat_min)
            global_map.generic_layer(
                name='circle',
                args=[
                    [lat, lng],
                    {
                        'color': color_mapper.interpolate(seism.get_magnitude()),
                        'fillColor': color_mapper.interpolate(seism.get_magnitude()),
                        'fillOpacity': 0.1,
                        'radius': seism.get_magnitude() * 1e5,
                        'weight': 1
                    }
                ]
            )

def main():
    header()
    with ui.row().classes('w-full grid grid-cols-12 min-h-[1000px]'):
        AVL_tree()
        BST_tree()
        reports_queue()
        events_map()
        add_event_form()

if __name__ in {"__main__", "__mp_main__"}:
    main()
    ui.run(title='SismoLab AVL', dark=True, favicon='assets/icon.svg')