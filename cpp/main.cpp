#include"Ising.hpp"
#include<iostream>
#include<vector>

int main(){
    int n = 1000; 
    double J = 1.0;
    double beta = 1.0; 

    std::vector<int> lattice(n * n, 1);
    fill_lattice(lattice);
    std::cout<<"Energy Before Step: "<<get_energy(lattice, n,J)<<std::endl;
    // print_lattice(lattice, n);
    for (int i = 0; i < 50; i++)
    {
            step(lattice, n, J, beta);

    }
    
    std::cout<<"Energy After Step: "<<get_energy(lattice, n, J)<<std::endl;
    // print_lattice(lattice, n);
    return 0;
}