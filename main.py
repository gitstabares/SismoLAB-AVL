"""NiceGUI dashboard for monitoring and managing seismic events.

The application visualizes AVL and BST trees, presents reports, supports
filtering, and stores the current scenario state. It is built around the
:class:`src.model.Scenario` model and the NiceGUI interface.
"""

import json
import re
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
    .q-drawer__content {
        overflow: hidden !important;
    }
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
    """Create the application header and global controls.

    The header contains the application title, date and time controls, stress and
    burst modes, scenario parameters, undo/redo actions, persistence controls, and
    report upload support.
    """
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
            global global_state
            try:
                file = await e.file.text()
                ui.notify('The file was uploaded successfully')
                new_global_state = serializer.deserialize(json.loads(file))
                global_state.__dict__.update(new_global_state.__dict__)
                global_state.refresh()
            except:
                ui.notify("The file doesn't have an appropiate format")

        ui.number(prefix='W : ',min=0,value=48,validation={'W must be a positive number':lambda v:v is not None and v >= 0},on_change=lambda e:global_state.set_W(e.value)).classes('w-50').tooltip('Temporal margin for aftershocks')
        ui.number(prefix='R : ',min=0,value=40,validation={'R must be a positive number':lambda v:v is not None and v >= 0},on_change=lambda e:global_state.set_R(e.value)).classes('w-50').tooltip('Spatial margin for aftershocks')
        ui.number(prefix='L : ',min=0,value=3,validation={'L must be a positive number':lambda v:v is not None and v >= 0},on_change=lambda e:global_state.set_L(e.value)).classes('w-50').tooltip('Costly access limit')
        ui.button(icon='undo',on_click=lambda: global_state.undo()).props('round').tooltip('Undo').bind_enabled_from(global_state,'can_undo')
        ui.button(icon='redo',on_click=lambda: global_state.redo()).props('round').tooltip('Redo').bind_enabled_from(global_state,'can_redo')
        ui.button(icon='save',on_click=lambda: ui.download.content(json.dumps(serializer.serialize(global_state),indent=4),'savestate.json')).props('round').tooltip('Save state')
        ui.upload(on_upload=lambda e:upload(e),on_rejected=lambda:ui.notify("The file couldn't be uploaded"),auto_upload=True)

def show_event(e):
    """Show a dialog with the details of an event selected in a tree.

    Args:
        e: Click event generated by an AVL or BST tree node.

    Raises:
        KeyError: If the selected event identifier is not present in the active
            AVL tree.
    """

    identifier = e.name[4:]
    nodo = global_state.get_event_AVL(int(identifier))
    with ui.dialog() as dialog,ui.card(align_items='end'):
        with ui.list().props('dense separator'):
            for k,v in nodo.__dict__.items():
                ui.item(f'{k[1:].capitalize()}:{str(v)}')

        def delete_and_close(node:Node):
            global_state.delete_event(node.get_key())
            dialog.close()

        def archive_and_close(node:Node):
            global_state.archive_event(node.get_key())
            dialog.close()

        with ui.row().classes('w-full'):
            ui.button(icon='archive',on_click=lambda e:archive_and_close(nodo)).props('round').tooltip('Archive event')
            ui.button(icon='delete',on_click=lambda e:delete_and_close(nodo)).props('round').tooltip('Delete event')
    dialog.open()

def AVL_tree():
    """Render the AVL tree and keep it synchronized with the scenario state.

    The tree is displayed as an ECharts graph and emits a click event when an
    event node is selected.
    """

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
    """Render the BST tree and keep it synchronized with the scenario state.

    The tree is displayed as an ECharts graph and emits a click event when an
    event node is selected.
    """
    with ui.column().classes('dashboard-card col-span-5 h-full'):
        with ui.row().classes('items-center'):
            ui.icon('account_tree', size='sm').classes('text-cyan-400')
            ui.label('BST Tree').classes('title')
        with ui.card().classes('w-full bg-white h-full'):
            bst_graph = ui.echart(global_state.get_BST_JSON()).classes('w-full h-full').on_click(show_event)

    @OnEvent(Scenario.refresh)
    def update_BST_tree():
        bst_graph._props['options'] = global_state.get_BST_JSON()
        bst_graph.update()

