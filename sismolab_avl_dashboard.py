from nicegui import ui
from src.model import *
from src.app.state import global_state
import datetime as dt

r = Report(1,5.6,98,50,100,"2026-10-06T14:35:20Z","Tolu",1)
a = Report(2,7.9,98,50,100,"2026-10-06T14:35:20Z","Tolu",1)

global_state.insert_report(r)
global_state.insert_report(a)

ui.add_head_html('''
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:opsz,wght@6..144,1..1000&display=swap" rel="stylesheet">
''')
ui.add_css('''
    body {
        background-color: #0c1017;
        color: #94a3b8;
        font-family: "Google Sans Flex", sans-serif;
        font-optical-sizing: auto;
        font-weight: 400;
        font-style: normal;
        font-variation-settings:
            "slnt" 0,
            "wdth" 100,
            "GRAD" 0,
            "ROND" 0;
    }
    .dashboard-card {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 0.5rem;
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

def main():
    with ui.column().classes('w-full min-h-screen bg-[#0b0f17] p-3 text-slate-300 select-none'):
        
        # TOP NAVIGATION & STATUS BAR
        with ui.row().classes('w-full items-center justify-between dashboard-card p-2 px-4 mb-3'):
            with ui.row().classes('items-center gap-4'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('hub', color='cyan').classes('text-2xl')
                    ui.label('SismoLab AVL').classes('text-lg font-bold text-white tracking-wider')
                ui.label('AVL · OBSERVATORIO TELEMÉTRICO').classes('text-xs text-slate-400 border-l border-slate-700 pl-3')
                with ui.row().classes('items-center gap-2 bg-[#172033] px-3 py-1 rounded border border-slate-700'):
                    ui.icon('schedule', size='xs').classes('text-cyan-400')
                    ui.label('UTC SINCRONIZADO').classes('text-[10px] text-cyan-400 font-semibold')
                    clock_label = ui.label('2026-10-02 01:41:09').classes('text-xs font-mono text-white')
            
            # Center time controls & metrics chips
            with ui.row().classes('items-center gap-3'):
                with ui.row().classes('bg-[#131b2e] p-1 rounded border border-slate-800 gap-1'):
                    ui.button('+1h', on_click=lambda: ui.notify('Time advanced +1h')).classes('bg-[#1f2937] text-xs text-slate-200 px-2 py-0.5')
                    ui.button('+24h', on_click=lambda: ui.notify('Time advanced +24h')).classes('bg-[#1f2937] text-xs text-slate-200 px-2 py-0.5')
                with ui.row().classes('items-center gap-3 bg-[#131b2e] px-3 py-1 rounded border border-slate-800'):
                    with ui.row().classes('items-center gap-1'):
                        ui.label('P').classes('text-xs font-bold text-orange-400')
                        ui.badge('2', color='orange').classes('text-xs')
                    with ui.row().classes('items-center gap-1'):
                        ui.label('R').classes('text-xs font-bold text-cyan-400')
                        ui.badge('6', color='cyan').classes('text-xs')
                    with ui.row().classes('items-center gap-1'):
                        ui.label('L').classes('text-xs font-bold text-slate-400')
                        ui.badge('0', color='grey').classes('text-xs')
                    with ui.row().classes('items-center gap-1'):
                        ui.label('T').classes('text-xs font-bold text-emerald-400')
                        ui.label('18m').classes('text-xs font-mono text-emerald-400')
                
                with ui.row().classes('gap-1'):
                    ui.button('Normal', on_click=lambda: ui.notify('Mode: Normal')).classes('bg-emerald-900/50 text-emerald-400 text-xs border border-emerald-600')
                    ui.button('Estrés', on_click=lambda: ui.notify('Stress test simulated')).classes('bg-orange-900/50 text-orange-400 text-xs border border-orange-600 font-bold')
                    ui.button(icon='undo', on_click=lambda: ui.notify('Undo')).classes('bg-slate-800 text-slate-300 text-xs')
                    ui.button(icon='redo', on_click=lambda: ui.notify('Redo')).classes('bg-slate-800 text-slate-300 text-xs')
                    
                ui.chip('AVL ÍNTEGRO', icon='check_circle').props('color=teal text-color=white outline').classes('text-xs')

            # User profile / ID
            with ui.row().classes('items-center gap-2'):
                with ui.column().classes('items-end'):
                    ui.label('GP-07 / L. ÁLVAREZ').classes('text-xs font-bold text-white')
                    ui.label('AUT-OF2A · 146 operaciones').classes('text-[10px] text-slate-400')
                ui.avatar('LA', color='cyan', text_color='black').classes('text-xs font-bold')

        with ui.row().classes('w-full gap-3 grid grid-cols-1 lg:grid-cols-12 mb-3'):
            
            # 1. CARTESIAN MAP PREVIEW (Left Top - 3 cols)
            with ui.column().classes('dashboard-card p-3 col-span-3'):
                with ui.row().classes('w-full justify-between items-center mb-2'):
                    with ui.row().classes('items-center gap-1'):
                        ui.icon('map', size='xs').classes('text-cyan-400')
                        ui.label('GEOESPACIO').classes('text-xs font-bold text-cyan-400 tracking-wider')
                    ui.label('1000 x 1000 km').classes('text-[10px] text-slate-500 font-mono')
                
                ui.label('Mapa cartesiano').classes('text-sm font-bold text-white mb-1')
                
                global_map = ui.leaflet(
                    center=(0,0),
                    zoom=1,
                    options={
                        'maxBounds': [[-85.051129, -170], [85.051129, 190]],
                        'maxBoundsViscosity': 1.0,
                        'minZoom':1
                    }
                ).classes('w-full')
                
                with ui.row().classes('w-full justify-between items-center mt-2 text-[10px] text-slate-400'):
                    with ui.row().classes('items-center gap-2'):
                        ui.badge('Alta > 5.5', color='red').classes('text-[9px]')
                        ui.badge('Media', color='orange').classes('text-[9px]')
                        ui.badge('Baja', color='blue').classes('text-[9px]')
                    ui.label('37 activos').classes('font-mono text-slate-400')

            # 2. AVL TREE VISUALIZATION (Center Top - 6 cols)
            with ui.column().classes('dashboard-card p-3 col-span-6 flex flex-col h-[340px]'):
                with ui.row().classes('w-full justify-between items-center mb-1'):
                    with ui.row().classes('items-center gap-1'):
                        ui.icon('account_tree', size='xs').classes('text-cyan-400')
                        ui.label('ESTRUCTURA ACTIVA').classes('text-xs font-bold text-cyan-400 tracking-wider')
                    ui.label('27 nodos · versión v16R').classes('text-[10px] text-slate-400 font-mono')
                
                with ui.row().classes('w-full justify-between items-center mb-2'):
                    ui.label('Árbol AVL de eventos').classes('text-sm font-bold text-white')
                    with ui.row().classes('items-center gap-2'):
                        ui.badge('AVL ACTIVO', color='teal').classes('text-[10px]')
                        ui.badge('BST SIN BALANCEAR', color='grey').classes('text-[10px]')
                        ui.badge('IN-ORDER', color='dark').classes('text-[10px] border border-slate-700')
                        ui.badge('ESTRÉS SIMULADO', color='orange').classes('text-[10px]')
                
                # Interactive SVG AVL Diagram
                with ui.card().classes('w-full flex-1 bg-[#ffffff] p-0 relative overflow-hidden border border-slate-800 flex items-center justify-center'):
                    ui.echart(global_state.get_AVL_JSON())

            # 3. CONTROL / OPERATIONS & QUEUE PANEL (Right Top - 3 cols)
            with ui.column().classes('dashboard-card p-3 col-span-3 flex flex-col h-[340px]'):
                with ui.row().classes('w-full justify-between items-center mb-1'):
                    with ui.row().classes('items-center gap-1'):
                        ui.icon('tune', size='xs').classes('text-cyan-400')
                        ui.label('CONTROL').classes('text-xs font-bold text-cyan-400 tracking-wider')
                    ui.label('OP-149').classes('text-[10px] text-slate-500 font-mono')
                
                ui.label('Operaciones y cola').classes('text-sm font-bold text-white mb-2')
                
                # Tab navigation simulation
                with ui.row().classes('w-full bg-[#0a0e14] p-1 rounded border border-slate-800 justify-between items-center mb-2'):
                    ui.button('CRUD', on_click=lambda: ui.notify('CRUD Mode active')).classes('bg-[#1f2937] text-white text-[10px] px-3 py-1')
                    ui.button('COLA FIFO', on_click=lambda: ui.notify('Queue selected')).classes('bg-transparent text-slate-400 text-[10px] px-3 py-1')
                    ui.button('SNAPSHOTS JSON', on_click=lambda: ui.notify('Snapshots loaded')).classes('bg-transparent text-slate-400 text-[10px] px-3 py-1')
                
                # Form inputs
                with ui.row().classes('w-full gap-2 mb-1'):
                    ui.input('ID', value='S-149').classes('w-1/3 text-xs')
                    ui.input('MAGNITUD', value='5.4').classes('w-1/3 text-xs')
                    ui.input('PROF.', value='23.7').classes('w-1/3 text-xs')
                
                with ui.row().classes('w-full gap-2 mb-2'):
                    ui.select(['2 - Media', '1 - Alta', '3 - Baja'], value='2 - Media', label='PRIORIDAD P').classes('w-1/2 text-xs')
                    ui.select(['Z-02 Costa', 'Z-01 Norte', 'Z-04 Cordillera'], value='Z-02 Costa', label='ZONA').classes('w-1/2 text-xs')
                
                with ui.row().classes('w-full justify-between items-center mb-2'):
                    ui.input('ESTACIÓN', value='EST-03').classes('w-1/2 text-xs')
                    ui.input('UTC', value='01:42:16').classes('w-1/2 text-xs')
                
                with ui.row().classes('w-full justify-between items-center bg-[#070a0f] p-2 rounded border border-slate-800 mb-2'):
                    ui.label('CLAVE CALCULADA').classes('text-[10px] text-slate-400')
                    ui.label('K=(2,5.4,149)').classes('text-xs font-mono font-bold text-cyan-400')
                
                # Action Buttons
                with ui.column().classes('w-full gap-1'):
                    ui.button('Insertar en AVL', icon='add_circle', on_click=lambda: ui.notify('Node inserted into AVL tree')).classes('w-full bg-cyan-950 text-cyan-300 text-xs border border-cyan-800 py-1')
                    with ui.row().classes('w-full gap-1'):
                        ui.button('Corregir (r+1)', icon='build', on_click=lambda: ui.notify('Tree balance corrected')).classes('flex-1 bg-slate-800 text-slate-200 text-[10px]')
                        ui.button('Marcar Revisado', icon='done', on_click=lambda: ui.notify('Status updated to Reviewed')).classes('flex-1 bg-slate-800 text-slate-200 text-[10px]')
                    with ui.row().classes('w-full gap-1'):
                        ui.button('Eliminar Individual', icon='delete', on_click=lambda: ui.notify('Node deleted')).classes('flex-1 bg-red-950 text-red-400 text-[10px] border border-red-900')
                        ui.button('Archivar Rama', icon='archive', on_click=lambda: ui.notify('Branch archived')).classes('flex-1 bg-slate-800 text-slate-200 text-[10px]')

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

ui.run(title='SismoLab AVL', dark=True)