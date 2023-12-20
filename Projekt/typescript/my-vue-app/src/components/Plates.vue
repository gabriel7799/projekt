<template>
  <div>
    <n-dropdown placement="bottom-start" trigger="click" size="small" placeholder="Wählen Sie ein Fahrzeug aus der Flotte" :options="plateOptions">
      <n-button>Nummernschild auswählen</n-button>
    </n-dropdown>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useMessage } from 'naive-ui';

export default defineComponent({
  setup: function () {
    const message = useMessage();
    const plateOptions = ref();

    async function fetchPlates() {
      try {
        const apiUrl = 'http://127.0.0.1:5000/data/orga/5a167a260db605287423a52d';
        const response = await fetch(apiUrl);
        const data = await response.json();

        plateOptions.value = Object.keys(data).map((plate) => ({
          label: plate,
          key: data[plate],
        }));
      } catch (error) {
        console.error('Fehler beim Abrufen der Kennzeichen:', error);
        message.error('Fehler beim Abrufen der Kennzeichen');
      }
    }

    onMounted(() => {
      fetchPlates();
    });

    return {
      plateOptions,
    };
  },
});
</script>

<style scoped>
label {
  color: white;
  font-size: 18px
}
p {
  color:white;
  font-size: 18px;
}

</style>
