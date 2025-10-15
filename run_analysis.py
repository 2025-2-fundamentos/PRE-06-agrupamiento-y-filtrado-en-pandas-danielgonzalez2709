#!/usr/bin/env python3
"""
Script para ejecutar el análisis de datos de conductores.
Este script es una alternativa para ejecutar el análisis sin tener que 
navegar al módulo homework.
"""

from homework import main

if __name__ == "__main__":
    print("=== Análisis de Datos de Conductores ===")
    print("Ejecutando análisis completo...")
    print()
    
    main()
    
    print()
    print("=== Análisis Completado ===")
    print("Archivos generados:")
    print("- files/output/summary.csv")
    print("- files/plots/top10_drivers.png")
