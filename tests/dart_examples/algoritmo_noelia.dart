// Algoritmo enfocado en funciones y validaciones básicas

class Calculadora {
  static double sumar(double a, double b) {
    return a + b;
  }
  
  static double multiplicar(double a, double b) {
    return a * b;
  }
  
  static double calcularArea(double radio) {
    if (radio <= 0) {
      print("Error: El radio debe ser positivo");
      return 0.0;
    }
    return 3.14159 * radio * radio;
  }
}

class Validador {
  static bool esPar(int numero) {
    return numero % 2 == 0;
  }
  
  static bool esPositivo(int numero) {
    return numero > 0;
  }
  
  static bool esMayorQue(int numero, int limite) {
    return numero > limite;
  }
}

void main() {
  // Probar funciones de calculadora
  double resultado1 = Calculadora.sumar(5.5, 3.2);
  double resultado2 = Calculadora.multiplicar(4.0, 2.5);
  
  print("5.5 + 3.2 = $resultado1");
  print("4.0 * 2.5 = $resultado2");
  
  // Calcular área de círculo
  double area1 = Calculadora.calcularArea(3.0);
  double area2 = Calculadora.calcularArea(-1.0);
  
  print("Área del círculo (radio 3): $area1");
  print("Área del círculo (radio -1): $area2");
  
  // Validar números
  List<int> numeros = [2, 5, 8, 10, 15];
  
  print("\nValidación de números:");
  for (int numero in numeros) {
    bool esPar = Validador.esPar(numero);
    bool esPositivo = Validador.esPositivo(numero);
    bool esMayorQue5 = Validador.esMayorQue(numero, 5);
    
    print("Número $numero:");
    print("  ¿Es par? $esPar");
    print("  ¿Es positivo? $esPositivo");
    print("  ¿Es mayor que 5? $esMayorQue5");
  }
  
  // Crear lista de números pares
  List<int> pares = [];
  for (int numero in numeros) {
    if (Validador.esPar(numero)) {
      pares.add(numero);
    }
  }
  print("Números pares: $pares");
  
  // Crear set de números únicos
  Set<int> numerosUnicos = {2, 5, 8, 10, 15, 2, 5};
  print("Números únicos: $numerosUnicos");
  
  // Crear map de resultados
  Map<String, double> resultados = {
    "suma": resultado1,
    "multiplicacion": resultado2,
    "area": area1
  };
  
  print("Resultados:");
  for (var entry in resultados.entries) {
    print("${entry.key}: ${entry.value}");
  }
} 