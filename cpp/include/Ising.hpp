#ifndef ISING_H
#define ISING_H
#include<iostream>
#include<random>
#include<vector>
#include<algorithm>
/**
 * A struct to store the paramter of the simulation 
 */
typedef struct Ising_t{
    std::vector<int> lattice; // Square lattice
    double J; // Coupling constant 
    double beta; // Temperature inverse 
    double kb; // Boltzmann constant 
    int n; // Dimension of the lattice 
} ising_t; 

/**
 * A function to generate a random spin state, either up or down. 
 */
int get_state(){

    int randy; // store the value of the random 

    std::random_device dv; // Get randomness from teh device 
                          // This seed will change the result for each excution 
                          // For reproducible results use instead a fixed seed :)
    std::mt19937_64 gen(dv()); // Pesudo random number generator.
    std::uniform_int_distribution<int>  dist(0, 1);  // get either 1 or 0 randomly. 

    randy = dist(gen) * 2 - 1; // Get either -1 or 1.

    return randy;  
}
/**
 * A function to generate an ising lattice
 */

void fill_lattice(std::vector<int> &lattice){

    std::generate(lattice.begin(), lattice.end(), get_state); // Fill the lattice with random states
}
/**
 * 
 */
void print_lattice(std::vector<int> lattice, int n){
    for (int i = 0; i < n; i++)
    {   
        std::cout<<std::endl;
        for (int j = 0; j < n; j++)
        {
            std::cout<<" "<<lattice[i *n + j]<<" ";
        }
        std::cout<<std::endl;
    }
    std::cout<<""<<std::endl;
}; 



#endif // ISING_H