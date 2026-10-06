import glob

from nicegui import ui
from src.model import *
from src.utils.decorators import OnEvent
import datetime as dt
from src.utils.intensity_color_mapper import IntensityColorMapper


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
scenario_manager = ScenarioManager(global_state)

for r in reports:
    global_state.insert_report(r)

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
            global_state.get_AVL().set_autobalance(not e.value)

        ui.number(prefix='W : ',min=0,value=48,validation={'W must be a positive number':lambda v:v is not None and v >= 0},on_change=lambda e:global_state.get_AVL().set_W(e.value)).classes('w-50').tooltip('Temporal margin for aftershocks')
        ui.number(prefix='R : ',min=0,value=40,validation={'R must be a positive number':lambda v:v is not None and v >= 0},on_change=lambda e:global_state.get_AVL().set_R(e.value)).classes('w-50').tooltip('Spatial margin for aftershocks')
        ui.number(prefix='L : ',min=0,value=3,validation={'L must be a positive number':lambda v:v is not None and v >= 0},on_change=lambda e:global_state.get_AVL().set_L(e.value)).classes('w-50').tooltip('Costly access limit')
        ui.button(icon='undo').props('round').tooltip('Undo')
        ui.button(icon='redo').props('round').tooltip('Redo')

def AVL_tree():
    with ui.column().classes('dashboard-card col-span-5 h-full'):
        with ui.row().classes('items-center'):
            ui.icon('account_tree', size='sm').classes('text-cyan-400')
            ui.label('AVL Tree').classes('title')
        with ui.card().classes('w-full bg-white h-full'):
            avl_graph = ui.echart(global_state.get_AVL_JSON()).classes('w-full h-full')

    @OnEvent(global_state.insert_report)
    @OnEvent(global_state.delete_event)
    def update_AVL_tree():
        avl_graph._props['options'] = global_state.get_AVL_JSON()
        avl_graph.update()

def BST_tree():
    with ui.column().classes('dashboard-card col-span-5 h-full'):
        with ui.row().classes('items-center'):
            ui.icon('account_tree', size='sm').classes('text-cyan-400')
            ui.label('BST Tree').classes('title')
        with ui.card().classes('w-full bg-white h-full'):
            bst_graph = ui.echart(global_state.get_BST_JSON(),on_point_click=lambda e:ui.notify(e.value)).classes('w-full h-full')

    @OnEvent(global_state.insert_report)
    @OnEvent(global_state.delete_event)
    def update_BST_tree():
        bst_graph._props['options'] = global_state.get_BST_JSON()
        bst_graph.update()

