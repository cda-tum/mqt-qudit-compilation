
import networkx as nx



class level_Graph(nx.Graph):

    def __init__(self,  edges, nodes_from, data=None, val=None, **attr):
        super(level_Graph, self).__init__()
        self.add_nodes_from(nodes_from)
        self.add_edges_from(edges)


    def distance_nodes(self, source, target):
        path = nx.shortest_path(self, source, target)
        return len(path)-1

    def distance_nodes_in_pi_pulses(self, source, target):

        path = nx.shortest_path(self, source, target)
        negs = 0
        pos = 0
        for n in path:
            if(n >= 0):
                pos += 1
            else:
                negs += 1
        pulses = (2*negs)-1+(pos)-1

        return pulses



    def define__states(self, list_Sp_nodes, list_Sm_nodes, list_D_nodes):
        #TODO TO REFACTOR FOR SUPPORTING DIFFERENT QUANTUM NUMBERS IN THE FUTURE

        Sp_dictionary = dict.fromkeys(list_Sp_nodes, "Sp")
        Sm_dictionary = dict.fromkeys(list_Sm_nodes, "Sm")
        D_dictionary = dict.fromkeys(list_D_nodes, "D")

        for n in list_Sp_nodes:
            nx.set_node_attributes(self, Sp_dictionary, name='level')

        for n in list_Sm_nodes:
            nx.set_node_attributes(self, Sm_dictionary, name='level')

        for n in list_D_nodes:
            nx.set_node_attributes(self, D_dictionary, name='level')




    def update_list(self, lst_, num_a, num_b):
        new_lst = []

        mod_index = []
        for i, t in enumerate(lst_):

            tupla = [0, 0]
            if (t[0] == num_a):
                tupla[0] = 1
            elif (t[0] == num_b):
                tupla[0] = 2

            if (t[1] == num_a):
                tupla[1] = 1
            elif (t[1] == num_b):
                tupla[1] = 2

            mod_index.append(tupla)

        for i, t in enumerate(lst_):
            substituter = list(t)

            if (mod_index[i][0] == 1):
                substituter[0] = num_b
            elif (mod_index[i][0] == 2):
                substituter[0] = num_a

            if (mod_index[i][1] == 1):
                substituter[1] = num_b
            elif (mod_index[i][1] == 2):
                substituter[1] = num_a

            new_lst.append(tuple(substituter))

        return new_lst


    def swap_nodes(self, node_a, node_b):

        edges = list(self.edges)
        nodes = list(self.nodes)

        attribute_list = []
        for e in edges:
            attribute_list.append(self.get_edge_data(*e))

        swapped_nodes_edges = self.update_list(edges, node_a, node_b)

        new_edge_list = []
        for i, e in enumerate(swapped_nodes_edges):
            new_edge_list.append((*e, attribute_list[i]))

        level_a = self.nodes[node_a]["level"]
        level_b = self.nodes[node_b]["level"]
        self.nodes[node_a]["level"] = level_b
        self.nodes[node_b]["level"] = level_a

        return level_Graph(new_edge_list, len(nodes))



    def get_sensitivity_cost(self, node_a, node_b):
        path = nx.shortest_path(self, source = node_a, target = node_b)

        totalsensibility = 0
        for i in range(len(path)-1):
            totalsensibility += self[path[i]][path[i+1]]["sensitivity"]

        return totalsensibility

    def get_edge_sensitivity(self, node_a, node_b):
        return self[node_a][node_b]["sensitivity"]

    @property
    def Sp(self):
        Sp_node = [x for x, y in self.nodes(data=True) if y['level'] == "Sp"]
        return Sp_node
    @property
    def Sm(self):
        Sm_node = [x for x, y in self.nodes(data=True) if y['level'] == "Sm"]
        return Sm_node

    def is_Sp(self, node):
        sp_nodes = self.Sp
        return (node in sp_nodes)

    def is_Sm(self, node):
        sm_nodes = self.Sm
        return (node in sm_nodes)

    def get_bookmark(self, lev_a, lev_b):
        #TODO APPLY ROUTINE TO CALCULATE MOST EFFECTIVE BOOKMARK
        if (lev_a in self.Sp and lev_b in self.Sm):
            return lev_b
        elif (lev_a not in self.Sp and lev_b in self.Sm):
            return self.Sp
        elif (lev_a  in self.Sp and lev_b  not in self.Sm):
            return self.Sm
        elif (lev_a not in self.Sp and lev_b not in self.Sm):
            #COSTS LESS IN THEORY
            return self.Sm