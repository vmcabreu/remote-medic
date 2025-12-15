export class Medicine {
  constructor(data = {}) {
    this.id = data.id || "";
    this.name = data.name || "";
    this.dosage = data.dosage || "";
    this.description = data.description || "";
    this.instructions = data.instructions || "";
    this.frequency_hours = data.frequency_hours || null;
    this.frequency_days = data.frequency_days || null;
    this.start_date = data.start_date || "";
    this.end_date = data.end_date || "";
    this.is_active = data.is_active || true;
    this.created_at = data.created_at || "";
    this.updated_at = data.updated_at || "";
  }

  
  validate() {
    const errors = [];

    if (!this.name || this.name.trim().length === 0) {
      errors.push("El nombre del medicamento es requerido");
    }

    if (this.name && this.name.length > 100) {
      errors.push("El nombre no puede exceder 100 caracteres");
    }

    if (!this.dosage || this.dosage.trim().length === 0) {
      errors.push("La dosis es requerida");
    }

    if (this.dosage && this.dosage.length > 50) {
      errors.push("La dosis no puede exceder 50 caracteres");
    }

    if (this.frequency_hours !== null && (this.frequency_hours < 1 || this.frequency_hours > 24)) {
      errors.push("La frecuencia en horas debe estar entre 1 y 24");
    }

    if (this.frequency_days !== null && (this.frequency_days < 1 || this.frequency_days > 30)) {
      errors.push("La frecuencia en días debe estar entre 1 y 30");
    }

    if (this.start_date && new Date(this.start_date) > new Date()) {
      errors.push("La fecha de inicio no puede ser futura");
    }

    if (this.start_date && this.end_date && new Date(this.start_date) > new Date(this.end_date)) {
      errors.push("La fecha de inicio no puede ser posterior a la fecha de fin");
    }

    return {
      isValid: errors.length === 0,
      errors,
    };
  }

  
  toJSON() {
    return {
      id: this.id,
      name: this.name,
      dosage: this.dosage,
      description: this.description,
      instructions: this.instructions,
      frequency_hours: this.frequency_hours,
      frequency_days: this.frequency_days,
      start_date: this.start_date,
      end_date: this.end_date,
      is_active: this.is_active,
      created_at: this.created_at,
      updated_at: this.updated_at,
    };
  }

  
  toCreatePayload() {
    const payload = {
      name: this.name,
      dosage: this.dosage,
      description: this.description || "",
      instructions: this.instructions || "",
      frequency_hours: this.frequency_hours || null,
      frequency_days: this.frequency_days || null,
      start_date: this.start_date || null,
      end_date: this.end_date || null,
      is_active: this.is_active !== null ? this.is_active : true,
    };

    
    Object.keys(payload).forEach(key => {
      if (payload[key] === null || payload[key] === undefined || payload[key] === "") {
        delete payload[key];
      }
    });

    return payload;
  }

  
  updateFromResponse(data) {
    this.id = data.id || this.id;
    this.name = data.name || this.name;
    this.dosage = data.dosage || this.dosage;
    this.description = data.description || this.description;
    this.instructions = data.instructions || this.instructions;
    this.frequency_hours = data.frequency_hours || this.frequency_hours;
    this.frequency_days = data.frequency_days || this.frequency_days;
    this.start_date = data.start_date || this.start_date;
    this.end_date = data.end_date || this.end_date;
    this.is_active = data.is_active ?? this.is_active;
    this.created_at = data.created_at || this.created_at;
    this.updated_at = data.updated_at || this.updated_at;
  }

  
  static fromBackend(data) {
    return new Medicine(data);
  }

  
  clone() {
    return new Medicine(this.toJSON());
  }

  
  getFormattedStartDate() {
    if (!this.start_date) return "N/A";
    return new Date(this.start_date).toLocaleDateString("es-ES", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  }

  getFormattedEndDate() {
    if (!this.end_date) return "Indefinido";
    return new Date(this.end_date).toLocaleDateString("es-ES", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  }

  
  getFrequencyText() {
    if (this.frequency_hours) {
      return `Cada ${this.frequency_hours} horas`;
    }
    if (this.frequency_days) {
      return `Cada ${this.frequency_days} día${this.frequency_days > 1 ? 's' : ''}`;
    }
    return "Según indicación";
  }

  
  getStatusText() {
    return this.is_active ? "Activo" : "Inactivo";
  }

  getStatusColor() {
    return this.is_active ? "success" : "danger";
  }
}