def reports_queue():
    with ui.column().classes('dashboard-card col-span-2 h-full'):
        with ui.row().classes('w-full items-center'):
            ui.icon('queue', size='sm').classes('text-cyan-400')
            ui.label('Reports queue').classes('title')
            ui.button(icon='send',on_click=lambda e:global_state.insert_report(global_state.reports_queue.popleft())).classes('ml-auto').props('round').tooltip('Send next report')
        with ui.scroll_area().props('visible=false'):
            queue = ui.list().props('dense separator')

    @OnEvent(global_state.add_report)
    @OnEvent(global_state.insert_report)
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

    @OnEvent(global_state.insert_report)
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

    with ui.row().classes('w-full gap-3 grid grid-cols-1 lg:grid-cols-12 mb-3 items-center'):
        
        # Station Status list (Left - 3 cols)
        with ui.column().classes('dashboard-card p-2 col-span-3 flex flex-col gap-1.5'):
            for name, ms, status, col in [('EST-01 Alpha', '18 ms', 'ÓPTIMA', 'green'), 
                                        ('EST-02 Norte', '24 ms', 'ÓPTIMA', 'green'), 
                                        ('EST-03 Costa', '91 ms', 'INESTABLE', 'orange'), 
                                        ('EST-04 Cordillera', '31 ms', 'ÓPTIMA', 'green')]:
                with ui.row().classes('w-full justify-between items-center bg-[#070a0f] p-1.5 rounded border border-slate-800'):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('sensors', size='xs').classes('text-cyan-400')
                        with ui.column().classes('gap-0'):
                            ui.label(name).classes('text-xs font-bold text-white')
                            ui.label(status).classes(f'text-[9px] text-{col}-400')
                    ui.label(ms).classes('text-xs font-mono text-slate-400')

        # Telemetry Selected Details & Complexity Cost (Center - 6 cols)
        with ui.column().classes('dashboard-card p-3 col-span-6 flex flex-row items-center justify-between'):
            with ui.column().classes('gap-1'):
                ui.label('MODO SELECCIONADO').classes('text-[10px] text-slate-400')
                ui.badge('PENDIENTE', color='orange').classes('text-[10px]')
                ui.label('K=(P3, M6.2, I148)').classes('text-sm font-bold font-mono text-cyan-400')
                with ui.row().classes('gap-4 text-[11px] text-slate-400'):
                    ui.label('evento: S-148 / Andina Sur')
                    ui.label('zona: Z-04 Cordillera')
                    ui.label('réplica: S-144 (r+1)')

            with ui.row().classes('gap-6'):
                with ui.column().classes('gap-0 items-center bg-[#070a0f] p-2 rounded border border-slate-800'):
                    ui.label('MAGNITUD').classes('text-[9px] text-slate-400')
                    ui.label('6.2 Mw').classes('text-xs font-bold text-orange-400')
                with ui.column().classes('gap-0 items-center bg-[#070a0f] p-2 rounded border border-slate-800'):
                    ui.label('PROFUNDIDAD').classes('text-[9px] text-slate-400')
                    ui.label('18.4 km').classes('text-xs font-bold text-white')
                with ui.column().classes('gap-0 items-center bg-[#070a0f] p-2 rounded border border-slate-800'):
                    ui.label('LATENCIA').classes('text-[9px] text-slate-400')
                    ui.label('42 ms').classes('text-xs font-bold text-emerald-400')
                with ui.column().classes('gap-0 items-center bg-[#070a0f] p-2 rounded border border-slate-800'):
                    ui.label('RÉPLICAS').classes('text-[9px] text-slate-400')
                    ui.label('83').classes('text-xs font-bold text-cyan-400')

        # Search cost complexity (Right - 3 cols)
        with ui.column().classes('dashboard-card p-3 col-span-3 flex flex-col justify-center'):
            with ui.row().classes('w-full justify-between items-center mb-1'):
                ui.label('COSTO DE BÚSQUEDA').classes('text-[10px] text-slate-400')
                ui.label('4 comparaciones').classes('text-[10px] text-slate-500')
            ui.label('O(log n)').classes('text-2xl font-bold font-mono text-cyan-400')
            ui.label('óptimo: s 5  BST: 7').classes('text-[10px] text-slate-400 mt-1')

    with ui.row().classes('w-full gap-3 grid grid-cols-1 lg:grid-cols-12'):
        
        # 4. QUERIES, COST & ROLLBACK INSPECTION PANEL (Bottom - 12 cols)
        with ui.column().classes('dashboard-card p-3 col-span-12 flex flex-col'):
            with ui.row().classes('w-full justify-between items-center mb-2'):
                with ui.row().classes('items-center gap-1'):
                    ui.icon('search', size='xs').classes('text-cyan-400')
                    ui.label('Consultas, costo y retroceso').classes('text-xs font-bold text-cyan-400 tracking-wider')
                with ui.row().classes('items-center gap-3'):
                    with ui.row().classes('items-center gap-1 bg-[#16a34a]/20 px-2 py-0.5 rounded border border-emerald-600/50'):
                        ui.icon('check', size='xs').classes('text-emerald-400')
                        ui.label('ÍNDICE CONSISTENTE').classes('text-[10px] font-bold text-emerald-400')
                    ui.label('Última evaluación 01:41:37 UTC · 12 ms').classes('text-[10px] text-slate-400 font-mono')

            # Advanced queries search row
            with ui.row().classes('w-full gap-3 items-center bg-[#070a0f] p-2 rounded border border-slate-800 mb-3'):
                ui.label('CONSULTAS AVANZADAS').classes('text-[10px] font-bold text-slate-400')
                with ui.row().classes('gap-2 items-center flex-1'):
                    ui.chip('Magnitud ≥ 4.0 Mw', icon='filter_alt').props('color=dark text-color=orange outline').classes('text-[10px]')
                    ui.chip('estado: Pendiente', icon='filter_alt').props('color=dark text-color=cyan outline').classes('text-[10px]')
                    ui.chip('ventana: 24 h', icon='schedule').props('color=dark text-color=slate-300 outline').classes('text-[10px]')
                    ui.chip('zona: Andino', icon='place').props('color=dark text-color=slate-300 outline').classes('text-[10px]')
                ui.button('Ejecutar', icon='play_arrow', on_click=lambda: ui.notify('Query executed successfully')).classes('bg-cyan-950 text-cyan-300 text-xs border border-cyan-800')

            # Three split columns at the bottom
            with ui.row().classes('w-full gap-3 grid grid-cols-1 lg:grid-cols-12'):
                
                # Left: SQL / AVL Query results table (4 cols)
                with ui.column().classes('col-span-4 bg-[#070a0f] p-2.5 rounded border border-slate-800 gap-2'):
                    ui.label('SEARCH AVL WHERE Mc4.0 AND status=PEND AND tc24h').classes('text-[10px] font-mono text-slate-400')
                    
                    # Results table mockup
                    with ui.row().classes('w-full justify-between text-[10px] font-bold text-slate-500 border-b border-slate-800 pb-1'):
                        ui.label('PRIORIDAD / CLAVE')
                        ui.label('ZONA')
                        ui.label('ESTADO')
                        ui.label('COSTO')
                    
                    for p, clave, zona, estado, costo in [('P3', '(6.2, 148)', 'Cordillera', 'Pendiente', '4 pasos'),
                                                        ('P2', '(5.4, 149)', 'Costa', 'Pendiente', '5 pasos'),
                                                        ('P2', '(4.3, 144)', 'Norte', 'Pendiente', '3 pasos'),
                                                        ('P2', '(4.2, 136)', 'Andina', 'Pendiente', '6 pasos')]:
                        with ui.row().classes('w-full justify-between items-center text-[11px] py-0.5'):
                            with ui.row().classes('gap-1 items-center'):
                                ui.badge(p, color='orange' if '3' in p else 'yellow').classes('text-[9px]')
                                ui.label(clave).classes('font-mono text-cyan-400')
                            ui.label(zona).classes('text-slate-400')
                            ui.label(estado).classes('text-orange-400 text-[10px]')
                            ui.label(costo).classes('font-mono text-slate-300')
                    
                    ui.label('4 resultados de 27 · 10 nodos podados').classes('text-[9px] text-slate-500 mt-1')

                # Middle: Cost Auditor (4 cols)
                with ui.column().classes('col-span-4 bg-[#070a0f] p-2.5 rounded border border-slate-800 gap-2'):
                    with ui.row().classes('w-full justify-between items-center'):
                        ui.label('AUDITOR DE COSTO').classes('text-[10px] font-bold text-slate-400')
                        ui.badge('1 ANOMALÍA', color='orange').classes('text-[9px]')
                    
                    with ui.row().classes('w-full justify-between gap-2'):
                        with ui.column().classes('flex-1 bg-[#111827] p-2 rounded border border-slate-800'):
                            ui.label('AVL ACTUAL').classes('text-[9px] text-slate-400')
                            ui.label('h=4  O(log n)').classes('text-xs font-bold text-cyan-400')
                        with ui.column().classes('flex-1 bg-[#111827] p-2 rounded border border-slate-800'):
                            ui.label('EST. REFERENCIA').classes('text-[9px] text-slate-400')
                            ui.label('h=7  O(n)').classes('text-xs font-bold text-slate-400')

                    with ui.column().classes('gap-1.5 w-full'):
                        with ui.row().classes('w-full justify-between items-center text-[10px]'):
                            ui.label('Buscar S-140')
                            ui.label('4 pasos · óptimo').classes('font-mono text-emerald-400')
                        with ui.row().classes('w-full justify-between items-center text-[10px]'):
                            ui.label('Rango Mn4.0')
                            ui.label('6 pasos · aceptable').classes('font-mono text-cyan-400')
                        with ui.row().classes('w-full justify-between items-center text-[10px]'):
                            ui.label('Rama derecha / BST')
                            ui.label('9 pasos · costoso').classes('font-mono text-orange-400')
                    
                    with ui.row().classes('w-full items-center justify-between bg-orange-950/40 p-2 rounded border border-orange-900/50 mt-1'):
                        with ui.row().classes('items-center gap-1'):
                            ui.icon('warning', size='xs').classes('text-orange-400')
                            ui.label('ACCESO COSTOSO: S-130 excede umbral T=8 en comparación EST.').classes('text-[9px] text-orange-300')
                        ui.label('+125%').classes('text-xs font-bold text-orange-400')
                    
                    ui.label('muestra: últimas 64 operaciones · p95=6 pasos · rotaciones=11').classes('text-[9px] text-slate-500')

                # Right: Rollback chronological stack & snapshot rollback (4 cols)
                with ui.column().classes('col-span-4 bg-[#070a0f] p-2.5 rounded border border-slate-800 gap-2'):
                    with ui.row().classes('w-full justify-between items-center'):
                        ui.label('PILA CRONOLÓGICA DE RETROCESO').classes('text-[10px] font-bold text-slate-400')
                        with ui.row().classes('gap-1'):
                            ui.button('Deshacer 1', on_click=lambda: ui.notify('Reverted 1 step')).classes('bg-slate-800 text-slate-200 text-[9px] px-2 py-0.5')
                            ui.button('Restaurar v143', on_click=lambda: ui.notify('Restored snapshot v143')).classes('bg-cyan-950 text-cyan-300 text-[9px] px-2 py-0.5 border border-cyan-800')

                    with ui.column().classes('gap-1 w-full max-h-[110px] overflow-y-auto'):
                        for time_str, action in [('01:41:32', 'ROTACIÓN RL  pivot S-144 · raíz S-148'),
                                                ('01:39:05', 'UPDATE  S-148 prioridad P2 → P3'),
                                                ('01:37:22', 'INSERT  K=(3,6.2,148) · EST-83'),
                                                ('01:32:55', 'ROTACIÓN LL  subárbol S-135 · BF +2'),
                                                ('01:28:49', 'REVISADO  S-141 · operador OP-07')]:
                            with ui.row().classes('w-full justify-between items-center text-[10px] bg-[#111827] px-2 py-1 rounded border border-slate-800'):
                                ui.label(time_str).classes('font-mono text-slate-400')
                                ui.label(action).classes('text-slate-300')

                    with ui.row().classes('w-full justify-between items-center mt-1 pt-1 border-t border-slate-800'):
                        ui.label('stack depth 18 / 64 · persistencia cada 5 uvs').classes('text-[9px] text-slate-500')
                        ui.button('ROLLBACK SEGURO', icon='history', on_click=lambda: ui.notify('Secure rollback executed')).classes('bg-emerald-950 text-emerald-400 text-[10px] border border-emerald-800 px-2 py-1')
main()

ui.run(title='SismoLab AVL', dark=True, favicon='assets/icon.svg')