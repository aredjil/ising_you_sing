#include "Ising.hpp"
#include <iostream>
#include <vector>
#include <fstream>

int main()
{
    double start = 1.2;
    double end = 3.0;
    // Number of elements to generate
    size_t count = 100;

    int n = 100;
    double J = 1.0;
    std::vector<double> Ts(count);
    double step_ = (end - start) / (count - 1);
    std::generate(Ts.begin(), Ts.end(), [n = 0, start, step_]() mutable
                  { return start + step_ * n++; });
    double energy;

    std::vector<int> lattice(n * n, 1);
    fill_lattice(lattice);
    print_lattice(lattice, n);
    std::ofstream file("energy.dat");
    for (auto T : Ts)
    {
        double mag;
        for (size_t i = 0; i < 10'000; i++)
        {
            auto beta = 1.0 / T;
            step(lattice, n, J, beta);
        }
        mag = std::accumulate(lattice.begin(), lattice.end(), 0);
        std::cout << T << " " << std::abs(mag) / (n * n) << std::endl;
        file << T << " " << std::abs(mag) / (n * n) << std::endl;
    }

    file.close();

    return 0;
}