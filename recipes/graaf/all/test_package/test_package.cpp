#include <filesystem>
#include <string>

#include <graaflib/graph.h>
#include <graaflib/io/dot.h>
#include <graaflib/types.h>

struct my_vertex {
  int number{};
  std::string name{};
};

enum class edge_priority { LOW, HIGH };

struct my_edge {
  edge_priority priority{edge_priority::LOW};
  float weight{};
};

auto create_graph() {
  graaf::directed_graph<my_vertex, my_edge> graph{};

  auto const vertex_1{graph.add_vertex(my_vertex{10, "some data"})};
  auto const vertex_2{graph.add_vertex(my_vertex{20, "some more data"})};
  auto const vertex_3{graph.add_vertex(my_vertex{30, "abc"})};
  auto const vertex_4{graph.add_vertex(my_vertex{40, "123"})};
  auto const vertex_5{graph.add_vertex(my_vertex{50, "xyz"})};

  graph.add_edge(vertex_1, vertex_2, my_edge{edge_priority::HIGH, 3.3});
  graph.add_edge(vertex_2, vertex_1, my_edge{edge_priority::HIGH, 5.0});
  graph.add_edge(vertex_1, vertex_3, my_edge{edge_priority::HIGH, 1.0});
  graph.add_edge(vertex_3, vertex_4, my_edge{edge_priority::LOW, 2.0});
  graph.add_edge(vertex_3, vertex_5, my_edge{edge_priority::HIGH, 3.0});
  graph.add_edge(vertex_2, vertex_5, my_edge{edge_priority::LOW, 42.0});

  return graph;
}

int main() {
  auto const my_graph{create_graph()};
}