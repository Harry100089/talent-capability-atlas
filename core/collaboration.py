def build_collaboration_graph(profiles):
    graph = {}

    for p in profiles:
        graph[p.name] = {}

    for p1 in profiles:
        for p2 in profiles:
            if p1.name == p2.name:
                continue

            shared = {
                s.skill for s in p1.skills
            } & {
                s.skill for s in p2.skills
            }

            if shared:
                graph[p1.name][p2.name] = len(shared)

    return graph
