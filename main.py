from pydoc import text

import streamlit as st
import src.model as m

root = m.Node(6)
root.add_nodes([5,4,3,2,1])
st.title('Arbol sin balancear',text_alignment='center')
st.graphviz_chart(root.get_tree_graph())
root.balance_tree()
st.title('Arbol balanceado',text_alignment='center')
st.graphviz_chart(root.get_tree_graph())