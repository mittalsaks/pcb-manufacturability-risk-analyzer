#!/usr/bin/env python3
"""
Sample script to generate documentation images for PCB Risk Analyzer
Run this script to create sample visualizations for the documentation
"""

import numpy as np
import matplotlib.pyplot as plt
import os

def create_sample_heatmaps():
    """Generate sample heatmaps for documentation"""

    # Create sample data
    np.random.seed(42)
    size = 20

    # Density heatmap - simulate trace concentration
    density = np.random.rand(size, size) * 0.8
    # Add some high-density regions
    density[5:10, 5:10] += 0.5
    density[12:17, 12:17] += 0.3

    # Thermal heatmap - correlated with density
    thermal = density ** 2 * np.random.rand(size, size) * 2

    # EMI heatmap - with neighbor coupling
    emi = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            # Add neighbor effects
            neighbors = density[max(0,i-1):min(size,i+2), max(0,j-1):min(size,j+2)]
            emi[i,j] = density[i,j] + np.mean(neighbors) * 0.5

    # Temperature map
    temperature = 25 + thermal * 15  # Ambient + thermal stress

    # Create figure with subplots
    fig, axs = plt.subplots(1, 4, figsize=(20, 5))

    # Density heatmap
    im1 = axs[0].imshow(density.T, origin='lower', cmap='viridis', extent=[0, 100, 0, 100])
    axs[0].set_title('Density Heatmap\n(Trace Concentration)', fontsize=12, fontweight='bold')
    plt.colorbar(im1, ax=axs[0], shrink=0.8)
    axs[0].set_xlabel('X (mm)')
    axs[0].set_ylabel('Y (mm)')

    # Thermal heatmap
    im2 = axs[1].imshow(thermal.T, origin='lower', cmap='inferno', extent=[0, 100, 0, 100])
    axs[1].set_title('Thermal Heatmap\n(Heat Generation)', fontsize=12, fontweight='bold')
    plt.colorbar(im2, ax=axs[1], shrink=0.8, label='Thermal Intensity')
    axs[1].set_xlabel('X (mm)')
    axs[1].set_ylabel('Y (mm)')

    # EMI heatmap
    im3 = axs[2].imshow(emi.T, origin='lower', cmap='coolwarm', extent=[0, 100, 0, 100])
    axs[2].set_title('EMI Risk Map\n(Signal Coupling)', fontsize=12, fontweight='bold')
    plt.colorbar(im3, ax=axs[2], shrink=0.8)
    axs[2].set_xlabel('X (mm)')
    axs[2].set_ylabel('Y (mm)')

    # Temperature map
    im4 = axs[3].imshow(temperature.T, origin='lower', cmap='hot', extent=[0, 100, 0, 100])
    axs[3].set_title('Temperature Map\n(°C)', fontsize=12, fontweight='bold')
    plt.colorbar(im4, ax=axs[3], shrink=0.8, label='Temperature (°C)')
    axs[3].set_xlabel('X (mm)')
    axs[3].set_ylabel('Y (mm)')

    # Add hotspot indicators (red boxes)
    threshold = np.max(density) * 0.6
    for i in range(size):
        for j in range(size):
            if density[i,j] >= threshold:
                x1, x2 = i*5, (i+1)*5
                y1, y2 = j*5, (j+1)*5
                for ax in axs:
                    ax.add_patch(plt.Rectangle((x1, y1), x2-x1, y2-y1,
                                             fill=False, edgecolor='red', linewidth=2))

    plt.tight_layout()
    plt.savefig('sample_heatmaps.png', dpi=300, bbox_inches='tight')
    plt.show()

    print("Sample heatmaps saved as 'sample_heatmaps.png'")

def create_trace_width_histogram():
    """Generate sample trace width distribution histogram"""

    # Simulate trace widths (in mm)
    np.random.seed(42)
    widths = np.random.normal(0.2, 0.05, 1000)
    # Add some outliers
    widths = np.concatenate([widths, np.random.choice([0.1, 0.15, 0.25, 0.3], 50)])

    plt.figure(figsize=(10, 6))
    plt.hist(widths, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    plt.axvline(np.mean(widths), color='red', linestyle='--', linewidth=2,
                label=f'Mean: {np.mean(widths):.3f} mm')
    plt.axvline(np.min(widths), color='orange', linestyle='--', linewidth=2,
                label=f'Min: {np.min(widths):.3f} mm')
    plt.xlabel('Trace Width (mm)')
    plt.ylabel('Frequency')
    plt.title('Trace Width Distribution Analysis', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('trace_width_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()

    print("Trace width histogram saved as 'trace_width_distribution.png'")

def create_risk_distribution_pie():
    """Generate sample risk distribution pie chart"""

    # Sample risk distribution
    risk_data = {
        'Safe (Green)': 935,
        'Moderate (Yellow)': 55,
        'High Risk (Red)': 10
    }

    colors = ['#4CAF50', '#FFC107', '#F44336']
    explode = (0, 0.1, 0.2)

    plt.figure(figsize=(8, 8))
    plt.pie(risk_data.values(), labels=risk_data.keys(), colors=colors,
            explode=explode, autopct='%1.1f%%', startangle=90,
            wedgeprops={'edgecolor': 'black', 'linewidth': 1})
    plt.title('Risk Distribution Analysis\n(Total Grid Cells: 1000)',
              fontsize=14, fontweight='bold')
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('risk_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()

    print("Risk distribution pie chart saved as 'risk_distribution.png'")

def create_correlation_plot():
    """Generate sample correlation analysis plot"""

    np.random.seed(42)
    n_points = 100

    # Generate correlated data
    density = np.random.rand(n_points)
    thermal = density * 0.8 + np.random.rand(n_points) * 0.2

    # Calculate correlation
    correlation = np.corrcoef(density, thermal)[0, 1]

    plt.figure(figsize=(10, 6))
    plt.scatter(density, thermal, alpha=0.6, color='blue', s=50)
    plt.xlabel('Normalized Trace Density')
    plt.ylabel('Thermal Stress Level')
    plt.title(f'Density vs Thermal Correlation Analysis\nCorrelation Coefficient: {correlation:.3f}',
              fontsize=14, fontweight='bold')

    # Add trend line
    z = np.polyfit(density, thermal, 1)
    p = np.poly1d(z)
    plt.plot(density, p(density), "r--", linewidth=2, alpha=0.8)

    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('correlation_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

    print("Correlation plot saved as 'correlation_analysis.png'")

if __name__ == "__main__":
    print("Generating sample documentation images...")

    # Create images directory if it doesn't exist
    os.makedirs('Images', exist_ok=True)
    os.chdir('Images')

    create_sample_heatmaps()
    create_trace_width_histogram()
    create_risk_distribution_pie()
    create_correlation_plot()

    print("\nAll sample images generated in 'Images/' directory!")
    print("You can use these images in your documentation.")