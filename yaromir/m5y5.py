class TreeNode:
    def __init__(self, name):
        self.name = name         
        self.children = []       

    def add_child(self, child_node):
        self.children.append(child_node)

    def print_tree(self, level=0):
        indent = "  " * level 
        
        print(indent + "- " + self.name)
        
        for child in self.children:
            child.print_tree(level + 1)


root = TreeNode("Компьютер")


folder_games = TreeNode("Игры")
folder_docs = TreeNode("Документы")

root.add_child(folder_games)
root.add_child(folder_docs)


game_minecraft = TreeNode("Minecraft")
game_stardew = TreeNode("Stardew Valley")
folder_games.add_child(game_minecraft)
folder_games.add_child(game_stardew)


print("Структура папок:")
root.print_tree()