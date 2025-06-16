export class User {
  constructor(data = {}) {
    this.id = data.id || "";
    this.username = data.username || "";
    this.email = data.email || "";
    this.first_name = data.first_name || "";
    this.last_name = data.last_name || "";
    this.is_active = data.is_active || false;
    this.is_admin = data.is_admin || false;
    this.last_login = data.last_login || "";
    this.created_at = data.created_at || "";
    this.updated_at = data.updated_at || "";
  }

  // Método para validar los datos del paciente
  validate() {
    const errors = [];

    if (!this.name || this.name.trim().length === 0) {
      errors.push("El nombre es requerido");
    }

    if (this.name && this.name.length > 100) {
      errors.push("El nombre no puede exceder 100 caracteres");
    }

    if (this.email && !this.isValidEmail(this.email)) {
      errors.push("El email no tiene un formato válido");
    }
    return {
      isValid: errors.length === 0,
      errors,
    };
  }

  // Validaciones auxiliares
  isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }



  // Convertir a objeto plano para enviar al backend
  toJSON() {
    return {
      id: this.id,
      username: this.username,
      email: this.email,
      first_name: this.first_name,
      last_name: this.last_name,
      is_active: this.is_active,
      is_admin: this.is_admin,
      last_login: this.last_login,
      created_at: this.created_at,
      updated_at: this.updated_at,
    };
  }

  // Método para enviar solo los campos necesarios para crear
  toCreatePayload() {
    const payload = {
      username: this.username,
      email: this.email,
      first_name: this.first_name,
      last_name: this.last_name,
      is_active: this.is_active,
      is_admin: this.is_admin,
    };

    // Solo agregar campos opcionales si tienen valor
    if (this.username) payload.username = this.username;
    if (this.email) payload.email = this.email;
    if (this.first_name) payload.first_name = this.first_name;
    if (this.last_name) payload.last_name = this.last_name;
    if (this.is_active) payload.is_active = this.is_active;
    if (this.is_admin) payload.is_admin = this.is_admin;

    return payload;
  }

  // Método para actualizar desde respuesta del backend
  updateFromResponse(data) {
    this.id = data.id;
    this.name = data.name;
    this.email = data.email;
    this.phone = data.phone;
    this.created_at = data.created_at;
    this.updated_at = data.updated_at;

    if (data.age) this.age = data.age;
    if (data.address) this.address = data.address;
    if (data.medical_notes) this.medical_notes = data.medical_notes;
    if (data.assigned_users) this.assigned_users = data.assigned_users;
  }

  // Método estático para crear desde respuesta del backend
  static fromBackend(data) {
    return new User(data);
  }

  // Método para clonar el paciente
  clone() {
    return new User(this.toJSON());
  }

  // Método para formatear fecha de creación
  getFormattedCreatedDate() {
    if (!this.created_at) return "N/A";
    return new Date(this.created_at).toLocaleDateString("es-ES", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  }

  // Método para obtener iniciales del nombre
  getInitials() {
    return this.name
      .split(" ")
      .map((word) => word[0])
      .join("")
      .toUpperCase()
      .substring(0, 2);
  }
}
