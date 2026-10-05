class Usuario:
    ROLES_PERMITIDOS = ("Administrador", "Empleado", "Cliente")

    def __init__(self, username: str, password: str, nombre: str, rol: str):
        self.username = username.strip()
        self.password = password.strip()
        self.nombre = nombre.strip()
        self.rol = self.validar_rol(rol)

    @staticmethod
    def validar_rol(rol: str) -> str:
        # Semana 16: restringe el rol a los valores definidos por el sistema.
        rol_normalizado = (rol or "").strip().capitalize()
        if rol_normalizado not in Usuario.ROLES_PERMITIDOS:
            raise ValueError("El rol debe ser Administrador, Empleado o Cliente.")
        return rol_normalizado

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "password": self.password,
            "nombre": self.nombre,
            "rol": self.rol
        }

    @staticmethod
    def from_dict(data: dict):
        return Usuario(
            username=data["username"],
            password=data["password"],
            nombre=data["nombre"],
            rol=data.get("rol", "Cliente")
        )
