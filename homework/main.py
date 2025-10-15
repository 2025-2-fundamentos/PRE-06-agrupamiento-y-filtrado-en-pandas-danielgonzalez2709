"""
Análisis de datos de conductores y generación de reportes.
Este script procesa datos de conductores y hojas de tiempo para generar:
1. Un resumen en CSV con estadísticas por conductor
2. Un gráfico de los top 10 conductores por horas trabajadas
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

def load_data():
    """Carga los datos de conductores y hojas de tiempo."""
    # Cargar datos de conductores
    drivers_df = pd.read_csv('files/input/drivers.csv')
    
    # Cargar datos de hojas de tiempo
    timesheet_df = pd.read_csv('files/input/timesheet.csv')
    
    return drivers_df, timesheet_df

def create_summary(drivers_df, timesheet_df):
    """Crea un resumen con estadísticas por conductor."""
    
    # Agrupar datos de timesheet por conductor
    timesheet_summary = timesheet_df.groupby('driverId').agg({
        'hours-logged': ['sum', 'mean', 'max'],
        'miles-logged': ['sum', 'mean', 'max'],
        'week': 'count'  # número de semanas trabajadas
    }).round(2)
    
    # Aplanar los nombres de columnas
    timesheet_summary.columns = [
        'total_hours', 'avg_hours_per_week', 'max_hours_week',
        'total_miles', 'avg_miles_per_week', 'max_miles_week',
        'weeks_worked'
    ]
    
    # Resetear índice para hacer merge
    timesheet_summary = timesheet_summary.reset_index()
    
    # Hacer merge con datos de conductores
    summary_df = pd.merge(drivers_df, timesheet_summary, on='driverId', how='left')
    
    # Llenar valores NaN con 0 para conductores sin registros de tiempo
    summary_df = summary_df.fillna(0)
    
    # Calcular eficiencia (millas por hora)
    summary_df['miles_per_hour'] = (summary_df['total_miles'] / 
                                   summary_df['total_hours']).round(2)
    summary_df['miles_per_hour'] = summary_df['miles_per_hour'].fillna(0)
    
    return summary_df

def create_top10_plot(summary_df):
    """Crea un gráfico de barras con los top 10 conductores por horas totales."""
    
    # Obtener top 10 conductores por horas totales
    top10 = summary_df.nlargest(10, 'total_hours')
    
    # Crear el gráfico
    plt.figure(figsize=(12, 8))
    bars = plt.bar(range(len(top10)), top10['total_hours'], 
                   color='steelblue', alpha=0.7)
    
    # Personalizar el gráfico
    plt.title('Top 10 Conductores por Horas Totales Trabajadas', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Conductores', fontsize=12)
    plt.ylabel('Horas Totales', fontsize=12)
    
    # Configurar etiquetas del eje X
    plt.xticks(range(len(top10)), top10['name'], rotation=45, ha='right')
    
    # Añadir valores en las barras
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 10,
                f'{int(height)}h', ha='center', va='bottom', fontweight='bold')
    
    # Ajustar layout
    plt.tight_layout()
    plt.grid(axis='y', alpha=0.3)
    
    # Guardar el gráfico
    plt.savefig('files/plots/top10_drivers.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """Función principal que ejecuta todo el análisis."""
    
    print("Cargando datos...")
    drivers_df, timesheet_df = load_data()
    
    print(f"Datos cargados:")
    print(f"- {len(drivers_df)} conductores")
    print(f"- {len(timesheet_df)} registros de tiempo")
    
    print("\nCreando resumen...")
    summary_df = create_summary(drivers_df, timesheet_df)
    
    # Guardar el resumen en CSV
    summary_df.to_csv('files/output/summary.csv', index=False)
    print("✓ Resumen guardado en files/output/summary.csv")
    
    print("\nCreando gráfico de top 10 conductores...")
    create_top10_plot(summary_df)
    print("✓ Gráfico guardado en files/plots/top10_drivers.png")
    
    # Mostrar algunas estadísticas
    print(f"\nEstadísticas generales:")
    print(f"- Total de horas trabajadas: {summary_df['total_hours'].sum():,.0f}")
    print(f"- Total de millas recorridas: {summary_df['total_miles'].sum():,.0f}")
    print(f"- Promedio de horas por conductor: {summary_df['total_hours'].mean():.1f}")
    print(f"- Conductor con más horas: {summary_df.loc[summary_df['total_hours'].idxmax(), 'name']} "
          f"({summary_df['total_hours'].max():.0f} horas)")

if __name__ == "__main__":
    main()
