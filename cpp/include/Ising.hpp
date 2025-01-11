#ifndef ISING_H
#define ISING_H
#include <iostream>
#include <random>
#include <vector>
#include <algorithm>
#include <filesystem>
#include<fstream>
#include<iomanip>
#ifdef _OPENACC
#include<openacc.h>
#endif

std::mt19937_64 gen(std::random_device{}()); // Create the random number generator globally
double get_uniform()
{
    std::uniform_real_distribution<double> dist(0.0, 1.0);
    return dist(gen);
}
// Generate a random spin state
int get_state()
{
    std::uniform_int_distribution<int> dist(0, 1); // 0 or 1
    return dist(gen) * 2 - 1;                      // Returns either -1 or 1
}

// Generate a random index between 0 and n-1
int get_indices(int n)
{
    std::uniform_int_distribution<int> dist(0, n - 1);
    return dist(gen);
}

// Fill lattice with random spin states
void fill_lattice(std::vector<int> &lattice)
{
    std::generate(lattice.begin(), lattice.end(), get_state); // Fill the lattice with random states
}

// Print lattice
void print_lattice(const std::vector<int> &lattice, int n)
{
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            std::cout << lattice[i * n + j] << " ";
        }
        std::cout << std::endl;
    }
}

// Calculate the energy of the lattice
double get_energy(const std::vector<int> &lattice, const int &n, const double &J)
{
    double energy = 0.0;
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            int neighbors = lattice[((i + 1) % n) * n + j] + lattice[i * n + ((j + 1) % n)] +
                            lattice[((i - 1 + n) % n) * n + j] + lattice[i * n + ((j - 1 + n) % n)];
            energy += -J * neighbors * lattice[i * n + j];
        }
    }
    return energy / 2; // Avoid double-counting interactions
}

// Perform one Metropolis-Hasting step
void step(std::vector<int> &lattice, const int &n, const double &J, const double &beta)
{
    #ifdef _OPENACC
    #pragma acc parallel loop 
    #else
    #endif
    for (int k = 0; k < n * n; k++)
    {
        int i = get_indices(n);
        int j = get_indices(n);
        int current_spin = lattice[i * n + j];

        int neighbors = lattice[((i + 1) % n) * n + j] + lattice[i * n + ((j + 1) % n)] +
                        lattice[((i - 1 + n) % n) * n + j] + lattice[i * n + ((j - 1 + n) % n)];

        double dE = 2.0 * J * current_spin * neighbors;
        double randy = get_uniform();
        if (dE < 0 || randy < std::exp(-beta * dE))
        {
            lattice[i * n + j] *= -1;
        }
    }
}

void simulate(std::vector<int> &lattice, const int &n, const double &J, const double &beta, const int &steps) {
    std::string foldername = "./data";

    // Ensure the directory exists
    if (!std::filesystem::exists(foldername)) {
        if (!std::filesystem::create_directory(foldername)) {
            std::cerr << "Error: Failed to create directory '" << foldername << "'." << std::endl;
            return;
        }
    }

    for (int i = 0; i < steps; i++) {
        std::ostringstream filenamestream;
        filenamestream << foldername << "/lattice_" << std::setw(3) << std::setfill('0') << i << ".dat";
        std::string filename = filenamestream.str();

        // Create and write to the file
        std::ofstream file(filename);
        if (file) {
            file << "Simulated data for step " << i << "\n"; // Example placeholder data
            file.close();
            std::cout << "File '" << filename << "' created successfully." << std::endl;
        } else {
            std::cerr << "Error: Could not create file '" << filename << "'." << std::endl;
        }
    }
}


#endif // ISING_H
