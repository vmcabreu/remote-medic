<script>
import { ref, computed, onMounted } from "vue";
import medicineService from "@/services/medicineService";
import { useAuthStore } from "@/stores/auth.store";

export default {
  name: "MedicineTable",
  setup() {
    const medicines = ref([]);
    const pagination = ref({
      page: 1,
      pages: 1,
      per_page: 10,
      total: 0
    });
    const selectedMedicines = ref([]);
    const isLoading = ref(false);
    const userStore = useAuthStore();

    const fetchMedicines = async (page = 1) => {
      try {
        isLoading.value = true;
        const adminFlag = userStore.user.is_admin;
        const activeOnly = !adminFlag;
        const response = await medicineService.getAllMedicines(page, null, activeOnly);

        medicines.value = response.medicines || [];
        pagination.value = response.pagination || {
          page: 1,
          pages: 1,
          per_page: 10,
          total: 0
        };
      } catch (err) {
        console.error("Error al cargar medicinas:", err);
        medicines.value = [];
        pagination.value = { page: 1, pages: 0, per_page: 10, total: 0 };
      } finally {
        isLoading.value = false;
      }
    };

    const goToPage = (page) => {
      fetchMedicines(page);
    };

    const isAdmin = computed(() => {
      const user = userStore.user;
      return user?.is_admin === true;
    });

    // Separar medicinas seleccionadas por estado
    const selectedActiveMedicines = computed(() => {
      return selectedMedicines.value.filter(id => {
        const medicine = medicines.value.find(m => m.id === id);
        return medicine && medicine.is_active;
      });
    });

    const selectedInactiveMedicines = computed(() => {
      return selectedMedicines.value.filter(id => {
        const medicine = medicines.value.find(m => m.id === id);
        return medicine && !medicine.is_active;
      });
    });

    const toggleSelection = (medicineId) => {
      const index = selectedMedicines.value.indexOf(medicineId);
      if (index > -1) {
        selectedMedicines.value.splice(index, 1);
      } else {
        selectedMedicines.value.push(medicineId);
      }
    };

    const disableMedicines = async () => {
      if (selectedActiveMedicines.value.length === 0) return;

      try {
        await Promise.all(
          selectedActiveMedicines.value.map(async (id) => {
            await medicineService.disableMedicine(id);
          })
        );
        selectedMedicines.value = [];
        await fetchMedicines(pagination.value.page);
      } catch (err) {
        console.error("Error al deshabilitar medicinas:", err);
      }
    };

    const enableMedicines = async () => {
      if (selectedInactiveMedicines.value.length === 0) return;

      try {
        await Promise.all(
          selectedInactiveMedicines.value.map(async (id) => {
            await medicineService.enableMedicine(id);
          })
        );
        selectedMedicines.value = [];
        await fetchMedicines(pagination.value.page);
      } catch (err) {
        console.error("Error al habilitar medicinas:", err);
      }
    };

    const formatDate = (dateStr) => {
      if (!dateStr) return 'No disponible';
      const date = new Date(dateStr);
      return date.toLocaleDateString("es-ES", {
        year: "numeric",
        month: "short",
        day: "numeric"
      });
    };

    onMounted(() => {
      fetchMedicines(1);
    });

    return {
      medicines,
      pagination,
      selectedMedicines,
      selectedActiveMedicines,
      selectedInactiveMedicines,
      isLoading,
      isAdmin,
      toggleSelection,
      disableMedicines,
      enableMedicines,
      goToPage,
      formatDate
    };
  },
};
</script>

