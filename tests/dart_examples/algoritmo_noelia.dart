List<int> obtenerPares(List<int> numeros) {
  List<int> pares = [];
  for (var numero in numeros) {
    if (numero % 2 == 0) {
      pares.add(numero);
    }
  }
  return pares;
}

void main() {
  List<int> numeros = [1, 2, 3, 4, 5, 6];
  List<int> pares = obtenerPares(numeros);
  print("Números pares: \$pares");
}