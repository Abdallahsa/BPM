import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt

# Function to check if the Petri net is sound
def is_sound(pn):
    # Check if there are any dead transitions
    for transition in pn['transitions']:
        if not any(p['input'] >= p['output'] for p in pn['flows'] if p['transition'] == transition):
            return False

    # Check if there are any unbounded places
    for place in pn['places']:
        tokens = pn['initial_marking'].get(place, 0)
        if tokens > 0 and not any(p['output'] >= tokens for p in pn['flows'] if p['place'] == place):
            return False

    return True


# Function to draw the reachability graph
def draw_reachability_graph(pn):
    graph = nx.DiGraph()

    # Add places and transitions as nodes
    graph.add_nodes_from(pn['places'])
    graph.add_nodes_from(pn['transitions'])

    # Add flows as edges
    for flow in pn['flows']:
        graph.add_edge(flow['place'], flow['transition'])
        # Only add the arrow in one direction
        if flow['input'] == 0:
            graph.add_edge(flow['transition'], flow['place'])

    # Draw the reachability graph
    pos = nx.spring_layout(graph)
    nx.draw_networkx(graph, pos, with_labels=True, node_color='lightblue')
    plt.show()


# Function to handle the submit button click
def submit():
    # Get the input values from the GUI
    place_names = input_places.get().split(',')
    transitions = input_transitions.get().split(',')

    # Create the Petri net dictionary
    pn = {
        'places': place_names,
        'transitions': transitions,
        'flows': [],
        'initial_marking': {}
    }

    # Parse the flows and initial marking
    for flow in input_flows.get().split(','):
        flow_parts = flow.split(':')
        place = flow_parts[0]
        transition = flow_parts[1]
        direction = flow_parts[2]

        pn['flows'].append({
            'place': place,
            'transition': transition,
            'input': direction.count('-'),
            'output': direction.count('+')
        })

    for place_entry in input_marking_entries.values():
        place_name = place_entry[0].get()
        marking = place_entry[1].get()
        pn['initial_marking'][place_name] = int(marking)

    # Check soundness and display the result
    if is_sound(pn):
        result_label.config(text='The Petri net is sound.')
    else:
        result_label.config(text='The Petri net is not sound.')

    # Draw the reachability graph
    draw_reachability_graph(pn)


# Create the GUI
root = tk.Tk()
root.title('Petri Net Soundness Checker')
root.geometry('400x500')

# Input fields and labels
places_label = tk.Label(root, text='Places (comma-separated):')
input_places = tk.Entry(root)
places_label.pack()
input_places.pack()

transitions_label = tk.Label(root, text='Transitions (comma-separated):')
input_transitions = tk.Entry(root)
transitions_label.pack()
input_transitions.pack()

flows_label = tk.Label(root, text='Flows (place:transition:direction):')
input_flows = tk.Entry(root)
flows_label.pack()
input_flows.pack()

marking_label = tk.Label(root, text='Initial Marking:')
marking_label.pack()

input
marking_label.pack()

input_marking_entries = {}

num_places = 5  # Enter the desired number of places here

for i in range(num_places):
    place_label = tk.Label(root, text=f'P{i+1}:')
    place_entry = tk.Entry(root)
    place_label.pack()
    place_entry.pack()
    input_marking_entries[i] = (place_entry, tk.StringVar())

# Test case values
place_names = ['p1', 'p2', 'p3', 'p4', 'p5']
transitions = ['t1', 't2', 't3']
flows = ['p1:t1:1-', 'p2:t1:1-', 't1:p3:1+', 'p3:t2:1-', 't2:p4:1+', 'p4:t3:1-', 't3:p2:1-', 't3:p5:1-']
initial_marking = {'p1': 1, 'p2': 1, 'p3': 0, 'p4': 0, 'p5': 0}

# Assigning test case values to input fields
input_places.insert(0, ','.join(place_names))
input_transitions.insert(0, ','.join(transitions))
input_flows.insert(0, ','.join(flows))

for i, place in enumerate(place_names):
    input_marking_entries[i][0].insert(0, place)
    input_marking_entries[i][1].set(initial_marking[place])

# Submit button
submit_button = tk.Button(root, text='Submit', command=submit)
submit_button.pack()

# Result label
result_label = tk.Label(root, text='')
result_label.pack()

# Call the submit function to automatically check the Petri net
submit()

# Run the GUI main loop
root.mainloop()
