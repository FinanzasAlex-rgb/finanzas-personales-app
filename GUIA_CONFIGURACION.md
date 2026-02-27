# Guía de Carga a GitHub y Conexión a Supabase

## 1. Subir tu proyecto a GitHub (Directo desde la página web)

Dado que no usaremos la terminal ni GitHub Desktop, vamos a subir los archivos manualmente desde la página web de GitHub:

1. Ve a [GitHub.com](https://github.com/) e inicia sesión.
2. Haz clic en el botón verde **"New"** (o "Nuevo Repositorio") en el panel izquierdo.
3. Dale el nombre `finanzas-personales-app`.
4. **NO marques** las opciones "Add a README file" o "Add .gitignore" (deja todo eso desmarcado, nosotros ya los tenemos listos).
5. Haz clic en **Create repository**.
6. En la siguiente pantalla que aparece, busca un enlace de texto pequeño que dice algo similar a **"uploading an existing file"** (subir archivos existentes) y haz clic en él.
7. Se abrirá una pantalla para arrastrar archivos.
8. En tu Mac, ve al Finder (Escritorio > `FINANZAS PERSONALES APP`).
9. Selecciona **todos los archivos y carpetas** que están dentro (excepto la carpeta `venv` si la ves, los archivos ocultos como `.git` y el `.env`).
10. Arrastra y suelta todos esos archivos seleccionados directamente en el área de la página web de GitHub.
11. Espera a que se carguen todos los archivos. Abajo, en la caja verde, haz clic en **Commit changes** (Guardar cambios).

¡Listo! Tu código ya está guardado de forma segura en GitHub.

---

## 2. Configurar la Base de Datos en Supabase

1. Ve a [Supabase.com](https://supabase.com/) e inicia sesión (o crea una cuenta).
2. Haz clic en **New Project** y dale un nombre como `finanzas-personales`.
3. Ingresa una contraseña segura para la base de datos y selecciona una región cercana a ti. Espera un par de minutos a que se cree el proyecto.
4. En el menú izquierdo de tu proyecto de Supabase, ve a la sección **SQL Editor**.
5. Haz clic en el botón de **"New query"** (Nueva consulta).
6. **Abre el archivo `supabase_schema.sql`** que acabo de generar en la carpeta de tu proyecto. Copia todo su contenido.
7. Pégalo en el SQL Editor de Supabase y presiona el botón **Run** (Ejecutar) en la esquina inferior derecha. Esto creará todas las tablas necesarias (Usuarios, Ingresos, Gastos, Deudas, etc.).

---

## 3. Conectar tu App Local a Supabase

*(Paso completado. El archivo `.env` ya fue configurado en tu máquina local).*

---

## 4. Obtener tu Link Público Mundial (Usar sin la Mac encendida)

Para que puedas abrir la app en tu teléfono (o cualquier parte) 24/7 sin depender de la computadora, vamos a subir tu código a **Render**, un servidor gratuito para Python:

1. Ve a **[Render.com](https://render.com/)** y crea una cuenta gratis usando tu perfil de GitHub.
2. Una vez dentro de Render, haz clic en el botón de **"New"** (Nuevo) y selecciona **"Web Service"** (Servicio Web).
3. Selecciona **"Build and deploy from a Git repository"**.
4. Te pedirá conectar tu GitHub. Dale permiso y selecciona el repositorio `finanzas-personales-app`.
5. En la configuración del servicio:
   * **Name:** finanzas-vip
   * **Region:** (Cualquiera cercana a ti, ej. US East)
   * **Instance Type:** Free (Gratis)
   * *Nota: Render detectará automáticamente el archivo `render.yaml` que acabo de crear para ti, así que no necesitas configurar los comandos de Python manualmente.*
6. Desplázate hacia abajo y haz clic en **"Advanced"**.
7. Busca el botón **"Add Environment Variable"** (Agregar variable de entorno), y agrega DOS variables exactamente iguales a las que pusimos en tu `.env` (sin las comillas):
   - Key: `SUPABASE_URL` | Value: `(Pega aquí tu enlace de supabase que empieza con https://)`
   - Key: `SUPABASE_KEY` | Value: `(Pega aquí el código larguísimo de Supabase)`
   *(Nota: También puedes agregar la de Gemini de una vez: Key: `GEMINI_API_KEY` | Value: `tu-llave-gemini`)*
8. Finalmente, dale clic al botón azul **"Create Web Service"**.

Render empezará a construir tu computadora virtual en la nube. Toma unos 3 a 5 minutos. Cuando termine y diga **"Live"** en verde, verás un link arriba a la izquierda que será algo como: `https://finanzas-vip.onrender.com`.

**¡LISTO!** Abre ese enlace en Safari en tu iPhone. Dale al icono de compartir y selecciona **"Agregar a inicio"**. Tendrás el ícono de tu app financiera en el celular y funcionará para siempre.
