from src.model import Scenario
from src.model import Report
from nicegui import ui

reports = [
    Report(1001, 4.5, 15.0, 120.5, 340.2, "2026-10-01T08:30:00", "Station-Alpha", True, 1),
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
for r in reports:
    global_state.insert_report(r)
ui.echart(global_state.get_AVL_JSON())
ui.run()