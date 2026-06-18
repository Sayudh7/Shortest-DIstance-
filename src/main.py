import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import networkx as nx
import contextily as ctx
from graph import cities, roads
from dijkstra import build_graph, dijkstra


def lon_lat_to_mercator(lon, lat):
    """Convert GPS coordinates to Web Mercator (EPSG:3857) for map display."""
    x = lon * 20037508.34 / 180
    y = math.log(math.tan((90 + lat) * math.pi / 360)) / (math.pi / 180)
    y = y * 20037508.34 / 180
    return x, y


# --- Convert all city GPS coords to mercator for plotting ---
pos = {city: lon_lat_to_mercator(*cities[city]) for city in cities}

# --- Build graph ---
graph = build_graph(cities, roads)
G = nx.Graph()
for city in cities:
    G.add_node(city)
for (city_a, city_b, distance) in roads:
    G.add_edge(city_a, city_b, weight=distance)

# --- Global state ---
selected        = []
distance_result = [0]
current_path    = [[]]


def draw(path=[], source=None, destination=None):
    plt.clf()
    ax = plt.gca()

    # --- Categorize edges ---
    path_edges   = []
    normal_edges = []
    for (city_a, city_b, _) in roads:
        if path and city_a in path and city_b in path:
            idx_a = path.index(city_a)
            idx_b = path.index(city_b)
            if abs(idx_a - idx_b) == 1:
                path_edges.append((city_a, city_b))
            else:
                normal_edges.append((city_a, city_b))
        else:
            normal_edges.append((city_a, city_b))

    # --- Categorize nodes ---
    if source and destination and path:
        start_end_nodes = [source, destination]
        middle_nodes    = [c for c in path if c not in start_end_nodes]
        other_nodes     = [c for c in cities if c not in path]
    elif source:
        start_end_nodes = [source]
        middle_nodes    = []
        other_nodes     = [c for c in cities if c != source]
    else:
        start_end_nodes = []
        middle_nodes    = []
        other_nodes     = list(cities.keys())

    # --- Draw edges ---
    nx.draw_networkx_edges(G, pos, edgelist=normal_edges,
        edge_color="#FFFFFF", width=1.5, alpha=0.6, ax=ax)

    nx.draw_networkx_edges(G, pos, edgelist=path_edges,
        edge_color="#00FF88", width=5.0, alpha=0.9, ax=ax)

    # --- Draw nodes ---
    nx.draw_networkx_nodes(G, pos, nodelist=other_nodes,
        node_color="#3A3A3A", node_size=500,
        edgecolors="white", linewidths=1.2, ax=ax)

    nx.draw_networkx_nodes(G, pos, nodelist=middle_nodes,
        node_color="#378ADD", node_size=600,
        edgecolors="white", linewidths=1.5, ax=ax)

    nx.draw_networkx_nodes(G, pos, nodelist=start_end_nodes,
        node_color="#E85D24", node_size=700,
        edgecolors="white", linewidths=2.0, ax=ax)

    # --- City name labels ---
    label_pos = {city: (x, y + 18000) for city, (x, y) in pos.items()}
    nx.draw_networkx_labels(G, label_pos,
        font_size=7, font_color="white", font_weight="bold", ax=ax)

    # --- Edge distance labels ---
    edge_labels = {(a, b): f"{d}km" for (a, b, d) in roads}
    nx.draw_networkx_edge_labels(G, pos,
        edge_labels=edge_labels,
        font_size=5.5,
        font_color="yellow",
        bbox=dict(boxstyle="round,pad=0.15", fc="black", alpha=0.3),
        ax=ax)

    # --- Real Nepal map background ---
    try:
        ctx.add_basemap(ax,
            crs="EPSG:3857",
            source=ctx.providers.CartoDB.DarkMatter,
            zoom=7)
    except Exception:
        ax.set_facecolor("#1A1A2E")

    # --- Title ---
    if not source:
        plt.title("🗺  Nepal Shortest Path Finder  |  Click a city to select SOURCE",
            fontsize=12, pad=12, color="white",
            bbox=dict(facecolor="#1A1A2E", alpha=0.8, edgecolor="none"))

    elif source and not destination:
        plt.title(f"✅ Source: {source}  |  Now click DESTINATION city",
            fontsize=12, pad=12, color="white",
            bbox=dict(facecolor="#1A1A2E", alpha=0.8, edgecolor="none"))

    elif source and destination and path:
        plt.title(
            f"📍 {source} → {destination}  |  "
            f"Shortest Distance: {distance_result[0]} km  |  "
            f"Route: {' → '.join(path)}",
            fontsize=10, pad=12, color="white",
            bbox=dict(facecolor="#1A1A2E", alpha=0.8, edgecolor="none"))

    # --- Legend ---
    legend_elements = [
        mlines.Line2D([],[], color="#00FF88", linewidth=3,            label="Shortest path"),
        mlines.Line2D([],[], color="white",   linewidth=1.5, alpha=0.6, label="Road"),
        mpatches.Patch(color="#E85D24", label="Source / Destination"),
        mpatches.Patch(color="#378ADD", label="City on path"),
        mpatches.Patch(color="#3A3A3A", label="Other city"),
    ]
    ax.legend(handles=legend_elements, loc="lower left",
        fontsize=8, framealpha=0.8,
        facecolor="#1A1A2E", labelcolor="white",
        edgecolor="none")

    plt.axis("off")
    plt.tight_layout()
    plt.draw()


def get_clicked_city(x, y):
    """Find which city node the user clicked on."""
    threshold = 25000  # ~25km radius in mercator units
    for city, (cx, cy) in pos.items():
        if abs(cx - x) < threshold and abs(cy - y) < threshold:
            return city
    return None


def on_click(event):
    if event.xdata is None or event.ydata is None:
        return

    city = get_clicked_city(event.xdata, event.ydata)
    if not city:
        return

    if len(selected) == 0:
        selected.append(city)
        print(f"✅ Source: {city}")
        draw(source=city)

    elif len(selected) == 1:
        if city == selected[0]:
            print("⚠️  Pick a different city for destination.")
            return
        selected.append(city)
        source      = selected[0]
        destination = selected[1]

        dist, path = dijkstra(graph, source, destination)
        distance_result[0] = dist
        current_path[0]    = path

        if not path:
            print(f"❌ No path found between {source} and {destination}.")
            return

        print(f"✅ {source} → {destination} : {dist} km")
        print(f"📍 {' → '.join(path)}")
        draw(path=path, source=source, destination=destination)

    elif len(selected) == 2:
        # Reset and start fresh with new source
        selected.clear()
        selected.append(city)
        print(f"\n🔄 Reset! New source: {city}")
        draw(source=city)


def main():
    fig = plt.figure(figsize=(15, 9))
    fig.patch.set_facecolor("#1A1A2E")
    fig.canvas.mpl_connect('button_press_event', on_click)

    print("\n=== Nepal Shortest Path Finder ===")
    print("👆 Click a city → SOURCE")
    print("👆 Click another → DESTINATION")
    print("👆 Click again → RESET\n")

    draw()
    plt.show()


if __name__ == "__main__":
    main()