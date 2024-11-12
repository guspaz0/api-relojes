# API relojes

Antes de clonar el repo, se requiere usar relojes biometricos de la linea Zkteco. este proyecto utiliza la libreria de [pyzk](https://github.com/fananimi/pyzk)

### introduccion
Dentro de una organizacion, como una Pyme, donde concurren muchas personas para cumplir con sus labores diarias, el control de horarios y asistencias es un factor critico. Hoy gracias al avance de las tecnologias, existen dispositivos de control de horarios con sistemas biometricos que hacen que esta tarea sea mucho mas amena. Pero algunos dispositivos solo cumplen con la tarea mecanica de registrar estos eventos y se necesita un posprocesamiento de la informacion para que tome valor real para la empresa. 


### Desarrollo
El cliente necesitaba poder manejar los relojes de asistencia de manera remota, centralizada, economica y ajustada a sus necesidades especificas, para automatizar procesos internos, debido al volumen de datos que manejaba.
Si bien existian soluciones comerciales Saas en el mercado brindado por el mismo fabricante, se desestimaron tales soluciones por ser complejas y tener muchas funcionalidades que el cliente no requeria. 
Entonces, se optó por hacer un desarrollo a medida, que sea accesible, multiplataforma, moderna y con poca infraestructura.Cuando se habla de accesible, me refiero a economico, las alternativas Open Source abundan actualmente y las comunidades crecen año tras año. Es asi que se opto por usar una libreria basada en Python y por ende, desarrollar todo el backend en este lenguaje tan popular, atraves de una API restful y complementar el proyecto con un frontend con React + Redux.

### Backend
Emplea como lenguaje principal Python. 
Las tecnologias empleadas son: 
- FastApi, framework para creacion de apis.
- Uvicorn, interface para server web.
- pyZk, para comunicar con relojes.
- PostreSQL, base de datos.
- psycopg para conectar a la BD.
- JWT (json web tockens) para authenticacion.
- Docker, para gestionar los entornos virtuales.
- python-dotenv, para gestion de variables de entorno.

Debes incluir las variables de entorno en el archivo .env antes de levantar el proyecto.

### Fronted
Desarrollado con React.

... en construccion.
