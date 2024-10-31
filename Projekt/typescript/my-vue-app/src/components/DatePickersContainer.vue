<template>
  <p>Geben Sie einen Zeitraum an für den die CO2-Emission berechnet wird:</p>
  <div style="display: flex; justify-content: center;">
    <div style="margin-right: 50px;">
      <label for="startDate">Beginn </label>
      <n-date-picker panel type="date" :value="localStartDate?.getTime()" @update-value="$emit('update:startDate',
                                                                                               !$event ? undefined : new Date($event))"/>
    </div>
    <div>
      <label for="endDate">Ende </label>
      <n-date-picker panel type="date" :value="localEndDate?.getTime()" @update-value="$emit('update:endDate',
                                                                                             !$event ? undefined : new Date($event))"/>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, watchEffect, ref } from 'vue';

export default defineComponent({
  props: {
    startDate: Date,
    endDate: Date,
  },
  setup(props, { emit }) {
    // Referenz für local state
    const localStartDate = ref(props.startDate);
    const localEndDate = ref(props.endDate);

    // warte auf Eingabe im Kalender-widget
    watchEffect(() => {
      localStartDate.value = props.startDate;
      localEndDate.value = props.endDate;

      // Ausgabe an App.vue
      emit('updateDatePickersValues', {
        startDate: localStartDate.value,
        endDate: localEndDate.value,
      });
    });

    return {
      localStartDate,
      localEndDate,
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
