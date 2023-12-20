

<template>
  <p>oder wählen Sie einen festen Zeitraum:</p>
  <n-radio-group :value="modelValue" @update:value="handleUpdate" name="radiobuttongroup1" color="white">
    <n-radio-button
        v-for="span in time_span"
        :key="span.value"
        :value="span.value"
        :label="span.label"
        style="background-color: white;"
    />
  </n-radio-group>
</template>

<script lang='ts'>
import { defineComponent, PropType } from 'vue';

export type DistanceRadioValue =
    'co2_last_track_in_kg'
    | 'co2_last_week_in_kg'
    | 'co2_last_month_in_kg'
    | 'co2_last_year_in_kg'
    | 'co2_last_day_in_kg'


export default defineComponent({
  props: {
    modelValue: { type: String as PropType<DistanceRadioValue>, required: true }
  },
  emits: ['update:modelValue', 'update:showOutput'],
  setup(_, { emit }) {
    const time_span = [
      {
        value: 'co2_last_track_in_kg',
        label: 'letzte Fahrt'
      },
      {
        value: 'co2_last_day_in_kg',
        label: 'letzter Tag'
      },
      {
        value: 'co2_last_week_in_kg',
        label: 'letzte Woche'
      },
      {
        value: 'co2_last_month_in_kg',
        label: 'letzter Monat'
      },
      {
        value: 'co2_last_year_in_kg',
        label: 'letztes Jahr'

      },
    ] as Array<{ value: DistanceRadioValue, label: string }>;

    const handleUpdate = (value: DistanceRadioValue) => {
      // Hier wird das Ereignis 'update:modelValue' mit dem ausgewählten Wert emittiert
      emit('update:modelValue', value);

      // Hier kannst du die Variable 'showOutput' auf false in deiner Hauptanwendung setzen
      emit('update:showOutput', false);
    };

    return {
      time_span,
      handleUpdate
    };
  }
});
</script>

<style scoped>
p {
  color: white;
  font-size: 18px
}

</style>