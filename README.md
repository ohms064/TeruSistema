# TeruSistema

El sistema de cobro y cierre de cajas de TeruTeru

Instalación:

Instalar la versión de python que corresponda al sistema operativo: https://www.python.org/downloads/release/python-343/

Para ejecutar el programa abrir el archivo TeruGUI.pyw, se tiene que elegir como programa determinado el programa de
la ruta de instalación de "pythonw" dentro de C:/python34 (Para windows), 

Como se usa:

El sistema es parecido a la versión anterior.
Al abrir el programa aparcerá una pequeña ventana con dos botones: "Nueva Mesa" y "Cerrar Caja".
"Nueva Mesa" abre la misma interfaz que en la versión anterior (a excepción del botón "Cerrar Caja"), se puede
utilizar el cuadro de consumo para agregar los precios de lo que se tiene en la comanda separado por espacios, 
al dar click en "Calcular" el resultado se sustituirá en el cuadro de "Total" en la parte superior y la respectiva
propina en el recuadro "Propina", si se diera click en el botón "Sumar" el valor total de "Consumo" se sumará
al valor de "Total" con su respectiva propina.

Para poder cobrar una comanda se requiere añadir el número de clientes a "Clientes" y el dinero con el que está
pagando y dar click en "Aceptar", se nos mostrará el recibo con el cambio que se le debe dar al cliente y dos botnes:
"Aceptar" y "Cancelar", si aceptamos la comanda se guardará en el sistema y si se cancela nos regresa a la ventana
anterior.

En resumen los pasos para usar el programa son como siguen:

 1.- Dar click en "Nueva Mesa"

 2.- Escribir los precios de consumo del cliente en la sección de "Consumo" y dar click en "Sumar" o "Añadir" como
 sea requerido

 3.- Cuando el cliente quiera pagar, llenar los datos de Número de clientes, Dinero recibido, verificar propina (se 
 puede dejar vacío) y Total si se omitio el paso 2.

 4.- Se abrirá una nueva ventana con el resumen de la transacción, verificarlo y en caso de que sea correcto dar click
 en "Aceptar", en caso contrario dar click en "Cancelar" y se nos regresará a la ventana anterior.

 5.- Una vez dado click en "Aceptar" la transacción se guardará en el sistema.

 En cualquier momento se puede hacer el paso 1 y tener varias mesas activas al mismo tiempo.


Nueva Versión!
Se agregó la funcionalidad de guardar Clientes para poder darles promociones en función al número de visitas que haga.

Inmediatamente se verá en el menú principal un nuevo botón llamado "Clientes". Si hacemos click nos abrirá una ventana donde
podremos buscar clientes por id, nick, correo o nombre (en esa jerarquía, es decir si escribimos id y nick buscará por id), 
insertar nuevos clientes a nuestra base de datos, borrar clientes y actualizar los datos de algún cliente.
