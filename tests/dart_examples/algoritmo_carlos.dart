// Algoritmo enfocado en estructuras de datos: Maps, Sets, Lists

class Producto {
  String nombre;
  double precio;
  
  Producto(this.nombre, this.precio);
}

void main() {
  // Lista simple de productos
  List<Producto> productos = [
    Producto("Laptop", 899.99),
    Producto("Mouse", 25.50),
    Producto("Teclado", 45.00)
  ];
  
  // Map simple de precios
  Map<String, double> precios = {
    "Laptop": 899.99,
    "Mouse": 25.50,
    "Teclado": 45.00
  };
  
  // Set de categorías únicas
  Set<String> categorias = {"Electrónicos", "Accesorios", "Computación"};
  
  // Calcular precio total
  double total = 0.0;
  for (var producto in productos) {
    total += producto.precio;
  }
  print("Precio total: \$${total.toStringAsFixed(2)}");
  
  // Mostrar productos
  for (int i = 0; i < productos.length; i++) {
    print("${i + 1}. ${productos[i].nombre}: \$${productos[i].precio}");
  }
  
  // Mostrar precios del map
  for (var entry in precios.entries) {
    print("${entry.key}: \$${entry.value}");
  }
  
  // Mostrar categorías
  print("Categorías: $categorias");
  
  // Crear lista de precios
  List<double> listaPrecios = [899.99, 25.50, 45.00, 899.99];
  Set<double> preciosUnicos = Set.from(listaPrecios);
  
  print("Precios únicos: $preciosUnicos");
}