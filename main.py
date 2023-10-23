from connection import conneccion
from juego import jugar
import re
cursor = conneccion()
class Usuario:  
    
    def __init__(self):
        self._lastname = ""
        self._name = ""
        self._user = ""
        self._password = ""
        self.roll = 3
    def login(self):
        self._user = input("Ingrese su nombre de usuario: ")
        self._password = input("Ingrese su contraseña: ")
        if self.logginValue():
            user_data = self.get_user_data()
            UserLogged = UsuarioLogueado(user_data)
            UserLogged.show_menu_logueado()
            return
        print("Nombre de usuario y/o contraseña incorrecto") 
    def get_user_data(self):
        cursor.execute("SELECT UserName,psw,nombre,apellido,roll FROM usuario WHERE UserName ='{0}'  AND psw = '{1}'".format(self._user, self._password))
        user_data = cursor.fetchone()
        return user_data

    @staticmethod
    def validate_password(password:str) -> bool:
        return all([
            re.search(r"[A-Z]", password),  # al menos una mayúscula
            re.search(r"[a-z]", password),  # al menos una minúscula
            re.search(r"\d", password),     # al menos un número
            re.search(r"[!@#$%^&*()_+\-=[\]{}|;:'\",.<>?/]", password),  # al menos un carácter especial
            len(password) >= 8
        ])
    def register(self):
        self._name = input("Ingrese su nombre: ").lower()
        self._lastname = input("Ingrese su apellido: ").lower()
        while(True):
            self._user = input("Ingrese su nombre de usuario: ")
            if not(self.registerValue()): break
            else: print("EL Nombre DE USUARIO YA ESTÁ EN USO\n")
        while(True):
            self._password = input("Ingrese su contraseña: ")
            if(Usuario.validate_password(self._password)):break
            print("LA CONTRASEÑA DEBE TENER UNA MAYUSCULA, UNA MINUSCULA, UN CARÁCTER ESPECIAL Y UN NUMERO Y UN MINIMO DE 8 CARACTERES")
            
        
        vip = input("Desea obtener un rol VIP? s/n: ").lower()=="s" 
        if(vip): self.roll = 2
        
        if not self.registerValue():
            cursor.execute("insert into usuario (UserName,psw,nombre,apellido,roll) VALUES ('{0}','{1}','{2}','{3}',{4})".format(self._user, self._password, self._name, self._lastname, self.roll))
            cursor.commit()
            print("!USUARIO REGISTRADO EXISTOSAMENTE!")


    def logginValue(self):   
        cursor.execute("select UserName,psw,nombre,apellido,roll from usuario")
        for user in cursor:
            if self._user == user[0] and self._password == user[1]:
                return True
        return False
    def registerValue(self):   
        cursor.execute("select UserName,psw,nombre,apellido,roll from usuario")
        for user in cursor:
            if self._user == user[0]:
                return True
        return False


