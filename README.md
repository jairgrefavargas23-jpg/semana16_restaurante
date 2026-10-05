# Restaurante App - Semana 16: Interacción con eventos en Tkinter

Nombre del estudiante: Bryan Jair Grefa Alvarado

Proyecto de la asignatura **Programación Orientada a Objetos**. Es la evolución de la aplicación gráfica `restaurante_app` de la Semana 15: se mantiene la arquitectura del servicio, la pestaña de Ventas y el patrón `tuple[bool, str]`, y se transforma la pestaña "Consulta de Usuarios" (antes solo lectura) en una gestión completa (CRUD) con roles, para trabajar el manejo real de eventos con `bind()`.

## Propósito de la Semana 16

Comprender la diferencia entre `command=` (acción explícita de un botón, ya usada desde la Semana 14) y `bind()` (respuesta directa a un evento generado por el usuario: seleccionar una fila, pulsar una tecla, cambiar un Combobox). La pestaña **Gestión de Usuarios** es el caso práctico: se agregan roles (`Administrador`, `Empleado`, `Cliente`) y un control de acceso básico, visible solo para el rol `Administrador`.

## Estructura del proyecto

```
restaurante_app/
├── assets/
│   ├── icons/
│   └── logo/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── main.py
└── README.md
```

| Capa | Responsabilidad |
|------|-----------------|
| `datos/` | Archivos JSON con los productos, los usuarios (ahora con `rol`) y las ventas. |
| `modelos/` | Clases `Producto`, `Usuario` y `Venta`, con conversión a y desde diccionarios (`to_dict` / `from_dict`). `Usuario` incorpora `ROLES_PERMITIDOS` y el validador estático `validar_rol`. |
| `servicios/` | `ArchivoServicio` lee y escribe los JSON. `RestauranteServicio` contiene la autenticación, las validaciones y el CRUD completo de productos, ventas y ahora usuarios; todos los métodos de escritura devuelven `tuple[bool, str]`. |
| `ui/` | `LoginView` (inicio de sesión) y `MainView` (interfaz principal, con pestañas). Solo presentan datos y piden las operaciones al servicio. |
| `main.py` | Punto de entrada: crea el servicio, configura el icono de la ventana, muestra el login y abre la vista principal. No se modificó esta semana. |

## Componentes y contenedores utilizados

**Contenedores**
- `tk.Tk`: ventana principal de la aplicación.
- `tk.Toplevel`: ventana de inicio de sesión, con el logotipo del sistema.
- `tk.Frame` y `ttk.Frame`: agrupan zonas de la interfaz (encabezado, botones, pestañas).
- `ttk.LabelFrame`: separa el formulario de producto, el catálogo, el formulario de usuario, la tabla de usuarios y el formulario e historial de ventas.
- `ttk.Notebook`: navegación por pestañas entre "Gestión de Productos", "Gestión de Usuarios" (solo Administrador) y "Ventas".

**Componentes**
- `ttk.Label`: títulos y etiquetas de campos, incluyendo el logotipo en el encabezado y la etiqueta de "Rol seleccionado".
- `ttk.Entry`: captura de ID, nombre, precio, usuario y contraseña (`show="*"` en ambos formularios de contraseña).
- `ttk.Combobox`: selección de la categoría del producto; selección del rol de usuario (nuevo); selección del usuario y del producto a vender.
- `ttk.Checkbutton`: indica si el producto está disponible para la venta.
- `ttk.Button`: acciones mediante `command=`, con iconos de `assets/icons/`.
- `ttk.Treeview` con `ttk.Scrollbar`: tablas de productos, usuarios y ventas.

**Gestores de geometría**
- `pack`: distribución de las zonas principales (encabezado, pestañas, panel izquierdo y derecho).
- `grid`: alineación de las etiquetas, campos y botones dentro de cada formulario.

## Pestaña Gestión de Usuarios: manejo de eventos con `bind()` (nuevo — Semana 16)

```
Interaccion del usuario -> evento -> bind() -> callback(event) -> RestauranteServicio -> usuarios.json -> tabla actualizada
```

| Evento | Widget | Callback | Efecto |
|---|---|---|---|
| `<<TreeviewSelect>>` | Tabla de usuarios | `_al_seleccionar_usuario` | Carga el usuario seleccionado en el formulario |
| `<Return>` | Contraseña / Rol | `_al_presionar_enter_usuario` | Registra el usuario desde el formulario |
| `<Escape>` | Todos los campos y la tabla | `_al_presionar_escape_usuario` | Limpia el formulario y cancela la selección |
| `<<ComboboxSelected>>` | Combobox de rol | `_al_seleccionar_rol` | Actualiza la etiqueta "Rol seleccionado" |

Botones con `command=`: **Registrar**, **Actualizar**, **Eliminar**, **Limpiar**. Ningún callback contiene lógica de negocio ni toca el JSON directamente: todos delegan en `RestauranteServicio`, que valida y devuelve `(bool, str)`, igual que `registrar_producto` o `registrar_venta`.

`RestauranteServicio` impide eliminar el usuario con el que se inició sesión y cambiar el rol del administrador actualmente conectado, para que la aplicación nunca quede sin una cuenta administrativa activa.

## Pestaña Ventas: flujo de eventos aplicado (Semana 15)

