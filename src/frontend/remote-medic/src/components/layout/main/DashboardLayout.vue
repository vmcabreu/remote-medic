<script>
import PatientTableView from "@/components/patient/PatientTableView.vue";
import MedicineTable from "@/components/medicine/MedicineTable.vue";

export default {
  name: "MainLayout",
  components: {
      MedicineTable,
      PatientTableView
  }
};
</script>

<template>
  <div class="layout">
    <PatientTableView :show-assigned="true" />
    <MedicineTable/>
  </div>
</template>

<style scoped>
/* Layout general */
.layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #1a1e23;
  color: #fff;
  font-family: Inter, sans-serif;
}
</style>
