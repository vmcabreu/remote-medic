<script>
import { ref, computed, onMounted } from "vue";
import { patientService } from "@/services/patientService";
import { useAuthStore } from "@/stores/auth.store";
import { useRouter } from "vue-router";

export default {
  name: "PatientTable",
  props: {
    showAssigned: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const patients = ref([]);
    const currentPage = ref(1);
    const router = useRouter();
    const itemsPerPage = ref(10);
    const userStore = useAuthStore();
    const currentUserId = ref(null);

    const showAssignModal = ref(false);
    const unassignedPatients = ref([]);
    const searchPatients = ref('');
    const selectedPatients = ref(new Set());
    const tableTitle = computed(() =>
      props.showAssigned ? 'Mis Pacientes' : 'Pacientes Sin Asignar'
    );
    const loadCurrentUser = async () => {
      try {
        const user = await userStore.getUser();
        currentUserId.value = Number(user?.id) || user;
      } catch (err) {
        console.error("Error cargando usuario:", err);
      }
    };

    const fetchPatients = async () => {
      try {
        if (props.showAssigned) {
          if (!currentUserId.value) {
            patients.value = [];
            return;
          }
          const response = await patientService.getPatientByUserId(currentUserId.value);
          patients.value = response.patients || response || [];
        } else {
          const response = await patientService.getUnassignedPatients();
          patients.value = response.patients || response || [];
        }
      } catch (err) {
        console.error("Error al cargar pacientes:", err);
        patients.value = [];
      }
    };

    const fetchUnassignedPatients = async () => {
      try {
        const response = await patientService.getUnassignedPatients();
        unassignedPatients.value = response.patients || response || [];
        selectedPatients.value.clear();
      } catch (err) {
        console.error("Error al cargar pacientes no asignados:", err);
        unassignedPatients.value = [];
      }
    };

    const openAssignModal = async () => {
      showAssignModal.value = true;
      await fetchUnassignedPatients();
    };

    const closeAssignModal = () => {
      showAssignModal.value = false;
      searchPatients.value = '';
      selectedPatients.value.clear();
    };

    const isPatientSelected = (patientId) => selectedPatients.value.has(patientId);

    const togglePatient = (patient) => {
      if (isPatientSelected(patient.id)) {
        selectedPatients.value.delete(patient.id);
      } else {
        selectedPatients.value.add(patient.id);
      }
    };

    const selectedCount = computed(() => selectedPatients.value.size);

    const savePatientAssignments = async () => {
      if (!currentUserId.value) {
        alert('Error: Usuario no identificado');
        return;
      }

      try {
        const selectedIds = Array.from(selectedPatients.value);
        for (const patientId of selectedIds) {
          await patientService.assignPatientToUser(patientId, currentUserId.value);
        }

        closeAssignModal();
        await fetchPatients();
      } catch (err) {
        console.error("Error al asignar pacientes:", err);
        alert('Error al asignar pacientes');
      }
    };

    const goToPatientDetails = (id) => router.push(`/patients/${id}`);

    const formatDate = (dateStr) => {
      if (!dateStr) return 'N/A';
      const date = new Date(dateStr);
      return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    };

    const totalPages = computed(() =>
      Math.ceil(patients.value.length / itemsPerPage.value)
    );

    const paginatedPatients = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage.value;
      return patients.value.slice(start, start + itemsPerPage.value);
    });

    const nextPage = () => {
      if (currentPage.value < totalPages.value) currentPage.value++;
    };

    const prevPage = () => {
      if (currentPage.value > 1) currentPage.value--;
    };

    const releasePatient = async (patientId) => {
      const confirmRelease = confirm('¿Deseas liberar este paciente?');
      if (!confirmRelease) return;
      try {
        await patientService.removeAssignedPatient(patientId);
        await fetchPatients();
      } catch (err) {
        console.error("Error al liberar paciente:", err);
        alert('Error al liberar paciente');
      }
    };

    onMounted(async () => {
      await loadCurrentUser();
      await fetchPatients();
    });

    return {
      patients,
      paginatedPatients,
      currentPage,
      totalPages,
      itemsPerPage,
      currentUserId,
      loadCurrentUser,
      nextPage,
      prevPage,
      formatDate,
      goToPatientDetails,
      showAssignModal,
      unassignedPatients,
      searchPatients,
      selectedPatients,
      selectedCount,
      isPatientSelected,
      togglePatient,
      openAssignModal,
      closeAssignModal,
      savePatientAssignments,
      releasePatient,
      tableTitle
    };
  },
};
</script>

