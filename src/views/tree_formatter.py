def get_echart_dict(tree):
    def __get_data(node):
        if not node:
            return {
                        "name": "", 
                        "itemStyle": {"opacity": 0}, # Oculta el círculo
                        "lineStyle": {"opacity": 0}, # Oculta la arista que lo une al padre
                        "label": {"show": False},    # Oculta el texto
                        "tooltip": {"show": False}   # Evita que el usuario interactúe con él
                    }
        return {
                    'name':str(node),
                    'children':[__get_data(node.get_left()),__get_data(node.get_right())]
                }
    return {
            "tooltip": {
                "trigger": "item",
                "triggerOn": "mousemove"
            },
            "series": [
                {
                    "type": "tree",
                    "data": [__get_data(tree.get_root())],
                    "orient": "TB",          # Top to Bottom (Descendente)
                    "roam": True,            # Habilita el zoom con trackpad y arrastre libre
                    "symbolSize": 40,        # Tamaño de los nodos
                    "initialTreeDepth": -1,  # -1 para que todo el árbol inicie expandido
                    "label": {
                        "position": "inside",
                        "verticalAlign": "middle",
                        "align": "center",
                        "color": "black",    # Letra blanca para contrastar con el nodo
                        "fontSize": 14
                    },
                    "symbol": "circle",
                    "itemStyle": {
                        "color": "#3b82f6",  # Color del nodo (azul)
                        "borderColor": "#1d4ed8"
                    },
                    "lineStyle": {
                        "color": "#ccc",     # Color de las aristas
                        "width": 2,
                        "curveness": 0.5     # 0 para líneas rectas, >0 para curvas suaves
                    },
                    # Márgenes para que no se corte al hacer zoom inicial
                    "top": "10%",
                    "bottom": "10%",
                    "left": "10%",
                    "right": "10%"
                }
            ]
        }