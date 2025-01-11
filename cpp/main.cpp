#include "Ising.hpp"
#include <iostream>
#include <vector>
#include <fstream>
#include<chrono>
#ifdef _OPENACC
#include<openacc.h>
#endif
int main()
{
    double start = 2.0;
    double end = 3.0;
    // Number of elements to generate
    size_t count = 20;

    int n = 100;
    double J = 1.0;
    std::vector<double> Ts(count);
    double step_ = (end - start) / (count - 1);
    std::generate(Ts.begin(), Ts.end(), [n = 0, start, step_]() mutable
                  { return start + step_ * n++; });
    double energy;

    std::vector<int> lattice(n * n, 1);
    fill_lattice(lattice);
    std::ofstream file("energy.dat");
    int iter = 1;
    std::cout<<"Program Started!"<<std::endl;
    std::chrono::high_resolution_clock::time_point start_t = std::chrono::high_resolution_clock::now();
    for (auto T : Ts)
    {
        double mag;
        for (size_t i = 0; i < 10'000; ++i)
        {
            auto beta = 1.0 / T;
            step(lattice, n, J, beta);
        }
        std::cout<<"#Iteration, "<<" T,"<<" <M>"<<std::endl;
        mag = std::accumulate(lattice.begin(), lattice.end(), 0);
        std::cout <<iter<<", "<<T<< ", " << std::abs(mag) / (n * n) << std::endl;
        file << T << " " << std::abs(mag) / (n * n) << std::endl;
        iter++;
    }
    std::chrono::high_resolution_clock::time_point end_t = std::chrono::high_resolution_clock::now();
    auto elapsed = std::chrono::duration_cast<std::chrono::minutes>(end_t - start_t).count();    
    std::cout<<"Program Finished!"<<std::endl;
    std::cout<<"Time elapsed: "<<elapsed<<" m"<<std::endl;
    file.close();

    return 0;
}