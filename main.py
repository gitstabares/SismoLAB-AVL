from pydoc import text

import streamlit as st
import src.model as m

tree = m.Tree()
for i in range(6,0,-1):
    tree.add_node(i)
print(tree.get_node(5))