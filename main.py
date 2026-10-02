from nicegui import ui
from src.model import *
from src.app.state import global_state
import datetime as dt

r = Report(1,5.6,98,50,100,"2026-10-06T14:35:20Z","Tolu",1)
global_state.insert_report(r)

print(global_state.get_AVL_JSON())

ui.echart(global_state.get_AVL_JSON())

ui.run()