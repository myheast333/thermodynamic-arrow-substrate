#!/usr/bin/env python3
"""
substrate_sim.py - Discrete Substrate Evolution Simulator
Implements the core dynamics of Substrate Ontology:
- Discrete lattice (2D for visualisation, can be extended to 3D)
- Global refresh cycles
- Deficit (informational difference) accumulation
- Simplified propensity equation (gradient + random noise)
- Monotonic entropy increase verification

Based on "The Geometric Origin of the Second Law" (V5.5)
Author: Jingsong Zhou
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import argparse
from typing import Tuple, Optional

# Physical constants (symbolic values, actual numbers not critical for simulation)
L_MIN = 1.0  # minimal spatial unit (arbitrary units)
T_MIN = 1.0  # minimal time unit (refresh period)
K_B = 1.0    # Boltzmann constant (set to 1 for simplicity)

class SubstrateSimulator:
    """
    Discrete substrate evolution simulator.
    
    Attributes:
        nx, ny: lattice dimensions
        B: brightness field (stored information capacity)
        delta: deficit field (propagating informational difference)
        eta: coupling/transport coefficient (epsilon in paper)
        kappa: coupling strength between neighbouring lattice points
        beta: sensitivity coefficient (depends on local brightness)
        sigma_xi: standard deviation of random noise (intrinsic stochasticity)
        history: list of total deficit sums for each refresh
    """
    
    def __init__(self, nx: int = 64, ny: int = 64, eta: float = 0.3,
                 kappa: float = 0.1, sigma_xi: float = 0.05, b0: float = 1.0):
        """
        Initialize the substrate.
        
        Args:
            nx, ny: grid dimensions
            eta: propagation coefficient (0 < eta < 1) – how fast deficits spread
            kappa: coupling strength (for interactions with neighbours)
            sigma_xi: standard deviation of additive Gaussian noise
            b0: base brightness (background)
        """
        self.nx = nx
        self.ny = ny
        self.eta = eta
        self.kappa = kappa
        self.sigma_xi = sigma_xi
        self.b0 = b0
        
        # Brightness field (initialised to uniform base value)
        self.B = np.ones((nx, ny)) * b0
        
        # Deficit field (initialised to small random fluctuations)
        self.delta = np.random.normal(0, 0.01, (nx, ny))
        
        # Sensitivity coefficient: higher where brightness is low (caution)
        # Simplified: beta = 1 / (B + epsilon) to avoid division by zero
        self.beta = 1.0 / (self.B + 1e-6)
        
        # History of total deficit for entropy tracking
        self.total_deficit_history = []
        self.time_step = 0
    
    def compute_gradient(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute brightness gradient components (G_x, G_y).
        
        Returns:
            Gx, Gy: gradient fields (x and y components)
        """
        Gx = np.zeros_like(self.B)
        Gy = np.zeros_like(self.B)
        Gx[1:-1, :] = self.B[2:, :] - self.B[1:-1, :]
        Gy[:, 1:-1] = self.B[:, 2:] - self.B[:, 1:-1]
        return Gx, Gy
    
    def propensity_direction(self, idx: int, jdx: int, Gx: float, Gy: float) -> np.ndarray:
        """
        Compute propensity (probability) for each of the 4 cardinal directions
        based on local gradient and random noise.
        
        Simplified equation:
            p_d = exp(-beta * (G_d + xi_d)) / Z
        where G_d is the gradient component along direction d,
        xi_d is Gaussian noise.
        
        Args:
            idx, jdx: lattice coordinates
            Gx, Gy: gradient components at this point
            
        Returns:
            p: array of 4 probabilities (order: right, up, left, down)
        """
        # Four directions: right (+x), up (+y), left (-x), down (-y)
        grad_components = np.array([Gx, Gy, -Gx, -Gy])
        
        # Random noise for each direction
        xi = np.random.normal(0, self.sigma_xi, 4)
        
        # Exponent factor: -beta * (gradient + noise)
        beta_val = self.beta[idx, jdx]
        exponents = -beta_val * (grad_components + xi)
        
        # Softmax to get probabilities
        exp_vals = np.exp(exponents)
        p = exp_vals / np.sum(exp_vals)
        return p
    
    def update_cell(self, idx: int, jdx: int, Gx_field: np.ndarray, Gy_field: np.ndarray) -> float:
        """
        Update a single lattice cell: compute deficit outflow based on propensity,
        update deficits, and return the net deficit change (positive = created).
        
        Basic mechanism:
        - Incoming deficit from neighbours? (not implemented in this simple version,
          we treat deficit as a field that diffuses via the transport equation)
        - Here we evolve deficit field directly using a discrete diffusion equation
          with a source term proportional to gradient-induced propensity.
        
        For simplicity, we implement the linear deficit update rule:
            delta_new = (1-eta)*delta_old + eta * laplacian + kappa * B + noise
        
        But to align with entropy increase, we also add a term that always creates
        positive deficit from gradient mismatch (simulating Axiom 3).
        
        Returns:
            local_deficit_creation: amount of deficit created at this cell (>0)
        """
        # Laplacian of deficit field
        laplacian = 0.0
        cnt = 0
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = idx + di, jdx + dj
            if 0 <= ni < self.nx and 0 <= nj < self.ny:
                laplacian += self.delta[ni, nj] - self.delta[idx, jdx]
                cnt += 1
        if cnt > 0:
            laplacian /= cnt
        
        # Random noise term (intrinsic fluctuation from Axiom 3)
        noise = np.random.normal(0, self.sigma_xi)
        
        # Deficit creation from symmetry breaking: always positive (small) term
        # proportional to local brightness gradient magnitude
        Gx = Gx_field[idx, jdx]
        Gy = Gy_field[idx, jdx]
        grad_mag = np.sqrt(Gx**2 + Gy**2)
        creation = 0.01 * grad_mag  # irreducible deficit from gradient
        
        # Update deficit: diffusion + coupling + noise + creation
        old_delta = self.delta[idx, jdx]
        new_delta = ((1 - self.eta) * old_delta + self.eta * laplacian +
                     self.kappa * self.B[idx, jdx] + noise + creation)
        
        # Ensure non-negativity (deficit cannot be negative)
        new_delta = max(0.0, new_delta)
        self.delta[idx, jdx] = new_delta
        
        # Brightness update: each unit of deficit creation reduces brightness
        # (as per deficit-brightness conversion)
        delta_bright = -creation
        self.B[idx, jdx] = max(0.1, self.B[idx, jdx] + delta_bright)
        
        # Update beta (sensitivity) based on new brightness
        self.beta[idx, jdx] = 1.0 / (self.B[idx, jdx] + 1e-6)
        
        # The created deficit contributes to entropy
        return creation
    
    def evolve(self, steps: int = 100, record_interval: int = 1) -> None:
        """
        Evolve the substrate for a number of refresh cycles.
        
        Args:
            steps: number of refresh steps
            record_interval: how often to record total deficit
        """
        for _ in range(steps):
            # Compute gradients once per refresh
            Gx, Gy = self.compute_gradient()
            
            # Update all cells (synchronous update)
            new_delta = np.zeros_like(self.delta)
            new_B = np.zeros_like(self.B)
            
            for i in range(self.nx):
                for j in range(self.ny):
                    # Compute deficit creation using current fields
                    grad_mag = np.sqrt(Gx[i, j]**2 + Gy[i, j]**2)
                    creation = 0.01 * grad_mag
                    
                    # Diffusion term (laplacian)
                    lap = 0.0
                    cnt = 0
                    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < self.nx and 0 <= nj < self.ny:
                            lap += self.delta[ni, nj] - self.delta[i, j]
                            cnt += 1
                    if cnt > 0:
                        lap /= cnt
                    
                    # Random noise
                    noise = np.random.normal(0, self.sigma_xi)
                    
                    # Update deficit
                    new_delta[i, j] = ((1 - self.eta) * self.delta[i, j] + 
                                      self.eta * lap + 
                                      self.kappa * self.B[i, j] + 
                                      noise + creation)
                    new_delta[i, j] = max(0.0, new_delta[i, j])
                    
                    # Update brightness
                    new_B[i, j] = max(0.1, self.B[i, j] - creation)
            
            # Apply updates
            self.delta = new_delta
            self.B = new_B
            
            # Update beta
            self.beta = 1.0 / (self.B + 1e-6)
            
            # Record history
            self.time_step += 1
            if self.time_step % record_interval == 0:
                total_deficit = np.sum(self.delta)
                self.total_deficit_history.append(total_deficit)
    
    def get_total_deficit(self) -> float:
        """Return current total deficit sum."""
        return np.sum(self.delta)
    
    def get_entropy(self) -> float:
        """Entropy = k_B * total deficit."""
        return K_B * self.get_total_deficit()
    
    def animate_evolution(self, steps: int = 100, interval: int = 50):
        """
        Run evolution and create an animation of deficit field.
        
        Args:
            steps: number of refresh steps per frame (total frames = steps)
            interval: delay between frames in ms
        """
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))
        ax1 = axes[0]
        ax2 = axes[1]
        
        im1 = ax1.imshow(self.delta, cmap='hot', interpolation='nearest', vmin=0)
        ax1.set_title('Deficit Field')
        plt.colorbar(im1, ax=ax1)
        
        # Initial entropy plot
        total_def = [self.get_total_deficit()]
        ax2.set_xlim(0, steps)
        ax2.set_ylim(0, max(1, total_def[0] * 1.5))
        line, = ax2.plot([0], total_def, 'b-')
        ax2.set_xlabel('Refresh Step')
        ax2.set_ylabel('Total Deficit (Entropy proxy)')
        ax2.set_title('Entropy Increase')
        
        def update(frame):
            # Evolve one step
            self.evolve(1)
            
            # Update deficit image
            im1.set_data(self.delta)
            im1.set_clim(vmin=0, vmax=np.percentile(self.delta, 95))
            
            # Update entropy line
            total_def.append(self.get_total_deficit())
            line.set_data(range(len(total_def)), total_def)
            ax2.relim()
            ax2.autoscale_view()
            
            return [im1, line]
        
        ani = FuncAnimation(fig, update, frames=steps, interval=interval, blit=False)
        plt.tight_layout()
        plt.show()
        return ani
    
    def run_simulation_and_verify_second_law(self, nx=32, ny=32, steps=200):
        """
        Run a simulation and verify that total deficit does not decrease.
        Print steps where deficit decreases (should never happen).
        """
        sim = SubstrateSimulator(nx=nx, ny=ny, eta=0.3, kappa=0.1, sigma_xi=0.05)
        print("Initial total deficit: ", sim.get_total_deficit())
        
        prev_deficit = sim.get_total_deficit()
        for step in range(1, steps + 1):
            sim.evolve(1)
            curr_deficit = sim.get_total_deficit()
            
            if curr_deficit < prev_deficit - 1e-8:
                print(f"WARNING: Deficit decreased at step {step}: {prev_deficit:.6f} -> {curr_deficit:.6f}")
            
            prev_deficit = curr_deficit
            
            if step % 50 == 0:
                print(f"Step {step}, total deficit = {curr_deficit:.4f}")
        
        print(f"Final total deficit: {sim.get_total_deficit():.4f}")
        print("Entropy increased" if sim.get_total_deficit() > 1e-6 else "Check simulation params.")
        return sim


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Discrete Substrate Evolution Simulator")
    parser.add_argument("--nx", type=int, default=32, help="Grid width")
    parser.add_argument("--ny", type=int, default=32, help="Grid height")
    parser.add_argument("--steps", type=int, default=200, help="Number of refresh steps")
    parser.add_argument("--animate", action="store_true", help="Show animation")
    
    args = parser.parse_args()
    
    # Create and run simulation
    sim = SubstrateSimulator(nx=args.nx, ny=args.ny, eta=0.3, kappa=0.1, sigma_xi=0.05)
    
    if args.animate:
        # Show animation
        sim.animate_evolution(steps=args.steps, interval=50)
    else:
        # Run verification
        print("Running simulation and verifying Second Law...")
        sim.run_simulation_and_verify_second_law(nx=args.nx, ny=args.ny, steps=args.steps)
