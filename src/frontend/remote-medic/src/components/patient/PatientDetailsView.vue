<script>
import { ref, watch, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { patientService } from "@/services/patientService";
import { useAuthStore } from "@/stores/auth.store";
import medicineService from "@/services/medicineService";

export default {
  name: "PatientDetailsView",
  setup() {
    const route = useRoute();
    const router = useRouter();
    const patientId = ref(null);
    const patient = ref(null);
    const medicines = ref([]);
    const isLoading = ref(true);
    const medicineCount = ref(0);
    const patientError = ref(null);
    const medicinesError = ref(null);
    const userStore = useAuthStore();
    const editingInstructions = ref(false);
    const instructionsTemp = ref("");

    const showMedicinesModal = ref(false);
    const availableMedicines = ref([]);
    const searchMedicines = ref("");
    const selectedMedicines = ref(new Set());
    const localMedicines = ref([]);

    const medicineAssignments = ref({});

    const fetchPatientDetails = async () => {
      if (!patientId.value) {
        isLoading.value = false;
        return;
      }

      isLoading.value = true;
      patientError.value = null;
      medicinesError.value = null;
      patient.value = null;
      medicines.value = [];
      medicineCount.value = 0;
      localMedicines.value = [];

      try {
        const patientData = await patientService.getPatientById(
          patientId.value
        );
        patient.value = patientData.patient;
        instructionsTemp.value = patient.value.instructions || "";
      } catch (err) {
        console.error("Error fetching patient:", err);
        patientError.value =
          err.message || "Error al cargar datos del paciente";
      }

      try {
        const medicinesData = await medicineService.getPatientMedicines(
          patientId.value
        );
        medicines.value = medicinesData.medicines || medicinesData || [];
        localMedicines.value = [...medicines.value];
        medicineCount.value = medicines.value.length;
      } catch (err) {
        console.error("Error fetching medicines:", err);
        medicinesError.value = err.message || "Error al cargar medicamentos";
        medicines.value = [];
        medicineCount.value = 0;
      }

      isLoading.value = false;
    };

    const saveInstructions = async () => {
      try {
        await patientService.updatePatient(patientId.value, {
          instructions: instructionsTemp.value,
        });
        patient.value.instructions = instructionsTemp.value;
        editingInstructions.value = false;
      } catch (err) {
        console.error("Error saving instructions:", err);
        alert("Error al guardar instrucciones");
      }
    };

    const cancelInstructions = () => {
      instructionsTemp.value = patient.value.instructions || "";
      editingInstructions.value = false;
    };

    const filteredAvailableMedicines = computed(() => {
      return availableMedicines.value.filter((medicine) =>
        medicine?.name
          ?.toLowerCase()
          .includes(searchMedicines.value.toLowerCase())
      );
    });

    const selectedCount = computed(() => selectedMedicines.value.size);

    const openMedicinesModal = async () => {
      try {
        const adminFlag = userStore.user.is_admin;
        const activeOnly = !adminFlag;
        const allMedicines = await medicineService.getAllMedicines(
          null,
          null,
          activeOnly,
          true
        );
        availableMedicines.value = allMedicines.medicines || [];

        selectedMedicines.value.clear();
        medicineAssignments.value = {};

        localMedicines.value.forEach((m) => {
          if (m?.id) {
            selectedMedicines.value.add(m.id);
            medicineAssignments.value[m.id] = {
              dose_per_take: m.dosage || m.dose_per_take || "",
              notes: m.notes || m.instructions || "",
            };
          }
        });

        availableMedicines.value.forEach((m) => {
          if (m?.id && !medicineAssignments.value[m.id]) {
            medicineAssignments.value[m.id] = {
              dose_per_take: "",
              notes: "",
            };
          }
        });

        showMedicinesModal.value = true;
      } catch (err) {
        console.error("Error loading medicines:", err);
        alert("Error al cargar medicamentos disponibles");
      }
    };

    const closeMedicinesModal = () => {
      showMedicinesModal.value = false;
      searchMedicines.value = "";
    };

    const isAssigned = (medicineId) => {
      return selectedMedicines.value.has(medicineId);
    };

    const toggleAssignMedicine = (medicine) => {
      if (!medicine?.id) return;

      if (isAssigned(medicine.id)) {
        selectedMedicines.value.delete(medicine.id);
      } else {
        selectedMedicines.value.add(medicine.id);
        if (!medicineAssignments.value[medicine.id]) {
          medicineAssignments.value[medicine.id] = {
            dose_per_take: "",
            notes: "",
          };
        }
      }
    };

    const saveAssignedMedicines = async () => {
      try {
        const currentIds = new Set(localMedicines.value.map((m) => m.id));
        const selectedIds = Array.from(selectedMedicines.value);

        const toRemove = Array.from(currentIds).filter(
          (id) => !selectedIds.includes(id)
        );
        if (toRemove.length > 0) {
          await patientService.removePatientMedicines(
            patientId.value,
            toRemove
          );
        }
        for (const medicineId of selectedIds) {
          const assignment = medicineAssignments.value[medicineId];
          if (!assignment) continue;

          const dose = assignment.dose_per_take || "1";
          const notes = assignment.notes || "";

          if (!currentIds.has(medicineId)) {
            await medicineService.assignMedicineToPatient(
              patientId.value,
              medicineId,
              dose,
              ""
            );
          } else {
            (await medicineService.updatePatientMedicineDose?.(
              patientId.value,
              medicineId,
              dose,
              notes
            )) ||
              medicineService.assignMedicineToPatient(
                patientId.value,
                medicineId,
                dose,
                notes
              );
          }
        }

        const medicinesData = await medicineService.getPatientMedicines(
          patientId.value
        );
        localMedicines.value = medicinesData.medicines || [];
        medicines.value = [...localMedicines.value];
        medicineCount.value = localMedicines.value.length;

        closeMedicinesModal();
      } catch (err) {
        console.error("Error saving medicines:", err);
        alert("Error al guardar medicamentos");
      }
    };

    const clearAllMedicines = async () => {
      if (confirm("¿Eliminar todos los medicamentos del paciente?")) {
        try {
          await patientService.updatePatientMedicines(patientId.value, []);
          localMedicines.value = [];
          medicines.value = [];
          medicineCount.value = 0;
        } catch (err) {
          console.error("Error clearing medicines:", err);
          alert("Error al limpiar medicamentos");
        }
      }
    };

    watch(
      () => route.params.id,
      async (newId) => {
        if (newId) {
          patientId.value = newId;
          await fetchPatientDetails();
        }
      },
      { immediate: true }
    );

    const formatDate = (dateStr) => {
      if (!dateStr) return "No disponible";
      try {
        return new Date(dateStr).toLocaleDateString("es-ES", {
          year: "numeric",
          month: "long",
          day: "numeric",
          hour: "2-digit",
          minute: "2-digit",
        });
      } catch (e) {
        return "Fecha inválida";
      }
    };

    const getFrequencyText = (medicine) => {
      if (medicine?.frequency_hours) return `Cada ${medicine.frequency_hours}h`;
      if (medicine?.frequency_days) return `Cada ${medicine.frequency_days}d`;
      return "Según indicación";
    };

    const goBack = () => {
      router.push("/");
    };

    return {
      patientId,
      patient,
      medicines,
      isLoading,
      medicineCount,
      patientError,
      medicinesError,
      userStore,
      editingInstructions,
      instructionsTemp,
      showMedicinesModal,
      availableMedicines,
      searchMedicines,
      selectedMedicines,
      localMedicines,
      medicineAssignments,
      filteredAvailableMedicines,
      selectedCount,
      formatDate,
      getFrequencyText,
      goBack,
      saveInstructions,
      cancelInstructions,
      openMedicinesModal,
      closeMedicinesModal,
      isAssigned,
      toggleAssignMedicine,
      saveAssignedMedicines,
      clearAllMedicines,
    };
  },
};
</script>

<template>
  <div class="patient-details-wrapper">
    <div v-if="isLoading" class="loading-state">
      <div class="spinner"></div>
      <span>Cargando detalles del paciente...</span>
    </div>

    <div v-else-if="!patient && patientError" class="error-state">
      <h2>
        <i class="core-icon triangle-warning big-icon"></i> Error al cargar
        paciente
      </h2>
      <p>{{ patientError }}</p>
      <button class="action-btn primary" @click="goBack">
        Volver al Dashboard
      </button>
    </div>

    <div v-else-if="patient" class="patient-details-container">
      <div v-if="medicinesError" class="alert-warning warning-message">
        <span class="alert-icon">
          <i class="core-icon triangle-warning big-icon"></i>
        </span>
        <div>
          <strong>Advertencia:</strong> No se pudieron cargar los medicamentos
          del paciente.
          <br />
          <small>{{ medicinesError }}</small>
        </div>
      </div>

        <button class="action-btn secondary" @click="goBack">
          ← Volver al Dashboard
        </button>
      <div class="patient-hero">
        <div class="patient-avatar">
          <i class="core-icon user-avatar big-icon"></i>
        </div>
        <div class="patient-info">
          <h1 class="patient-fullname">
            {{ patient.name }} {{ patient.surname }}
          </h1>
          <div class="patient-meta">
            <span class="meta-item">
              <i class="core-icon square-phone small-icon icon-color-green"></i>{{ patient.phone || "No disponible" }}
            </span>
            <span class="meta-item">
              <i class="core-icon calendar-clock small-icon icon-color-green"></i>
              Fecha de ingreso: {{ formatDate(patient.created_at) }}
            </span>
          </div>
        </div>
      </div>

      <div class="stats-grid">
        <div class="stat-card primary">
          <div class="stat-number">{{ medicineCount }}</div>
          <div class="stat-label">Medicamentos</div>
        </div>
        <div class="stat-card secondary">
          <div class="stat-number">Activo</div>
          <div class="stat-label">Estado</div>
        </div>
      </div>

      <div class="info-section">
        <div class="section-header">
          <h3 class="section-title">
            <i class="core-icon stethoscope big-icon icon-color-green"></i>
            Instrucciones Médicas
          </h3>
          <div class="edit-controls">
            <button v-if="!editingInstructions" class="action-btn small" @click="editingInstructions = true">
              <i class="core-icon file-edit small-icon icon-color-green"></i>
              <span>Editar</span>
            </button>
            <button v-else class="action-btn primary small" @click="saveInstructions">
              <i class="core-icon check-circle small-icon icon-color-green"></i>
              <span>Guardar</span>
            </button>
            <button v-if="editingInstructions" class="action-btn secondary small" @click="cancelInstructions">
              <i class="core-icon delete small-icon icon-color-green"></i>
              <span>Cancelar</span>
            </button>
          </div>
        </div>

        <div class="instructions-content">
          <textarea v-if="editingInstructions" v-model="instructionsTemp" class="instructions-textarea"
            placeholder="Escribe las instrucciones médicas..."></textarea>
          <div v-else-if="patient.instructions" class="instructions-text">
            {{ patient.instructions }}
          </div>
          <div v-else class="instructions-empty">
            No hay instrucciones médicas
          </div>
        </div>
      </div>

      <div class="medicines-section">
        <div class="section-header">
          <h3 class="section-title">
            <i class="core-icon pills big-icon icon-color-green"></i>
            Medicamentos Asignados ({{ medicineCount }})
          </h3>
          <div class="edit-controls">
            <button class="action-btn primary" @click="openMedicinesModal">
              <i class="core-icon pills small-icon icon-color-green"></i>
              <span>Gestionar Medicamentos</span>
            </button>
            <button class="action-btn secondary" v-if="localMedicines.length > 0" @click="clearAllMedicines">
              <i class="core-icon delete small-icon"></i>
              <span>Limpiar Todos</span>
            </button>
          </div>
        </div>

        <div v-if="localMedicines.length > 0" class="medicines-grid">
          <div v-for="medicine in localMedicines" :key="medicine.id" class="medicine-card">
            <div class="medicine-header">
              <h4 class="medicine-name">{{ medicine.name }}</h4>
              <span class="medicine-dosage">{{
                medicine.dosage || medicine.dose_per_take || "N/A"
              }}</span>
            </div>
            <div class="medicine-frequency">
              {{ getFrequencyText(medicine) }}
            </div>
            <div v-if="medicine.instructions || medicine.notes" class="medicine-instructions">
              {{ medicine.instructions || medicine.notes }}
            </div>
            <div v-if="medicine.notes" class="medicine-instructions">
              Notas: {{ medicine.notes }}
            </div>
            <div class="medicine-dates">
              <span v-if="medicine.start_date">Inicio: {{ formatDate(medicine.start_date) }}</span>
              <span v-if="medicine.end_date">Fin: {{ formatDate(medicine.end_date) }}</span>
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          <i class="core-icon medication big-icon"></i>
          <p>
            {{
              medicinesError
                ? "No se pudieron cargar los medicamentos"
                : "No hay medicamentos asignados"
            }}
          </p>
        </div>
      </div>
    </div>

    <div v-else class="error-state">
      <h2>Paciente no encontrado</h2>
      <p>No se pudo encontrar el paciente con ID: {{ patientId }}</p>
      <button class="action-btn primary" @click="goBack">
        Volver al Dashboard
      </button>
    </div>

    <div v-if="showMedicinesModal" class="modal-overlay" @click="closeMedicinesModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Gestionar Medicamentos</h3>
          <button class="modal-close" @click="closeMedicinesModal">
            <i class="core-icon cross-circle small-icon"></i>
          </button>
        </div>

        <div class="modal-search">
          <input v-model="searchMedicines" placeholder="Buscar medicamentos..." class="search-input" />
        </div>

        <div class="modal-medicines">
          <div v-if="filteredAvailableMedicines.length === 0" class="empty-state">
            No hay medicamentos disponibles
          </div>

          <div v-else class="medicines-list">
            <div v-for="medicine in filteredAvailableMedicines" :key="medicine.id" class="medicine-item"
              :class="{ selected: isAssigned(medicine.id) }">
              <div class="medicine-info">
                <h4>{{ medicine.name || "Sin nombre" }}</h4>
                <span v-if="medicine.dosage" class="medicine-dosage">
                  {{ medicine.dosage }}
                </span>
              </div>

              <button class="toggle-assign-btn" @click="toggleAssignMedicine(medicine)">
                {{ isAssigned(medicine.id) ? "Editando ✓" : "Asignar" }}
              </button>

              <div v-if="isAssigned(medicine.id)" class="medicine-form">
                <input :value="medicineAssignments[medicine.id]?.dose_per_take || ''" @input="
                  medicineAssignments[medicine.id] = {
                    ...medicineAssignments[medicine.id],
                    dose_per_take: $event.target.value,
                  }
                  " placeholder="Dosis (ej: 1 tableta)" class="form-input small" />

                <textarea :value="medicineAssignments[medicine.id]?.notes || ''" @input="
                  medicineAssignments[medicine.id] = {
                    ...medicineAssignments[medicine.id],
                    notes: $event.target.value,
                  }
                  " placeholder="Notas (opcional)" class="form-input notes" rows="2"></textarea>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="action-btn secondary" @click="closeMedicinesModal">
            Cancelar
          </button>
          <button class="action-btn primary" @click="saveAssignedMedicines">
            Guardar {{ selectedCount }} seleccionados
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.medicine-form {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #2a2f36;
}

.form-input {
  width: 100%;
  background: #111418;
  border: 1px solid #38aa77;
  border-radius: 6px;
  color: #fff;
  padding: 8px 12px;
  font-size: 0.9rem;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #51f7ac;
  box-shadow: 0 0 0 2px rgba(81, 247, 172, 0.2);
}

.form-input.small {
  padding: 6px 10px;
  font-size: 0.85rem;
}

.form-input.notes {
  resize: vertical;
  min-height: 50px;
}

.patient-details-wrapper {
  min-height: 100vh;
  background: #0d1117;
  padding: 20px;
}

.patient-details-container {
  background: #1a1e23;
  padding: 30px;
  border-radius: 12px;
  color: #cfd3dc;
  font-family: Inter, sans-serif;
  max-width: 1400px;
  margin: 0 auto;
}

.alert-warning {
  background: rgba(245, 158, 11, 0.1);
  border: 1px solid rgba(245, 158, 11, 0.3);
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 24px;
  display: flex;
  gap: 12px;
  align-items: flex-start;
  color: #fbbf24;
}

.alert-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.alert-warning strong {
  color: #fbbf24;
}

.alert-warning small {
  color: #d1a84f;
  font-size: 0.85rem;
}

.patient-hero {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 30px;
  padding: 24px;
  background: linear-gradient(135deg, #111418 0%, #1a1e23 100%);
  border-radius: 16px;
  border: 1px solid #222;
}

.icon-color-green {
  background-color: #38aa77;
}

.patient-avatar {
  width: 90px;
  height: 90px;
  background: linear-gradient(135deg, #38aa77, #51f7ac);
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.8rem;
  box-shadow: 0 12px 30px rgba(56, 170, 119, 0.3);
}

.warning-message {
  display: flex;
  justify-content: center;
  align-items: center;

  i {
    background-color: #fbbf24;
  }
}

.patient-fullname {
  color: #fff;
  font-size: 2.2rem;
  margin: 0 0 8px 0;
  font-weight: 700;
  display: flex;
}

.patient-meta {
  display: flex;
  gap: 20px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #38aa77;
  font-weight: 500;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: #111418;
  padding: 24px;
  border-radius: 12px;
  text-align: center;
  border: 1px solid #222;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 4px;
}

.stat-label {
  color: #38aa77;
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.info-section,
.medicines-section {
  background: #111418;
  border-radius: 12px;
  border: 1px solid #222;
  margin-bottom: 24px;
  overflow: hidden;
}

.section-title {
  color: #fff;
  font-size: 1.3rem;
  margin: 0;
  padding: 20px 24px;
  background: #1f252d;
  border-bottom: 1px solid #222;
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 600;
}

.section-header {
  display: flex;
  justify-content: flex-end;  
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.instructions-content {
  padding: 24px;
  color: #cfd3dc;
  line-height: 1.6;
}

.medicines-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
  padding: 24px;
}

.medicine-card {
  background: #1a1e23;
  border: 1px solid #2a2f36;
  border-radius: 10px;
  padding: 20px;
  transition: all 0.2s;
}

.medicine-card:hover {
  border-color: #38aa77;
  box-shadow: 0 8px 25px rgba(56, 170, 119, 0.15);
}

.medicine-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  gap: 12px;
}

.medicine-name {
  color: #fff;
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
  flex: 1;
}

.medicine-dosage {
  background: #38aa77;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  white-space: nowrap;
}

.medicine-frequency {
  color: #38aa77;
  font-weight: 500;
  margin-bottom: 8px;
}

.medicine-instructions {
  color: #9ca3af;
  font-size: 0.9rem;
  margin-bottom: 12px;
  line-height: 1.5;
}

.medicine-dates {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 0.85rem;
  color: #6b7280;
}

.action-btn {
  background: transparent;
  color: #38aa77;
  border: 1px solid #38aa77;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s;
  font-size: 0.95rem;
  display: flex;
  justify-content: center;
  align-items: flex-end;
  gap: 10px;

  i {
    background-color: #38aa77 !important;
  }
}

.action-btn:hover {
  background: #38aa77;
  color: white;
  transform: translateY(-2px);

  i {
    background-color: white !important;
  }
}

.action-btn.secondary {
  color: #6b7280;
  border-color: #6b7280;

  i {
    background-color: #6b7280 !important;
  }
}

.action-btn.secondary:hover {
  background: #6b7280;
  color: white;

  i {
    background-color: white !important;
  }
}

.empty-state {
  text-align: center;
  padding: 60px 24px;
  color: #9ca3af;

  i {
    background-color: #9ca3af;
  }
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state p {
  margin-bottom: 20px;
  font-size: 1.1rem;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  color: #cfd3dc;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #222;
  border-top: 4px solid #38aa77;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  min-height: 60vh;
  color: #9ca3af;
  padding: 40px;
}

.error-state h2 {
  color: #fff;
  margin-bottom: 16px;
  font-size: 2rem;
}

.error-state p {
  margin-bottom: 24px;
  font-size: 1.1rem;
}

.actions-footer {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #222;
  display: flex;
  justify-content: center;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .patient-hero {
    flex-direction: column;
    text-align: center;
  }

  .medicines-grid {
    grid-template-columns: 1fr;
  }

  .section-header {
    flex-direction: column;
    align-items: stretch;
  }

  .patient-details-container {
    padding: 20px;
  }

  .alert-warning {
    flex-direction: column;
  }
}

.edit-controls {
  display: flex;
  gap: 8px;
  align-items: center;
}

.action-btn.small {
  padding: 6px 12px;
  font-size: 0.85rem;
}

.instructions-textarea {
  width: 100%;
  min-height: 120px;
  background: #1a1e23;
  border: 1px solid #38aa77;
  border-radius: 8px;
  color: #fff;
  padding: 16px;
  font-family: inherit;
  font-size: 1rem;
  resize: vertical;
}

.instructions-textarea:focus {
  outline: none;
  border-color: #51f7ac;
  box-shadow: 0 0 0 3px rgba(56, 170, 119, 0.1);
}

.instructions-empty {
  color: #6b7280;
  font-style: italic;
  padding: 24px;
  text-align: center;
}

.delete-btn {
  background: #ef4444;
  color: white;
  padding: 4px 8px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.2s;
}

.delete-btn:hover {
  background: #dc2626;
  transform: scale(1.1);
}

css <style scoped>
/* ESTILOS EXISTENTES (mantener todos) + NUEVOS PARA MODAL */

.patient-details-wrapper {
  min-height: 100vh;
  background: #0d1117;
  padding: 20px;
}

.patient-details-container {
  background: #1a1e23;
  padding: 30px;
  border-radius: 12px;
  color: #cfd3dc;
  font-family: Inter, sans-serif;
  max-width: 1400px;
  margin: 0 auto;
}

/* ✅ NUEVOS ESTILOS PARA MODAL MEDICAMENTOS */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-content {
  background: #1a1e23;
  border-radius: 16px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow: hidden;
  border: 1px solid #38aa77;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  background: #1f252d;
  border-bottom: 1px solid #222;
}

.modal-header h3 {
  color: #fff;
  margin: 0;
  font-size: 1.4rem;
  font-weight: 600;
}

.modal-close {
  background: none;
  border: none;
  cursor: pointer;
  padding: 9px 9px;
  border-radius: 50%;
  transition: 0.25s;
  display: flex;
  justify-content: center;
  align-items: center;

  i {
    background-color: #ef4444;
  }
}

.modal-close:hover {
  background: #ef4444;
  color: white;

  i {
    background-color: white;
  }
}

.modal-search {
  padding: 24px;
  border-bottom: 1px solid #222;
}

.search-input {
  width: 100%;
  padding: 12px 16px;
  background: #111418;
  border: 1px solid #38aa77;
  border-radius: 8px;
  color: #fff;
  font-size: 1rem;
}

.search-input:focus {
  outline: none;
  border-color: #51f7ac;
  box-shadow: 0 0 0 3px rgba(56, 170, 119, 0.1);
}

.modal-medicines {
  max-height: 400px;
  overflow-y: auto;
  padding: 0;
}

.medicines-list {
  padding: 0 24px 24px;
}

.medicine-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: #111418;
  border: 1px solid #2a2f36;
  border-radius: 10px;
  margin-bottom: 12px;
  transition: all 0.2s;
  cursor: pointer;
}

.medicine-item:hover {
  border-color: #38aa77;
  background: #1a1e23;
}

.medicine-item.selected {
  border-color: #51f7ac;
  background: rgba(81, 247, 172, 0.1);
  box-shadow: 0 0 0 3px rgba(81, 247, 172, 0.2);
}

.medicine-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
}

.medicine-info h4 {
  color: #fff;
  margin: 0 0 4px 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.medicine-info .medicine-dosage {
  background: #38aa77;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.toggle-assign-btn {
  background: #38aa77;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9rem;
}

.toggle-assign-btn:hover {
  background: #51f7ac;
  transform: translateY(-1px);
}

.modal-footer {
  display: flex;
  gap: 12px;
  padding: 24px;
  border-top: 1px solid #222;
  justify-content: flex-end;
}

/* ✅ ESTILOS PARA INSTRUCCIONES (nuevos) */
.edit-controls {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}

.action-btn.small {
  padding: 6px 12px;
  font-size: 0.85rem;
}

.instructions-textarea {
  width: 100%;
  min-height: 120px;
  background: #1a1e23;
  border: 1px solid #38aa77;
  border-radius: 8px;
  color: #fff;
  padding: 16px;
  font-family: inherit;
  font-size: 1rem;
  resize: vertical;
  box-sizing: border-box;
}

.instructions-textarea:focus {
  outline: none;
  border-color: #51f7ac;
  box-shadow: 0 0 0 3px rgba(56, 170, 119, 0.1);
}

.instructions-text {
  padding: 24px;
  color: #cfd3dc;
  line-height: 1.6;
}

.instructions-empty {
  color: #6b7280;
  font-style: italic;
  padding: 60px 24px;
  text-align: center;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
  padding: 20px 24px;
  background: #1f252d;
  border-bottom: 1px solid #222;
}

/* Scrollbar personalizada para modal */
.modal-medicines::-webkit-scrollbar {
  width: 8px;
}

.modal-medicines::-webkit-scrollbar-track {
  background: #1a1e23;
}

.modal-medicines::-webkit-scrollbar-thumb {
  background: #38aa77;
  border-radius: 4px;
}

.modal-medicines::-webkit-scrollbar-thumb:hover {
  background: #51f7ac;
}
</style>
