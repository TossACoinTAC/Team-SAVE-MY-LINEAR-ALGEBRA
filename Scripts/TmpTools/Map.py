import pygame
from Statics import *
import random

class MapTree:
    def __init__(self, id, value):
        self.value = value
        self.id  = id
        self.left = None
        self.right = None
        self.father = None

RoomTree = []  #记录房间关系

scene_choices = ["COMMON_ROOM","SHOP","TREASURE","SECRET","BLUEWOMB","CATACOMB"]
root = "START_ROOM"
    

def add_children(node, depth, shop_added, treasure_added, catacomb_added):
    if depth == 4:
        RoomTree.append(node)
        return

    choices = scene_choices.copy()
    if shop_added:
        choices.remove("SHOP")
    if treasure_added:
        choices.remove("TREASURE")
    if catacomb_added:
        choices.remove("CATACOMB")

    if choices:
        node.left = MapTree(node.id * 2, random.choice(choices))
        node.left.father = node
        node.right = MapTree(node.id * 2 + 1, random.choice(choices))
        node.right.father = node
        RoomTree.append(node)

    if node.left:
        add_children(node.left, depth + 1, node.left in ["SHOP"], node.left in ["TREASURE"], node.left in ["CATACOMB"])
    if node.right:
        add_children(node.right, depth + 1, node.right in ["SHOP"], node.right in ["TREASURE"], node.right in ["CATACOMB"])

root_node = MapTree(1, root)
add_children(root_node, 1, False, False, False)