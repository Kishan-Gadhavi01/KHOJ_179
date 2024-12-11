# KHOJ-179: Simulation of Evacuation Routes and Disaster Mitigation Strategies

## Overview
This repository hosts the project "Simulation of Evacuation Routes and Disaster Mitigation Strategies." The goal is to optimize evacuation planning and simulate real-world disaster scenarios to improve disaster preparedness and resilience.

## Features
- **Evacuation Route Optimization**: Leveraging GIS data and algorithms to create the most efficient routes.
- **Disaster Simulations**: Using SUMO (Simulation of Urban Mobility) to model traffic flow during emergencies.

## Tools and Libraries
- **SUMO**: The main tool for traffic and evacuation simulation.
- **Python**: Required for scripting and integration with SUMO.
- **Libraries**:
  - `TraCi` (Traffic Control Interface): For interacting with SUMO simulations.
  - `libsumo`: A high-performance library for SUMO.

## Getting Started
### Prerequisites
1. **Download SUMO**  
   SUMO can be downloaded from [SUMO Downloads](https://sumo.dlr.de/docs/Downloads.html).

2. **Install Python**  
   Ensure Python is installed on your system. The recommended version is Python 3.7+.

3. **Install Required Libraries**  
   Use the following commands to install the necessary Python libraries:
   ```bash
   pip install sumolib traci
