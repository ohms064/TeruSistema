# TeruSistema

El sistema de cobro y cierre de cajas de TeruTeru

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


------------------------------Versión anterior---------------------------------------------------------
En la ventana principal existen dos secciones: la parte de cobro de la comanda y la sección de consumo. Ambas son independientes
entre sí.
	
La sección de cobro se requiere llenar los datos de Clientes, Total y Dinero recibido, si Propina se deja en blanco se considera 
que es cero. Una vez llenado dar click en Aceptar y se nos abrirá otra ventana con la información de la transacción que incluye 
la información ya dada, el total con la propina y el cambio. Es importante escribir aparte la propina del total para tener el control
de cuanto hay de propina. Una vez confirnado se da click en Aceptar para que la información se guardé en el sistema, sino estamos 
de acuerdo podemos cerrar la ventana.
El botón de borrar en la sección de cobro borra todos los datos de la sección.

La sección de consumo es completamente opcional. En el cuadro de texto escribimos los precios de lo que se haya consumido separado por
espacios (ejemplo: pidieron onigiris y un te frío se escribiría (35 25)). Cuando terminemos damos click en Aceptar de la parte de abajo
y nos desplegará otra ventana con el Total, la Propina Sugerida y el Total con la Propina Sugerida (Total Sugerido). Dando click en Aceptar
nos cierra la ventana y limpia los datos de consumo.
Al igual que en la sección de cobro, el botón de borrar de la sección de consumo borra los datos de la misma.

Si hubiera algún error de escritura (escribir una letra en lugar de un número) en cualquiera de las dos secciones anteriores se desplegará
una ventana de error.
----------------------------------------------------------------------------------------------------