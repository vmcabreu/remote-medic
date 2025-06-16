export class Patient {
  constructor(data = {}) {
    this.id = data.id || null
    this.name = data.name || ''
    this.email = data.email || ''
    this.phone = data.phone || ''
    this.created_at = data.created_at || null
    this.updated_at = data.updated_at || null
    
    // Campos adicionales si los necesitas
    this.age = data.age || null
    this.address = data.address || ''
    this.medical_notes = data.medical_notes || ''
    this.assigned_users = data.assigned_users || []
  }

  // Método para validar los datos del paciente
  validate() {
    const errors = []
    
    if (!this.name || this.name.trim().length === 0) {
      errors.push('El nombre es requerido')
    }
    
    if (this.name && this.name.length > 100) {
      errors.push('El nombre no puede exceder 100 caracteres')
    }
    
    if (this.email && !this.isValidEmail(this.email)) {
      errors.push('El email no tiene un formato válido')
    }
    
    if (this.phone && !this.isValidPhone(this.phone)) {
      errors.push('El teléfono no tiene un formato válido')
    }
    
    return {
      isValid: errors.length === 0,
      errors
    }
  }

  // Validaciones auxiliares
  isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  }

  isValidPhone(phone) {
    const phoneRegex = /^[\+]?[\d\s\-\(\)]{10,}$/
    return phoneRegex.test(phone)
  }

  // Convertir a objeto plano para enviar al backend
  toJSON() {
    return {
      id: this.id,
      name: this.name,
      email: this.email,
      phone: this.phone,
      age: this.age,
      address: this.address,
      medical_notes: this.medical_notes
    }
  }

  // Método para enviar solo los campos necesarios para crear
  toCreatePayload() {
    const payload = {
      name: this.name,
      email: this.email,
      phone: this.phone
    }
    
    // Solo agregar campos opcionales si tienen valor
    if (this.age) payload.age = this.age
    if (this.address) payload.address = this.address
    if (this.medical_notes) payload.medical_notes = this.medical_notes
    
    return payload
  }

  // Método para actualizar desde respuesta del backend
  updateFromResponse(data) {
    this.id = data.id
    this.name = data.name
    this.email = data.email
    this.phone = data.phone
    this.created_at = data.created_at
    this.updated_at = data.updated_at
    
    if (data.age) this.age = data.age
    if (data.address) this.address = data.address
    if (data.medical_notes) this.medical_notes = data.medical_notes
    if (data.assigned_users) this.assigned_users = data.assigned_users
  }

  // Método estático para crear desde respuesta del backend
  static fromBackend(data) {
    return new Patient(data)
  }

  // Método para clonar el paciente
  clone() {
    return new Patient(this.toJSON())
  }

  // Método para formatear fecha de creación
  getFormattedCreatedDate() {
    if (!this.created_at) return 'N/A'
    return new Date(this.created_at).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }

  // Método para obtener iniciales del nombre
  getInitials() {
    return this.name
      .split(' ')
      .map(word => word[0])
      .join('')
      .toUpperCase()
      .substring(0, 2)
  }
}