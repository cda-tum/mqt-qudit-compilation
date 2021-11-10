
import networkx as nx
import copy


class level_Graph(nx.Graph):

    def __init__(self,  edges, nodes, nodes_physical_mapping=None, initialization_nodes=None):
        super(level_Graph, self).__init__()


        self.logic_nodes = nodes
        self.add_nodes_from(self.logic_nodes)


        if(nodes_physical_mapping):
            self.logic_physical_map(nodes_physical_mapping)


        self.add_edges_from(edges)

        if( initialization_nodes ):

            inreach_nodes = [x for x in nodes if x not in initialization_nodes]
            self.define__states(initialization_nodes, inreach_nodes)





    def distance_nodes(self, source, target):
        path = nx.shortest_path(self, source, target)
        return len(path)-1



    def distance_nodes_pi_pulses_fixed_ancilla(self, source, target):

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



    def logic_physical_map(self, physical_nodes):

        logic_phy_map = { nl:np for nl, np in zip(self.logic_nodes, physical_nodes)}
        nx.set_node_attributes(self, logic_phy_map, 'lpmap')



    def define__states(self, initialization_nodes, inreach_nodes):

        inreach_dictionary = dict.fromkeys(inreach_nodes, "r")
        initialization_dictionary = dict.fromkeys(initialization_nodes, "i")

        for n in inreach_dictionary:
            nx.set_node_attributes(self, inreach_dictionary, name='level')

        for n in initialization_dictionary:
            nx.set_node_attributes(self, initialization_dictionary, name='level')





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

    def deep_copy_func(self, l_n):
        cpy_list = []
        for li in l_n:
            d2 = copy.deepcopy(li)
            cpy_list.append(d2)

        return cpy_list
    def index(self, l, node):

        for i in range(len(l)):
            if(l[i][0]== node):
                return i
        return  None

    def swap_node_attributes(self, node_a, node_b):
        # TODO REMOVE HARDCODING
        nodelistcopy = self.deep_copy_func(list(self.nodes(data=True)))
        node_a = self.index(nodelistcopy, node_a)
        node_b = self.index(nodelistcopy, node_b)

        level_a = nodelistcopy[node_a][1]["level"]
        level_b = nodelistcopy[node_b][1]["level"]
        nodelistcopy[node_a][1]["level"] = level_b
        nodelistcopy[node_b][1]["level"] = level_a

        lp_a = nodelistcopy[node_a][1]["lpmap"]
        lp_b = nodelistcopy[node_b][1]["lpmap"]
        nodelistcopy[node_a][1]["lpmap"] = lp_b
        nodelistcopy[node_b][1]["lpmap"] = lp_a



        return nodelistcopy


    def swap_nodes(self, node_a, node_b):

        nodes = self.swap_node_attributes(node_a, node_b)

        #------------------------------------------------
        new_Graph = level_Graph([], nodes)

        edges = self.deep_copy_func( list(self.edges) )

        attribute_list = []
        for e in edges:
            attribute_list.append(self.get_edge_data(*e).copy())

        swapped_nodes_edges = self.update_list(edges, node_a, node_b)

        new_edge_list = []
        for i, e in enumerate(swapped_nodes_edges):
            new_edge_list.append((*e, attribute_list[i]))

        new_Graph.add_edges_from(new_edge_list)

        return new_Graph



    def get_node_sensitivity_cost(self, node):
        neighbs = [n for n in self.neighbors(node)]

        totalsensibility = 0
        for i in range(len(neighbs)-1):
            totalsensibility += self[node][neighbs[i]]["sensitivity"]

        return totalsensibility




    def get_edge_sensitivity(self, node_a, node_b):
        #todo add try catch in case not there
        return self[node_a][node_b]["sensitivity"]




    @property
    def _1stRnode(self):
        r_node = [x for x, y in self.nodes(data=True) if y['level'] == "r"]
        return r_node[0]
    @property
    def _1stInode(self):
        Inode = [x for x, y in self.nodes(data=True) if y['level'] == "i"]
        return Inode[0]

    def is_irnode(self, node):
        irnodes = [x for x, y in self.nodes(data=True) if y['level'] == "r"]
        r = (node in irnodes)
        return r

    def is_Inode(self, node):
        Inodes = [x for x, y in self.nodes(data=True) if y['level'] == "i"]
        r = (node in Inodes)
        return r

    @property
    def lpmap(self):
        nodes = self.nodes
        listret = []

        for key in nodes:
            for N in self.nodes(data=True):
                if(N[0]==key):

                    listret.append(N[1]["lpmap"])
        return  listret


    """
    def get_bookmark(self, lev_a, lev_b):

        #TODO APPLY ROUTINE TO CALCULATE MOST EFFECTIVE BOOKMARK

        if (lev_a in self._1stRnode and lev_b in self._1stInode):
            return lev_b
        elif (lev_a not in self._1stRnode and lev_b in self._1stInode):
            return self._1stRnode
        elif (lev_a  in self._1stRnode and lev_b  not in self._1stInode):
            return self._1stInode
        elif (lev_a not in self._1stRnode and lev_b not in self._1stInode):
            #COSTS LESS IN THEORY
            return self._1stInode
    """



    def __str__(self):
        description = str(self.nodes(data=True))+ "\n"+ str(self.edges(data=True))

        return description