```
Usuario elige un Usuario y un Producto en los Combobox
              |
Clic en "Registrar Venta"  (command=self._registrar_venta)
              |
Callback _registrar_venta() en MainView:
  - lee el texto seleccionado en cada Combobox
  - lo traduce al username / id_producto real
  - llama a servicio.registrar_venta(username_cliente, id_producto)
              |
RestauranteServicio.registrar_venta():
  - valida que ambos campos vengan seleccionados
  - valida que el usuario exista
  - valida que el producto exista
  - crea el objeto Venta y lo agrega a la lista en memoria
  - guarda la lista completa en ventas.json
  - devuelve (True, mensaje) o (False, mensaje)
              |
El callback muestra el mensaje con messagebox y, si tuvo exito,
refresca la tabla de ventas (Treeview) con _refrescar_tabla_ventas()
```

Esta pestaña se conserva sin cambios; convive con Gestión de Usuarios como ejemplo de la diferencia entre `command=` y `bind()`. Igual que `registrar_producto`, `actualizar_producto`, `eliminar_producto` y ahora `registrar_usuario`, `actualizar_usuario` y `eliminar_usuario`, ninguno de estos métodos lanza excepciones: todos devuelven una tupla `(bool, str)` que la interfaz interpreta para decidir si muestra éxito o error.

## Recursos gráficos (assets/)

- `assets/logo/logo.png`: logotipo mostrado en la ventana de inicio de sesión.
- `assets/logo/icono.png`: versión simplificada usada como icono de la ventana principal (`iconphoto`) y junto al nombre de usuario en el encabezado de `MainView`.
- `assets/icons/`: iconos para los botones de cada pestaña (Registrar, Cargar/Consultar, Actualizar, Eliminar, Limpiar y Registrar Venta), reutilizados también en el nuevo formulario de usuarios.

## Control de acceso

| Rol | Acceso a la pestaña Gestión de Usuarios |
|---|---|
| `Administrador` | Sí |
| `Empleado` | No |
| `Cliente` | No |

La pestaña ni siquiera se construye cuando el rol conectado no es `Administrador`; no se implementa un sistema avanzado de permisos, solo este control básico por rol.

## Operaciones sobre usuarios, productos y ventas

Todas se ejecutan con botones (`command=`) o eventos (`bind()`) y se delegan a `RestauranteServicio`:

- **Registrar / Actualizar / Eliminar / Cargar-Consultar producto:** igual que en semanas anteriores.
- **Registrar / Actualizar / Eliminar usuario (nuevo):** valida campos obligatorios, rol permitido, username duplicado, protege al administrador actual y persiste en `usuarios.json`.
- **Registrar Venta:** relaciona el usuario y el producto seleccionados en los combobox, valida su existencia y guarda la venta.

Validaciones realizadas en el servicio: ID y nombre obligatorios, ID no repetido, categoría válida, precio numérico y no negativo; para usuarios, username/contraseña/nombre obligatorios, rol válido (`Administrador`, `Empleado` o `Cliente`), username no repetido; para ventas, usuario y producto obligatorios y que ambos existan.

## Persistencia

Los productos se guardan en `datos/productos.json`, las ventas en `datos/ventas.json` y los usuarios ahora se guardan (no solo se leen) en `datos/usuarios.json` mediante `_guardar_usuarios()`, todo a través de `ArchivoServicio`, invocado desde `RestauranteServicio`. La interfaz nunca lee ni escribe archivos directamente. Los cambios se conservan al cerrar y volver a abrir la aplicación.

Ejemplo de usuario persistido:

```json
{
    "username": "mesero1",
    "password": "123",
    "nombre": "Juan Pérez",
    "rol": "Empleado"
}
```

## Cómo ejecutar

Requisitos: Python 3.10 o superior. No se necesitan librerías externas (solo la biblioteca estándar, con Tkinter incluido).

```bash
cd restaurante_app
python main.py
```

Usuarios de prueba incluidos en `datos/usuarios.json`:

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| `admin` | `123` | Administrador |
| `mesero1` | `123` | Empleado |
| `cliente1` | `123` | Cliente |

## Pruebas realizadas

- Se ejecutó `main.py`: la aplicación inicia sin errores y muestra el icono del sistema en la ventana.
- El login muestra el logotipo y continúa validando usuario y contraseña correctamente.
- La pestaña "Gestión de Productos" conserva el CRUD completo de semanas anteriores.
- Con la sesión de `admin` aparece la pestaña "Gestión de Usuarios"; con `cliente1` (Cliente) la pestaña no se construye.
- Se registró un usuario nuevo con rol `Empleado` desde el formulario; apareció de inmediato en la tabla.
- Al seleccionar una fila de la tabla (`<<TreeviewSelect>>`), los datos se cargaron correctamente en el formulario.
- Se actualizaron el nombre, la contraseña y el rol de un usuario seleccionado; el cambio se reflejó en la tabla y en `usuarios.json`.
- Se intentó cambiar el rol del administrador con el que se inició sesión: el servicio devolvió `(False, mensaje)`.
- Se intentó eliminar el usuario con el que se inició sesión: el servicio devolvió `(False, mensaje)`.
- Se usó la tecla `Enter` desde el campo Contraseña para registrar un usuario, y `Escape` para limpiar el formulario y cancelar la selección.
- El Combobox de rol actualizó la etiqueta "Rol seleccionado" al cambiar de valor (`<<ComboboxSelected>>`).
- La pestaña Ventas se probó sin cambios y continúa registrando ventas mediante `command=`.
- Se cerró y volvió a abrir la aplicación: los usuarios, productos y ventas registrados se recuperaron correctamente.
