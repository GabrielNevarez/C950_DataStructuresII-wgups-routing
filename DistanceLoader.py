from DistanceGraph import DistanceGraph
from Location import Location


class DistanceLoader:

    @staticmethod
    def load(locations):
        graph = DistanceGraph(locations)

        # Temporary test distances.
        graph.set_distance(0, 1, 3.0)
        graph.set_distance(0, 2, 5.0)
        graph.set_distance(0, 3, 4.0)
        graph.set_distance(0, 4, 6.0)
        graph.set_distance(0, 5, 7.0)
        graph.set_distance(0, 6, 8.0)

        graph.set_distance(1, 2, 2.0)
        graph.set_distance(1, 3, 4.0)
        graph.set_distance(2, 3, 3.0)

        graph.set_distance(3, 4, 2.5)
        graph.set_distance(4, 5, 3.0)
        graph.set_distance(5, 6, 2.0)

        return graph