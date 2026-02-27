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

1. En tu proyecto de Supabase, ve a **Project Settings** (el engrane en la parte inferior del menú izquierdo).
2. Selecciona **API** en el sub-menú.
3. Copia el valor de la **Project URL**.
4. Copia el valor de la clave en **Project API keys** sub-sección `anon` / `public`.
5. En la carpeta de tu proyecto en la Mac, busca el archivo `.env.example`, **renómbralo a `.env`** (quítale el `.example`).
6. Abre el archivo `.env` y pega tus valores:
   ```env
   SUPABASE_URL=pega_tu_url_aqui
   SUPABASE_KEY=pega_tu_key_anonima_aqui
   ```

¡Con eso estarás listo al 100%! Dime cuando termines estos pasos para continuar con la programación de las APIs en Python (Fase 4).
