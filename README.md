---

```markdown
# 🏥 Sistema de Monitorización de Pacientes y Cuidadores

Este proyecto es una aplicación web diseñada para ayudar en el **seguimiento de pacientes o familiares enfermos**, permitiendo registrar información médica clave como medicamentos, dolencias e instrucciones de cuidado personalizado.

## 🧱 Tecnologías utilizadas

- **Frontend:** [Vue.js](https://vuejs.org/)  
- **Backend:** [Flask (Python)](https://flask.palletsprojects.com/)  
- **Base de Datos:** [PostgreSQL](https://www.postgresql.org/)
- **Contenedores:** [Docker](https://www.docker.com/) y [Docker Compose](https://docs.docker.com/compose/)

---

## 🚀 Funcionalidades principales

- 📋 Registro y gestión de pacientes
- 💊 Asignación de medicamentos con dosis y horarios
- 🤒 Registro de dolencias y condiciones médicas
- 📘 Instrucciones personalizadas de cuidado
- 🔐 Sistema básico de autenticación para cuidadores o familiares con JWT


---

## 📂 Estructura del proyecto

```
/frontend/          # Proyecto Vue.js
/backend/           # API REST con Flask
/docker-compose.yml # Orquestador de contenedores
README.md           # Documentación del proyecto
```

---

## ⚙️ Instalación y uso

### 🔧 Requisitos previos

- Node.js >= 18
- Python >= 3.10
- PostgreSQL >= 14
- Docker y Docker Compose
- `pip`, `virtualenv`, `pnpm` o `npm`

---

### ▶️ Frontend (Vue.js)

```bash
cd frontend
pnpm install         # o npm install
pnpm dev             # o npm run dev
```

---

### 🐍 Backend (Flask)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # en Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

---

### 🐳 Levantar el proyecto con Docker

```bash
docker-compose up --build
```

Esto iniciará los servicios de frontend (Vue), backend (Flask) y la base de datos (PostgreSQL).

> Asegúrate de tener configurados los `.env` correctamente antes de levantar los contenedores.

---


## 🔐 Variables de entorno

### backend/.env

```env
FLASK_ENV=development
DATABASE_URL=postgresql://usuario:contraseña@localhost/paciente_monitor
SECRET_KEY=supersecreto
```

### frontend/.env

```env
VITE_API_BASE_URL=http://localhost:5000/api
```

---

## 📌 Futuras mejoras

- Panel de notificaciones y alertas de medicación
- Calendario de seguimiento
- Versión móvil optimizada

---

## 📄 Licencia

Este proyecto está licenciado bajo la **MIT License**.
```

---
