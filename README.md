# Base backend fastapi (python)

## Primeros comandos
```bash
# Crear entorno
virtualenv .venv
# O
python -m venv .venv

# Activar entorno
.\.venv\Scripts\activate

# Instalar dependencias en el entorno
pip install -r .\requirements.txt
```

## Ejecutar aplicacion localmente
```bash
uvicorn app.api:app --reload
uvicorn main:app --reload 
uvicorn application:application --reload
```

## Guardar nuevas dependencias del entorno virtual
```bash
pip freeze > .\requirements.txt
```

## Armar una version zip para subir (con 7zip)
```bash
# Con 7zip
7z a -tzip -r <nombre-del-proyecto>.zip .\requirements.txt .\application.py .\Procfile .\.env .\api .\core .\db .\libs .\queries .\schemas .\.ebextensions
```

## Push - subrir al repo
```bash
git checkout <rama-a-subir>
git push <nombre-remoto> <rama-local>:<rama-remota>
```

### Ejemplo:
```bash
git checkout Kevin
git push origin Kevin:Kevin
```

## Pull - traer del repo
```bash
git checkout <rama-local-donde-quedaran-los-cambios>
git pull <nombre-remoto> <rama-remota>
```

### Ejemplo:
```bash
git checkout Kevin
git push origin Kevin
```