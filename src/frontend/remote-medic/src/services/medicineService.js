import apiClient from "./apiClient";

const medicineService = {
  async getAllMedicines(
    page = 1,
    perPage = 10,
    activeOnly = true,
    getAll = false
  ) {
    const params = {
      page,
      per_page: perPage,
      active_only: activeOnly,
      get_all: getAll,
    };
    const response = await apiClient.get("/api/medicines", { params });
    return response.data;
  },

  async getMedicineById(id) {
    const response = await apiClient.get(`/api/medicines/${id}`);
    return response.data;
  },

  async getPatientMedicines(patientId) {
    const response = await apiClient.get(
      `/api/medicines/patients/${patientId}/medicines`
    );
    return response.data;
  },
  async enableMedicine(medicineId) {
    const response = await apiClient.put(`/api/medicines/enable/${medicineId}`);
    return response.data;
  },
  async disableMedicine(medicineId) {
    const response = await apiClient.put(
      `/api/medicines/disable/${medicineId}`
    );
    return response.data;
  },

  async assignMedicineToPatient(patientId, medicineId, dose_per_take, notes) {
    const response = await apiClient.post(
      `/api/medicines/patients/${patientId}/medicines/${medicineId}`,
      {
        dose_per_take,
        notes,
      }
    );
    return response
  },

  async removeMedicineFromPatient(patientId, medicineId) {
    const response = await apiClient.delete(
      `/api/medicines/patients/${patientId}/medicines/${medicineId}`
    );
    return response.data;
  },

  async searchMedicines(query, activeOnly = true) {
    const params = { q: query };
    if (activeOnly) params.active = true;
    const response = await apiClient.get("/api/medicines/search", { params });
    return response.data;
  },

  async getCarerMedicines(carerId) {
    const response = await apiClient.get(`/api/carers/${carerId}/medicines`);
    return response.data;
  },
};

export default medicineService;
