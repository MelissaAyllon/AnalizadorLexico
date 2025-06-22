// Algoritmo enfocado en bucles for y estructuras de control

class Tarea {
  String titulo;
  bool completada;
  
  Tarea(this.titulo, this.completada);
}

void main() {
  // Lista simple de tareas
  List<Tarea> tareas = [
    Tarea("Estudiar Dart", false),
    Tarea("Hacer ejercicio", false),
    Tarea("Leer documentación", true),
    Tarea("Limpiar casa", false)
  ];
  
  // Bucle for tradicional
  print("Lista de tareas:");
  for (int i = 0; i < tareas.length; i++) {
    String estado = tareas[i].completada ? "✓" : "○";
    print("${i + 1}. $estado ${tareas[i].titulo}");
  }
  
  // Bucle for-in
  print("\nTareas completadas:");
  for (var tarea in tareas) {
    if (tarea.completada) {
      print("✓ ${tarea.titulo}");
    }
  }
  
  // Contar tareas pendientes
  int pendientes = 0;
  for (var tarea in tareas) {
    if (!tarea.completada) {
      pendientes++;
    }
  }
  print("Tareas pendientes: $pendientes");
  
  // Marcar primera tarea como completada
  if (tareas.isNotEmpty) {
    tareas[0].completada = true;
    print("Tarea '${tareas[0].titulo}' marcada como completada");
  }
  
  // Mostrar estado final
  print("\nEstado final:");
  for (int i = 0; i < tareas.length; i++) {
    String estado = tareas[i].completada ? "Completada" : "Pendiente";
    print("${i + 1}. ${tareas[i].titulo} - $estado");
  }
}