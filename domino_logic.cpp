#include <pybind11/pybind11.h>
#include <pybind11/stl.h>          // For std::vector, std::string, std::map, etc.
#include <pybind11/functional.h>   // If you're binding std::function
#include <pybind11/chrono.h>       // If you're using std::chrono types
#include <pybind11/complex.h>      // For std::complex

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <random>
#include <algorithm>
#include <vector>
#include <nlohmann/json.hpp>

namespace py = pybind11;
using json = nlohmann::json;

std::vector<std::vector<json>> deal_dominos_cpp(const std::vector<json>& deck) {
    std::vector<json> shuffled_deck = deck;
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(shuffled_deck.begin(), shuffled_deck.end(), g);

    std::vector<std::vector<json>> hands(4, std::vector<json>());

    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 7; ++j) {
            hands[i].push_back(shuffled_deck[i * 7 + j]);
        }
    }

    return hands;
}

PYBIND11_MODULE(domino_cpp, m) {
    m.def("deal_dominos_cpp", &deal_dominos_cpp, "Shuffle and deal dominos into 4 hands");
}