<template>
  <div class="patient-table-container">
    <div class="table-header">
      <h2 class="table-title">{{ tableTitle }}</h2>
      <div class="table-actions">
        <button class="action-btn assign-btn" @click="openAssignModal">
          Asignar pacientes
        </button>
      </div>
    </div>

    <div class="table-wrapper">
      <table class="patient-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Apellido</th>
            <th>Teléfono</th>
            <th>Instrucciones</th>
            <th>Fecha</th>
            <th v-if="showAssigned">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="patient in paginatedPatients" :key="patient.id" class="hover-table"
            @dblclick="goToPatientDetails(patient.id)">
            <td>{{ patient.id }}</td>
            <td>{{ patient.name }}</td>
            <td>{{ patient.surname }}</td>
            <td>{{ patient.phone || 'N/A' }}</td>
            <td>{{ patient.instructions || '-' }}</td>
            <td>{{ formatDate(patient.created_at) }}</td>
            <td v-if="showAssigned">
              <button class="action-btn release-btn small" @click.stop="releasePatient(patient.id)">
                Liberar
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pagination">
      <button class="page-btn" :disabled="currentPage === 1" @click="prevPage">
        ⬅ Anterior
      </button>
      <span class="page-info">
        Página {{ currentPage }} / {{ totalPages }}
      </span>
      <button class="page-btn" :disabled="currentPage === totalPages" @click="nextPage">
        Siguiente ➡
      </button>
    </div>

    <div v-if="showAssignModal" class="modal-overlay" @click="closeAssignModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Asignar Pacientes</h3>
          <button class="modal-close" @click="closeAssignModal">
            <i class="core-icon cross-circle small-icon"></i>
          </button>
        </div>

        <div class="modal-search">
          <input v-model="searchPatients" placeholder="Buscar pacientes disponibles..." class="search-input">
        </div>

        <div class="modal-patients">
          <div v-if="unassignedPatients.filter(p =>
            p.name.toLowerCase().includes(searchPatients.toLowerCase()) ||
            p.surname.toLowerCase().includes(searchPatients.toLowerCase())
          ).length === 0" class="empty-state">
            No hay pacientes disponibles
          </div>

          <div v-else class="patients-list">
            <div v-for="patient in unassignedPatients.filter(p =>
              p.name.toLowerCase().includes(searchPatients.toLowerCase()) ||
              p.surname.toLowerCase().includes(searchPatients.toLowerCase())
            )" :key="patient.id" class="patient-item" :class="{ 'selected': isPatientSelected(patient.id) }">
              <div class="patient-info">
                <h4>{{ patient.name }} {{ patient.surname }}</h4>
                <span class="patient-id">#{{ patient.id }}</span>
                <span v-if="patient.phone" class="patient-phone">{{ patient.phone }}</span>
              </div>

              <button class="toggle-assign-btn" @click="togglePatient(patient)">
                {{ isPatientSelected(patient.id) ? '✓ Seleccionado' : 'Asignar' }}
              </button>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="action-btn secondary" @click="closeAssignModal">
            Cancelar
          </button>
          <button class="action-btn primary" @click="savePatientAssignments" :disabled="selectedCount === 0">
            Guardar {{ selectedCount }} seleccionados
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.hover-table:hover {
  cursor: pointer;
}

