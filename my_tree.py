#!/usr/bin/python3



class NodeNotFoundException(Exception):
	def __init__(self, value):
		self.value = value
	
	def __str__(self):
		return repr(self.value)


class Node:
	def __init__(self, key, rotation, U_of_level, current_cost, max_cost, parent_key, children=None):
		self.key = key
		self.children = []
		self.rotation = rotation
		self.U_of_level = U_of_level
		self.finished = False
		self.current_cost = current_cost
		self.max_cost = max_cost
		self.size =  0
		self.parent_key = parent_key


	def add(self, new_key, rotation, U_of_level, current_cost, max_cost):
		new_node = Node(new_key, rotation, U_of_level, current_cost, max_cost, self.key)

		self.children.append(new_node)
		self.size += 1
	
	def __str__(self):
		return str(self.key)

class N_ary_Tree:

	def __init__(self):
		self.root = None
		self.size = 0

	def find_node(self, node, key):
		if node == None or node.key == key:
			return node		
		for child in node.children:
			return_node = self.find_node(child, key)
			if return_node: 
				return return_node
		return None	


	def depth(self, key):
		node = self.find_node(self.root, key)
		if not(node):
			raise NodeNotFoundException('No element was found with the informed parent key.')
		return self.max_depth(node)

	def max_depth(self, node):
		if not(node.children):
			return 0
		children_max_depth = []
		for child in node.children:
			children_max_depth.append(self.max_depth(child))
		return 1 + max(children_max_depth)

	def add(self, new_key, rotation, U_of_level, current_cost, max_cost, parent_key=None):
		new_node = Node(new_key, rotation, U_of_level, current_cost, max_cost, parent_key)

		if parent_key == None:
			self.root = new_node
			self.size = 1
		else:
			parent_node = self.find_node(self.root, parent_key)
			if not(parent_node):
				raise NodeNotFoundException('No element was found with the informed parent key.')
			parent_node.children.append(new_node)
			self.size += 1
	
	def print_tree(self, node, str_aux):

		if node == None: return "holahola"
		f = ""
		if(node.finished):
			f = "f"
		str_aux += str(node) +f+ "("
		for i in range(len(node.children)):

			child = node.children[i]
			end = ',' if i < len(node.children) - 1 else ''
			str_aux = self.print_tree(child, str_aux) + end
			
		str_aux += ')'
		return str_aux


	def found_checker(self, node):
		if not(node.children):
			return node.finished

		children_checking = []
		for child in node.children:
			children_checking.append(self.found_checker(child))
		if(True in children_checking ):
			node.finished = True

		return node.finished

	def min_cost_decomp(self, node):
		if ( not(node.children) ) :
			return [node], node.current_cost
		else:
			children_cost = []

			for child in node.children:
				if(child.finished):
					children_cost.append( self.min_cost_decomp(child) )


			minimum_child, best_cost = min(children_cost, key=lambda t: t[1])
			minimum_child.insert(0, node)
			return minimum_child, best_cost

	def retrieve_decomposition(self, node):
		self.found_checker(node)

		if( not node.finished):
			decomp =  []
			from numpy import inf
			best_cost = inf
		else:
			decomp, best_cost = self.min_cost_decomp(node)

		return decomp, best_cost


	def is_empty(self):
		return self.size == 0

	def lenght(self):
		return self.size

	def __str__(self):
		return self.print_tree(self.root, "")