class UsuarioLogueado(Usuario):
    def __init__(self, user_data):
        super().__init__()
        self._user = user_data[0]
        self._password = user_data[1]
        self._name = user_data[2]
        self._lastname = user_data[3]
        self.roll = user_data[4]

    def show_menu_logueado(self):
        while True:
            print(f"\n--- MENÚ DE {self._user.upper()} ---")
            print("1. Ver perfil")
            print("2. Cambiar contraseña")
            print("3. Opciones VIP" if self.roll == 2 or self.roll == 1 else "")
            print("4. Opciones Admin" if self.roll == 1 else "")
            print("5. Cerrar sesión")
            opcion = input("\nSeleccione una opción: ")

            if opcion == '1':
                self.ver_perfil()
            elif opcion == '2':
                self.cambiar_contrasena()
            elif opcion == '3' and (self.roll == 2 or self.roll == 1):
                self.opciones_vip()
            elif opcion == '4' and self.roll == 1:
                self.opcionesAdmin()
            elif opcion == '5':
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida. Intente nuevamente.")

    def ver_perfil(self):
        # Implementa la lógica para ver el perfil
        print("\n--- Tu Perfil ---")
        print(f"Usuario: {self._user}")
        print(f"Nombre: {self._name}")
        print(f"Apellido: {self._lastname}")
        print(f"Rol: {self.roll}")
        print("-----------------")

    def cambiar_contrasena(self):
        # Implementa la lógica para cambiar la contraseña
        print("\n--- Cambiar Contraseña ---")
        
        while(True):
            _ = input("Ingrese la Contraseña actual: ")
            if(self._password != _):
                print("Contraseña incorrecta\n")
                continue
            nueva_password = input("Nueva contraseña: ")
            nueva_password2 = input("Repite la nueva contraseña: ")
            if nueva_password != nueva_password2:
                print("Las contraseñas no coinciden\n") 
                continue
            self.validate_password(nueva_password)
            if self.validate_password(nueva_password): break
            print("La contraseña debe tener una mayúscula, una minúscula, un número, un carácter especial y tener al menos 8 caracteres\n")
        cursor.execute("update usuario set psw = '{0}' where UserName = '{1}'".format(nueva_password, self._user))
        cursor.commit()
        print("¡Contraseña actualizada!")


    def viewCommonUsers(self):
        cursor.execute("select UserName,psw,nombre,apellido,roll from usuario where roll = 3")
        print("__________________________________________________________")
        print("\n------------- Lista de usuarios Comunes ----------------")    
        for user in cursor:
            print(f"Usuario: {user[0]}")
            print(f"Contraseña: {user[1]}")
            print(f"Nombre: {user[2]}")
            print(f"Apellido: {user[3]}")
            print(f"Rol: {user[4]}")
            print("--------------------------------")
        print("__________________________________________________________")
    def viewVIPUsers(self):
        cursor.execute("select UserName,psw,nombre,apellido,roll from usuario where roll = 2")
        print("__________________________________________________________")
        print("\n------------- Lista de usuarios Comunes ----------------")    
        for user in cursor:
            print(f"Usuario: {user[0]}")
            print(f"Contraseña: {user[1]}")
            print(f"Nombre: {user[2]}")
            print(f"Apellido: {user[3]}")
            print(f"Rol: {user[4]}")
            print("--------------------------------")
        print("__________________________________________________________")

    def delete_user(self):
        if (input("ESTA SEGURO QUE DESEA ELIMINAR AL USUARIO?  S/N ").lower() == "s"):
            passWord=input("Ingresa tu contraseña como usuario Administrador ")
            if not self._password == passWord: 
                print("Contraseña incorrecta")
                return
            userToDelete = input("Ingresa el nombre de usuario a eliminar: ")    
            cursor.execute("select * from usuario where UserName = '{0}'".format(userToDelete))
            if cursor.fetchone() is None:
                print("¡El usuario no existe!")
                return
            cursor.execute("delete from usuario where UserName = '{0}'".format(userToDelete))
            cursor.commit()
            print("¡Usuario eliminado!")
        print("hiciste lo correcto bob.")


    def opciones_vip(self):
        # Implementa lógicas específicas para usuarios VIP
      while(True):
        print("\n--- Opciones VIP ---")
        print("1. Jugar ") 
        print("2. Salir")       
        print("--------------------")
        op = input("Seleccione una opción: ")
        if op == '1':
          jugar()
        elif op != '1':
            break

    def opcionesAdmin(self):
       while(True):
        print("\n--- Opciones Admin ---")
        print("1. Ver lista de usuarios comunes")
        print("2. ver lista de usuarios VIP")
        print("3. Borrar usuario")
        print("4. Jugar")
        print("5. Salir")
        op = input("Seleccione una opción: ")
        if op == '1':
            self.viewCommonUsers()
        elif op == '2':
            self.viewVIPUsers()
        elif op == '3':
            self.delete_user()
        elif op == '4':
            jugar()
        elif op == '5':
            break
        else:
            print("¡Entrada inválida!")

    
class Main:
    def __init__(self):
        pass
        
    def menu_principal(self):
        User = Usuario()
        while True:
            print("\n--- MENÚ PRINCIPAL ---")
            print("1. Iniciar sesión")
            print("2. Registrar usuario")
            print("3. Salir\n")
            
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                User.login()
            elif opcion == '2':
                User.register()
            elif opcion == '3':
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida. Intente nuevamente.")

        
        


Main = Main()
Main.menu_principal()
        