def reports_queue():
    """Render the queued reports and provide a control to send one to the tree.

    The queue is rebuilt whenever the scenario refreshes.
    """
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
    """Render the form used to create a new seismic report.

    The form collects event data, derives its epicenter from the supplied
    coordinates, and inserts the resulting report into the active scenario.
    """
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
    """Render the global event map with radius-scaled earthquake markers.

    Each AVL event is transformed from the application's coordinate system into
    the geographic bounds used by the Leaflet map and colored according to its
    magnitude.
    """
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
                        'radius': (seism.get_magnitude()+2) * 1e5,
                        'weight': 1,
                    }
                ]
            ).run_method('bindTooltip', f'<b>{seism.get_key()}</b> <br>{seism.get_epicenter()}')

def filter_events():
    """Render an event filter and display the matching results.

    Filters use expressions such as ``magnitude>=5`` or ``deepness<10``. Invalid
    expressions produce a notification and leave the previous result set intact.
    """
    with ui.column().classes('dashboard-card col-span-4 h-full'):
        with ui.row().classes('items-center'):
            ui.icon('search', size='sm').classes('text-cyan-400')
            ui.label('Filtering events').classes('title text-2xl')
        ui.input_chips(on_change=lambda e:update_results(e)).classes('w-full')
        with ui.scroll_area().classes('h-full').props('visible=false'):
            results_list = ui.list().props('dense separator')

        def update_results(e):
            results = global_state.get_AVL().get_levelorder_traverse()
            for filter in e.value:
                try:
                    oper = re.split(r'(>=|<=|==|!=|>|<)',filter)
                    results = eval(f'[seism for seism in results if seism.get_{oper[0]}() {oper[1]} {oper[2]}]')
                except:
                    ui.notify("One or more filters are unvalid")
            results_list.clear()
            with results_list:
                for result in results:
                    ui.item(str(result))

def left_drawer():
    """Create the secondary drawer with archived trees and eliminated IDs.

    The drawer expands on mouse hover and refreshes its contents whenever the
    scenario changes.
    """
    with ui.left_drawer().classes('dashboard-card').props('mini') as drawer:
        with ui.column().classes('h-1/2 w-full min-w-[280px] shrink-0'):
            with ui.row().classes('items-center'):
                ui.icon('forest', size='sm').classes('text-cyan-400')
                ui.label('Archived Trees').classes('title text-2xl')
            archived_trees = ui.scroll_area()

        def build_tree(event):
            if event is None:
                return None
            node = {
                'id': str(event.get_key()),
                'children': []
            }
            left = build_tree(event.get_left())
            right = build_tree(event.get_right())
            if left is not None:
                node['children'].append(left)
            if right is not None:
                node['children'].append(right)
            return node

        @OnEvent(Scenario.refresh)
        def update_archived_trees():
            archived_trees.clear()
            with archived_trees:
                for tree in global_state.get_archived_trees():
                    root = tree.get_root()
                    if root is None:
                        continue
                    tree_data = build_tree(root)
                    ui.tree(
                        [tree_data],
                        label_key='id',
                    ).props('default-expand-all')
                    ui.separator()

        with ui.column().classes('h-1/2 w-full min-w-[280px] shrink-0'):
            with ui.row().classes('items-center'):
                ui.icon('folder_delete', size='sm').classes('text-cyan-400')
                ui.label('Eliminated IDs').classes('title text-2xl')
            with ui.scroll_area():
                eliminated_ids = ui.list().classes('w-full').props('dense separator')

        @OnEvent(Scenario.refresh)
        def update_archived_trees():
            with eliminated_ids:
                eliminated_ids.clear()
                for node in global_state.get_eliminated_ids():
                    ui.item(str(node))

        drawer.on('mouseenter', lambda: drawer.props('mini-to-overlay',remove='mini'))
        drawer.on('mouseleave', lambda: drawer.props('mini'))

def main():
    """Build and launch the complete SismoLab AVL dashboard.

    The function creates every dashboard region, then starts the NiceGUI
    application and triggers an initial state refresh.
    """
    left_drawer()
    header()
    with ui.row().classes('w-full grid grid-cols-12 min-h-[1000px]'):
        AVL_tree()
        BST_tree()
        reports_queue()
        events_map()
        add_event_form()
        filter_events()

if __name__ in {"__main__", "__mp_main__"}:
    main()
    ui.run(title='SismoLab AVL', dark=True, favicon='assets/icon.svg')
    global_state.refresh()