<template>
  <div class="medicine-table-container">
    <div class="table-header">
      <h2 class="table-title">Lista de Medicamentos</h2>
      <div v-if="isAdmin" class="admin-actions">
        <!-- Botón para deshabilitar activos -->
        <button v-if="selectedActiveMedicines.length > 0" class="action-btn danger" @click="disableMedicines">
          <i class="core-icon disable-round small-icon"></i>
          <span>Deshabilitar {{ selectedActiveMedicines.length }}</span>
        </button>

        <!-- Botón para habilitar inactivos -->
        <button v-if="selectedInactiveMedicines.length > 0" class="action-btn success" @click="enableMedicines">
          <i class="core-icon check-circle small-icon"></i>
          <span>Habilitar {{ selectedInactiveMedicines.length }}</span>
        </button>

        <span v-if="selectedMedicines.length > 0" class="selection-count">
          {{ selectedMedicines.length }} seleccionados
        </span>
      </div>
    </div>

    <div class="table-wrapper">
      <table class="medicine-table">
        <thead>
          <tr>
            <th v-if="isAdmin">
              <input type="checkbox" @change="$event.target.checked ? selectAll() : clearAll()" />
            </th>
            <th>ID</th>
            <th>Nombre</th>
            <th>Dosificación</th>
            <th>Frecuencia</th>
            <th>Fecha Creación</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody v-if="!isLoading">
          <tr v-if="medicines.length === 0">
            <td :colspan="isAdmin ? 7 : 6" class="no-data">
              No hay medicinas disponibles
            </td>
          </tr>
          <tr v-else v-for="medicine in medicines" :key="medicine.id" class="medicine-row"
            :class="{ 'selected': selectedMedicines.includes(medicine.id), 'inactive': !medicine.is_active }">
            <td v-if="isAdmin">
              <input type="checkbox" :checked="selectedMedicines.includes(medicine.id)"
                @change="toggleSelection(medicine.id)" />
            </td>
            <td>{{ medicine.id }}</td>
            <td>{{ medicine.name }}</td>
            <td>
              <span class="dosage-badge">{{ medicine.dosage }}</span>
            </td>
            <td>{{ medicine.frequency_hours ? `Cada ${medicine.frequency_hours}h` : 'Según indicación' }}</td>
            <td>{{ formatDate(medicine.created_at) }}</td>
            <td>
              <span class="status-badge" :class="medicine.is_active ? 'active' : 'inactive'">
                {{ medicine.is_active ? 'Activo' : 'Inactivo' }}
              </span>
            </td>
          </tr>
        </tbody>
        <tbody v-else>
          <tr>
            <td :colspan="isAdmin ? 7 : 6" class="loading-row">
              <div class="spinner"></div>
              Cargando...
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pagination">
      <button class="page-btn" :disabled="pagination.page === 1" @click="goToPage(pagination.page - 1)">
        ⬅ Anterior
      </button>

      <span class="page-info">
        Página {{ pagination.page }} / {{ pagination.pages }} ({{ pagination.total }} total)
      </span>

      <button class="page-btn" :disabled="pagination.page === pagination.pages" @click="goToPage(pagination.page + 1)">
        Siguiente ➡
      </button>
    </div>
  </div>
</template>

<style scoped>
.medicine-table-container {
  background: #1a1e23;
  padding: 20px;
  border-radius: 8px;
  color: #cfd3dc;
  font-family: Inter, sans-serif;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.table-title {
  font-size: 1.4rem;
  margin: 0;
  color: #fff;
  font-weight: 600;
  border-left: 4px solid #38aa77;
  padding-left: 10px;
}

.admin-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.selection-count {
  background: #1f252d;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  color: #38aa77;
}

.table-wrapper {
  overflow-x: auto;
  background: #111418;
  border-radius: 8px;
  border: 1px solid #222;
  margin-bottom: 20px;
}

.medicine-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 900px;
}

.medicine-table th {
  background: #1f252d;
  padding: 14px 16px;
  font-size: 0.9rem;
  color: #38aa77;
  font-weight: 600;
  border-bottom: 1px solid #222;
  letter-spacing: 0.05em;
  text-align: left;
}

.medicine-table th:first-child {
  width: 50px;
  text-align: center;
}

.medicine-table td {
  padding: 14px 16px;
  border-bottom: 1px solid #222;
  color: #cfd3dc;
  font-size: 0.9rem;
}

.medicine-table td:first-child {
  text-align: center;
}

.medicine-row {
  cursor: default;
  transition: all 0.2s ease;
}

.medicine-row:hover {
  background-color: #232a33;
}

.medicine-row.selected {
  background-color: #2a4a3e !important;
  border-left: 3px solid #38aa77;
}

.medicine-row.inactive {
  opacity: 0.6;
}

.dosage-badge {
  background: #38aa77;
  color: white;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.status-badge.active {
  background: rgba(56, 170, 119, 0.2);
  color: #38aa77;
  border: 1px solid #38aa77;
}

.status-badge.inactive {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  border: 1px solid #ef4444;
}

.action-btn {
padding: 8px 16px;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.25s;
    border: none;
    font-family: Inter, sans-serif;
    font-size: 0.9rem;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 12px;
}

.action-btn.danger {
  background: transparent;
  color: #ef4444;
  border: 1px solid #ef4444;
  i{
    background-color: #ef4444;
  }
}

.action-btn.danger:hover {
  background: #ef4444;
  color: white;
    i{
    background-color: white;
  }
}

.action-btn.success {
  background: transparent;
  color: #38aa77;
  border: 1px solid #38aa77;
    i{
    background-color: #38aa77;
  }
}

.action-btn.success:hover {
  background: #38aa77;
  color: white;
      i{
    background-color: white;
  }
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
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

.loading-row {
  text-align: center;
  padding: 40px !important;
}

.spinner {
  display: inline-block;
  width: 30px;
  height: 30px;
  border: 3px solid #222;
  border-top: 3px solid #38aa77;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-right: 12px;
  vertical-align: middle;
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
  .table-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .admin-actions {
    width: 100%;
    justify-content: flex-end;
    flex-wrap: wrap;
  }

  .medicine-table th,
  .medicine-table td {
    font-size: 0.85rem;
    padding: 10px 8px;
  }

  .pagination {
    flex-direction: column;
    gap: 10px;
  }
}
</style>