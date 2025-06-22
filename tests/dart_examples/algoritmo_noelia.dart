void main() {
  // Double expressions
  double pi = 3.14159;
  double radius = 5.0;
  double area = pi * radius * radius;
  
  // Traditional for loop
  for (int i = 0; i < 10; i++) {
    print("Número: $i");
  }
  
  // For-in loop
  List<int> numbers = [1, 2, 3, 4, 5];
  for (var num in numbers) {
    print("Valor: $num");
  }
  
  // Map declaration
  Map<String, int> ages = {"Alice": 25, "Bob": 30, "Charlie": 35};
  Map<String, String> cities = {};
  
  // Set declaration
  Set<int> uniqueNumbers = {1, 2, 3, 4, 5};
  Set<String> names = {"Alice", "Bob", "Charlie"};
  Set<double> temperatures = {};
} 