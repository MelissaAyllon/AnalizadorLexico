bool esMayorDeEdad(int edad) {
  return edad >= 18;
}

void main() {
  int edad = 20;
  if (esMayorDeEdad(edad)) {
    print("Eres mayor de edad");
  } else {
    print("Eres menor de edad");
  }
}