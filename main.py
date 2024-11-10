import tkinter as tk
from tkinter import messagebox, ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ArticulationPointAppDFS:
    def __init__(self, root):
        self.root = root
        self.root.title("Recherche des points d'articulation (DFS)")
        self.root.geometry("800x700+200+100")  # Fenêtre plus grande
        self.root.configure(bg="#E2F1E7")  # Beige clair
        self.root.resizable(True, True)
        # Initialiser les données du graphe
        self.graph = nx.Graph()
        self.num_vertices = tk.IntVar()
        self.u = tk.IntVar()
        self.v = tk.IntVar()
        
        # Configurer l'interface utilisateur
        self.create_widgets()
    
    def create_widgets(self):
        # Label du titre
        title_label = tk.Label(self.root, text="Points d'articulation : 0", fg="blue", font=("Arial", 14), bg="#E2F1E7")
        title_label.pack(pady=10)
        self.title_label = title_label
        
        # Nombre de sommets
        frame_vertices = tk.Frame(self.root, bg="#E2F1E7")
        frame_vertices.pack(pady=5)
        
        tk.Label(frame_vertices, text="Nombre de sommets :", font=("Arial", 12), bg="#E2F1E7").pack(side=tk.LEFT, padx=5)
        vertices_entry = tk.Entry(frame_vertices, textvariable=self.num_vertices, width=5)
        vertices_entry.pack(side=tk.LEFT, padx=5)
        
        create_graph_btn = tk.Button(frame_vertices, text="Créer le graphe", command=self.create_graph, fg="white",bg="#629584")
        create_graph_btn.pack(side=tk.LEFT, padx=5)
        
        # Liste des arêtes
        self.edge_listbox = tk.Listbox(self.root, width=40, height=10)
        self.edge_listbox.pack(pady=5)
        
        # Section Ajouter une arête
        frame_edges = tk.Frame(self.root, bg="#E2F1E7")
        frame_edges.pack(pady=5)
        
        tk.Label(frame_edges, text="Ajouter une arête (u, v) :", font=("Arial", 12), bg="#E2F1E7").pack(side=tk.LEFT, padx=5)
        tk.Entry(frame_edges, textvariable=self.u, width=5).pack(side=tk.LEFT, padx=2)
        tk.Entry(frame_edges, textvariable=self.v, width=5).pack(side=tk.LEFT, padx=2)
        add_edge_btn = tk.Button(frame_edges, text="Ajouter",fg="white", command=self.add_edge, bg="#629584")
        add_edge_btn.pack(side=tk.LEFT, padx=5)
        
        # Bouton Calculer les points d'articulation
        calculate_btn = tk.Button(self.root, text="Calculer les points d'articulation", command=self.calculate_articulation_points, bg="#243642", fg="white", font=("Arial", 12))
        calculate_btn.pack(pady=10)
        
        # Ajouter le canvas pour afficher le graphe avec un conteneur scrollable
        self.graph_canvas_frame = tk.Frame(self.root, bg="#E2F1E7")
        self.graph_canvas_frame.pack(pady=10, expand=True, fill=tk.BOTH)

        self.canvas_container = tk.Canvas(self.graph_canvas_frame, bg="white")
        self.canvas_container.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        self.scrollbar = tk.Scrollbar(self.graph_canvas_frame, orient=tk.VERTICAL, command=self.canvas_container.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas_container.config(yscrollcommand=self.scrollbar.set)
        
        self.inner_frame = tk.Frame(self.canvas_container, bg="white")
        self.canvas_container.create_window((0, 0), window=self.inner_frame, anchor='nw')
        self.inner_frame.bind("<Configure>", lambda e: self.canvas_container.config(scrollregion=self.canvas_container.bbox("all")))
    
    def create_graph(self):
        self.graph.clear()
        n = self.num_vertices.get()
        
        # Ajouter les nœuds au graphe
        self.graph.add_nodes_from(range(n))
        self.edge_listbox.delete(0, tk.END)
        self.title_label.config(text="Points d'articulation : 0")
        self.show_temporary_message("Graphe créé avec {} sommets.".format(n))
        
        # Afficher le graphe
        self.draw_graph()
    
    def add_edge(self):
        u, v = self.u.get(), self.v.get()
        
        if u >= self.num_vertices.get() or v >= self.num_vertices.get() or u == v:
            self.show_temporary_message("Arête invalide. Vérifiez les sommets.", duration=4000)
            return
        
        self.graph.add_edge(u, v)
        self.edge_listbox.insert(tk.END, f"Arête ajoutée entre {u} et {v}")
        self.show_temporary_message("Arête ajoutée entre {} et {}.".format(u, v))
        
        # Afficher le graphe
        self.draw_graph()
    
    def calculate_articulation_points(self):
        if not nx.is_connected(self.graph):
            self.show_temporary_message("Le graphe est déconnecté ; pas de points d'articulation.", duration=4000)
            self.title_label.config(text="Points d'articulation : N/A")
            return
        
        # Trouver les points d'articulation en utilisant DFS
        articulation_points = self.find_articulation_points()
        self.title_label.config(text=f"Points d'articulation : {articulation_points}")
        self.show_temporary_message("Points d'articulation calculés.")
        
        # Afficher le graphe
        self.draw_graph()
    
    def find_articulation_points(self):
        self.time = 0
        self.articulation_points = set()
        self.visited = [False] * len(self.graph.nodes)
        self.disc = [-1] * len(self.graph.nodes)
        self.low = [-1] * len(self.graph.nodes)
        self.parent = [-1] * len(self.graph.nodes)
        
        for u in self.graph.nodes:
            if not self.visited[u]:
                self.dfs(u)
        
        return list(self.articulation_points)
    
    def dfs(self, u):
        children = 0
        self.visited[u] = True
        self.disc[u] = self.low[u] = self.time
        self.time += 1
        
        for v in self.graph.neighbors(u):
            if not self.visited[v]:
                children += 1
                self.parent[v] = u
                self.dfs(v)
                self.low[u] = min(self.low[u], self.low[v])
                
                if self.parent[u] == -1 and children > 1:
                    self.articulation_points.add(u)
                elif self.parent[u] != -1 and self.low[v] >= self.disc[u]:
                    self.articulation_points.add(u)
            elif v != self.parent[u]:
                self.low[u] = min(self.low[u], self.disc[v])
    
    def draw_graph(self):
        fig, ax = plt.subplots(figsize=(6, 6))
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, ax=ax, with_labels=True, node_color="skyblue",
                node_size=2000, font_size=12, font_weight="bold", edge_color="gray")
        ax.margins(0.2)  # Ajouter un padding autour du graphe
        
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        
        canvas = FigureCanvasTkAgg(fig, master=self.inner_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)

    def show_temporary_message(self, message, duration=3000):
        message_label = tk.Label(self.root, text=message, bg="lightgreen", font=("Arial", 10))
        message_label.pack(pady=5)
        
        def remove_message():
            message_label.destroy()
        
        self.root.after(duration, remove_message)

def run_app():
    root = tk.Tk()
    app = ArticulationPointAppDFS(root)
    root.mainloop()

# Lancer l'application
run_app()
