import apiClient from "./apiClient";

export const patientService = {
  async getAllPatients() {
    const response = await apiClient.get("/api/patients");
    return response.data;
  },

  getPatientsPaginated(page = 1, per_page = 10) {
    return apiClient.get(`/api/patients?page=${page}&per_page=${per_page}`);
  },

  async getPatientById(id) {
    const response = await apiClient.get(`/api/patients/${id}`);
    return response.data;
  },
  async getUnassignedPatients() {
    const response = await apiClient.get(`/api/patients/unassigned`);
    return response.data;
  },
  async getPatientByUserId(id) {
    const response = await apiClient.get(`/api/patients/carer/${id}/patients`);
    return response.data;
  },

  async createPatient(data) {
    const response = await apiClient.post("/api/patients", data);
    return response.data;
  },

  async updatePatient(id, data) {
    const response = await apiClient.put(`/api/patients/${id}`, data);
    return response.data;
  },

  async deletePatient(id) {
    const response = await apiClient.delete(`/api/patients/${id}`);
    return response.data;
  },
  async removeAssignedPatient(id) {
    const response = await apiClient.delete(`/api/patients/${id}/assign`);
    return response.data;
  },
  async assignPatientToUser (patientId, userId) {
    const response = await apiClient.post(`/api/patients/${patientId}/assign`, {
      user_id: userId,
    });
    return response.data;
  },
  async getPatientFromAssignedUser(id) {
    const response = await apiClient.get(`/api/patients/${id}/users`);
    return response.data;
  },
};
