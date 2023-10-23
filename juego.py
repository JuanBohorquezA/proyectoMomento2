import random

class AdivinaElNumero:
    
    def __init__(self, minimo=1, maximo=100, vidas=10):
        self.numero = random.randint(minimo, maximo)
        self.vidas = vidas
        self.minimo = minimo
        self.maximo = maximo

    def jugar(self):
        print(f"¡Adivina el número entre {self.minimo} y {self.maximo}!")
        
        while self.vidas > 0:
            try:
                adivinanza = int(input(f"Tienes {self.vidas} intentos restantes. Adivina el número: "))

                if adivinanza == self.numero:
                    print("¡Felicidades, adivinaste el número!")
                    return
                elif adivinanza < self.numero:
                    print("El número es más alto.")
                else:
                    print("El número es más bajo.")
                self.vidas -= 1
            except ValueError:
                print("Por favor, introduce un número válido.")
        
        print(f"¡Se te acabaron los intentos! El número era {self.numero}.")


class PiedraPapelTijeras:
    acciones = ["piedra", "papel", "tijeras"]

    def __init__(self):
        pass

    def eleccion_maquina(self):
        return random.choice(self.acciones)

    def jugar(self):
        eleccion_usuario = input("Elige: piedra, papel o tijeras: ").lower()
        if eleccion_usuario not in self.acciones:
            print("¡Entrada inválida!")
            return

        eleccion_computadora = self.eleccion_maquina()
        print(f"La máquina eligió: {eleccion_computadora}")

        if eleccion_usuario == eleccion_computadora:
            print("¡Es un empate!")
        elif (eleccion_usuario == "piedra" and eleccion_computadora == "tijeras") or \
             (eleccion_usuario == "tijeras" and eleccion_computadora == "papel") or \
             (eleccion_usuario == "papel" and eleccion_computadora == "piedra"):
            print("¡Has ganado!")
        else:
            print("¡La máquina gana!")

def jugar():
    while(True):
        print("\n--- Opciones Juegos ---")
        print("1. Adivina el número")
        print("2. Piedra, Papel o Tijeras")
        print("3. Salir")
        print("--------------------")
        opJuego = input("Seleccione una opción: ")
        if opJuego == '1':
            AdivinaElNumero().jugar()
        elif opJuego == '2':
            PiedraPapelTijeras().jugar()
        elif opJuego == '3':
            break 
    