.patient-table-container {
  background: #1a1e23;
  padding: 20px;
  border-radius: 8px;
  color: #cfd3dc;
  font-family: Inter, sans-serif;
}

.table-title {
  font-size: 1.4rem;
  margin-bottom: 20px;
  color: #fff;
  font-weight: 600;
  border-left: 4px solid #38aa77;
  padding-left: 10px;
  display: flex;
}

.table-wrapper {
  overflow-x: auto;
  background: #111418;
  border-radius: 8px;
  border: 1px solid #222;
}

.patient-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 800px;
}

.patient-table th {
  background: #1f252d;
  padding: 14px 16px;
  font-size: 0.9rem;
  color: #38aa77;
  font-weight: 600;
  border-bottom: 1px solid #222;
  letter-spacing: 0.05em;
}

.patient-table td {
  padding: 14px 16px;
  border-bottom: 1px solid #222;
  color: #cfd3dc;
  font-size: 0.9rem;
}

.patient-table tr:nth-child(even) {
  background-color: #181c21;
}

.patient-table tr:hover {
  background-color: #232a33;
  transition: background 0.2s ease;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 15px;
  gap: 15px;
}

.page-btn {
  background: #111418;
  color: #38aa77;
  border: 1px solid #38aa77;
  padding: 8px 14px;
  border-radius: 5px;
  cursor: pointer;
  transition: 0.25s;
}

.page-btn:hover:enabled {
  background: #38aa77;
  color: white;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 0.9rem;
  color: #cfd3dc;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.65);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal-content {
  background: #1a1e23;
  padding: 20px;
  border-radius: 8px;
  color: #cfd3dc;
  width: 300px;
  text-align: center;
}

.modal-item {
  cursor: pointer;
  padding: 10px;
  border-bottom: 1px solid #333;
}

.modal-item:hover {
  background-color: #232a33;
}

@media (max-width: 768px) {

  .patient-table th,
  .patient-table td {
    font-size: 0.85rem;
    padding: 10px;
  }

  .pagination {
    flex-direction: column;
    gap: 10px;
  }
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.table-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  background: #111418;
  color: #38aa77;
  border: 1px solid #38aa77;
  padding: 8px 14px;
  border-radius: 5px;
  cursor: pointer;
  transition: 0.25s;
}

.action-btn:hover {
  background: #38aa77;
  color: white;
}


.assign-btn {
  border-color: #38aa77;
}

.release-btn {
  border-color: #dc3545;
  color: #dc3545;

  &:disabled {
    border-color: #686868;
    color: #686868;
  }
}

.release-btn:hover {
  background: #dc3545;
  color: white;
}

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
  max-width: 700px;
  max-height: 80vh;
  overflow: hidden;
  border: 1px solid #38aa77;
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
  font-size: 1.3rem;
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
  padding: 20px 24px;
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
}

.modal-patients {
  max-height: 400px;
  overflow-y: auto;
}

.patients-list {
  padding: 24px;
}

.patient-item {
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

.patient-item:hover {
  border-color: #38aa77;
}

.patient-item.selected {
  border-color: #51f7ac;
  background: rgba(81, 247, 172, 0.1);
}

.patient-info {
  flex: 1;
}

.patient-info h4 {
  color: #fff;
  margin: 0 0 4px 0;
  font-size: 1.1rem;
}

.patient-id,
.patient-phone {
  color: #9ca3af;
  font-size: 0.85rem;
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
}

.modal-footer {
  display: flex;
  gap: 12px;
  padding: 24px;
  border-top: 1px solid #222;
  justify-content: flex-end;
}

.action-btn.primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Scrollbar */
.modal-patients::-webkit-scrollbar {
  width: 8px;
}

.modal-patients::-webkit-scrollbar-track {
  background: #1a1e23;
}

.modal-patients::-webkit-scrollbar-thumb {
  background: #38aa77;
  border-radius: 4px;
}
</style>
