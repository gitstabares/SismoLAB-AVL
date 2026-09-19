from nicegui import ui
from src.model import *
from src.views import get_echart_dict

tree = Tree()
for i in range(6,0,-1):
    tree.add_node(i)
ui.label('Grafo')
tree.balance_tree()
echarts = get_echart_dict(tree)
ui.echart(echarts).classes('w-full h-screen')
ui.run(dark=True, language='es')