# Consideraciones Importantes

- La API se encuentra en el siguiente servidor de Heroku: https://api-g25.herokuapp.com

- Se recomienda ENCARECIDAMENTE entrar a la página de la API (link de arriba) unos 5-10 minutos antes de probar la aplicación (para que Heroku inicialize el hosting), ya que al realizar búsquedas pesadas sobre la base de datos de MongoDB se pueden producir errores internos en Heroku antes de dicho intervalo de tiempo (al pasar unos minutos funciona sin problemas, aunque tras una media hora de inactividad se vuelve a 'desactivar'). Las consultas más livianas sobre MongoDB no presentan problemas y se pueden probar inmediatamente, pero se recomienda esperar el tiempo indicado arriba para evitar errores.

- La dirección en la que está corriendo la API se indicará como "API/" en este 
Readme.

- En el caso de que sólo se busque por palabras prohibidas se entregarán todos los resultados sin nigún tipo de filtro.
 
# Rutas Tipo GET

- En la ruta "API/messages" se obtienen todos los mensajes de la base de datos. 
También acepta los parámetros del Text Search para filtrar los mensajes.

- En la ruta "API/messages/mid" se obtiene toda la información del mensaje con 
id 'mid'.

- En la ruta "API/users/uid" se obtiene toda la información del usuario con id 
'uid'. También acepta los parámetros del Text Search para filtrar los mensajes 
emitidos por dicho usuario.

- En la ruta "API/communication/uid_1/uid_2" se obtienen todos los mensajes 
intercambiados entre los usuarios con id 'uid_1' y 'uid_2'.

# Rutas Tipo POST

- La ruta "API/messages" (modo POST) acepta los parámetros para guardar en la 
base de datos un nuevo mensaje entre 2 usuarios. Estos parámetros son: 
'message', 'sender', 'receptant', 'lat', 'long', 'date' (los mismos que ya 
estaban indicados en la variable MESSAGES_KEYS del 'main.py' entregado).

# Rutas Tipo DELETE

- En la ruta "API/messages/mid" (modo DELETE) se puede eliminar de la base de 
datos el mensaje con id 'mid'.
