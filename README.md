"WYSIWYG EDITOR" 
OPENSOURCE
*THANKS TO THE TRIBE OF THE FREE - COSTA RICA*
www.latribucr.site

ESTE SOFTWARE FUE CREADO PARA LA COMUNIDAD DE SENDERISMO DE LA TRIBU DE LOS LIBRES DE COSTA RICA
THIS SOFTWARE WAS CREATED FOR THE HIKING COMMUNITY OF THE TRIBE DE LOS LIBRES OF COSTA RICA



🚀 Guía de Instalación Rápida: Editor Colibrí (Sin Framework)

¡Integrar el editor Colibrí en tu página web es muy fácil! Sigue estos tres sencillos pasos para una instalación limpia y profesional en cualquier proyecto HTML.
Paso 1: 📁 Organiza tus Archivos

Una buena organización es clave. Vamos a crear carpetas específicas para los estilos y la lógica del editor.

    Crea las carpetas: Dentro de la raíz de tu proyecto, crea una carpeta css y otra js.

    Mueve los archivos: Coloca colibri.css y colibri.js en sus respectivas carpetas.

Tu estructura de proyecto debería verse así:

tu-proyecto/
├── index.html
├── css/
│   └── colibri.css
└── js/
    └── colibri.js

Paso 2: 📝 Prepara tu HTML

Ahora, vamos a decirle a tu página HTML dónde encontrar los archivos del editor y dónde debe aparecer.
2.1 Enlaza los Archivos en <head>

Añade las siguientes líneas dentro de la etiqueta <head> de tu archivo HTML. Esto cargará los estilos del editor.

<head>
    <!-- ... otros metadatos y etiquetas ... -->
    <title>Mi Página con Editor</title>

    <!-- Hoja de estilos de Colibrí -->
    <link rel="stylesheet" href="css/colibri.css">

    <!-- Font Awesome para los iconos (Recomendado) -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
</head>

2.2 Crea el Contenedor en <body>

Coloca un <div> con un ID único en el lugar donde quieres que aparezca el editor. Colibrí se construirá automáticamente dentro de este contenedor.

<body>
    <h1>Mi Artículo</h1>
    <p>Usa el editor de abajo para escribir tu contenido.</p>

    <!-- Contenedor para el Editor Colibrí -->
    <div id="mi-editor-personalizado"></div>

    <!-- ... resto del contenido de tu página ... -->
</body>

Paso 3: ✨ Inicializa el Editor con JavaScript

Este es el último paso para darle vida al editor.

Justo antes de que cierre la etiqueta </body>, añade el siguiente bloque de código. Esto carga la lógica del editor y la activa.

    <!-- ... resto del contenido de tu página ... -->

    <!-- Script de Colibrí -->
    <script src="js/colibri.js"></script>

    <!-- Inicializa el editor -->
    <script>
        // Espera a que toda la página se haya cargado
        document.addEventListener('DOMContentLoaded', function() {
            // Crea una nueva instancia del editor, apuntando al ID de tu div
            const miEditor = new ColibriEditor('#mi-editor-personalizado');

            // --- CÓMO OBTENER EL CONTENIDO ---
            // Puedes obtener el HTML del editor en cualquier momento así:
            // const contenidoHtml = miEditor.getContent();
            // console.log(contenidoHtml);
            // Esto es útil para guardarlo en una base de datos al enviar un formulario.
        });
    </script>
</body>

¡Y eso es todo! 🎉 Al seguir esta estructura, tu proyecto estará perfectamente organizado y el editor Colibrí funcionará a la perfección en cualquier página web estándar.
"# colibiri" 
