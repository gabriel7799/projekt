<template>
  <div class="app-wrapper">
    <div style="display: flex; justify-content: center;">
    <h1>CO<sub>2</sub>-Rechner</h1>

    </div>
    <div>
      <a href="https://cynatix.com/" target="_blank">
        <img src="./assets/cyn1.png" class="logo" style="width:20%; height:auto"/>
      </a>
    </div>

    <div class=" align items-center">

      <plates/>
      <hsn v-model:hsn="hsn" v-model:tsn="tsn"/>
      <date-pickers-container v-model:start-date="startDate" v-model:end-date="endDate"
                              @update:showOutput="updateShowOutput"
                              @update:DatePickersValues="updateDatePickersValues"/>
      <distance-radio
          v-model:model-value="distance"
          @update:showOutput="updateShowOutput"
          v-bind:disabled="isRadioDisabled"
      />
      <n-switch v-model="isRadioDisabled"/>


      <n-space justify="center" style="margin-top: 20px">
        l
        <n-button type="warning" style="width:200px; height:45px" @click="calculate()">
          Berechne
          <template #icon>
            <n-icon>
              <Car/>
            </n-icon>
          </template>
        </n-button>
      </n-space>


      <p v-if="showOutput">
        {{ calculationTitle }}: {{ calculationValue }} kg CO2<br>
        Die CO2-Emission in Ihrem ausgewählten Zeitraum beträgt {{ time_value }} kg.
      </p>


    </div>
  </div>

</template>


<script lang="ts">
import {computed, defineComponent, reactive, ref, watch} from 'vue';
import {CarSide as Car} from '@vicons/fa';
import Plates from "./components/Plates.vue";
import Hsn from "./components/Hsn.vue";
import DatePickersContainer from "./components/DatePickersContainer.vue";
import DistanceRadio, {DistanceRadioValue} from "./components/DistanceRadio.vue";

interface Co2Values {
  co2_last_track_in_kg: undefined | number;
  co2_last_day_in_kg: undefined | number;
  co2_last_week_in_kg: undefined | number;
  co2_last_month_in_kg: undefined | number;
  co2_last_year_in_kg: undefined | number;
  co2_for_timespan: undefined | number;
}

export default defineComponent({

  components: {Plates, DistanceRadio, Hsn, Car, DatePickersContainer},
  setup() {
    // Refs for date pickers
    const startDate = ref<Date>();
    const endDate = ref<Date>();

    const isRadioDisabled = ref(true)


    // Other refs and variables
    const hsn = ref('0005');
    const tsn = ref('AAA');
    const distance = ref<DistanceRadioValue>('co2_last_day_in_kg');
    const co2Values: Co2Values = reactive({
      co2_last_track_in_kg: undefined,
      co2_last_day_in_kg: undefined,
      co2_last_week_in_kg: undefined,
      co2_last_month_in_kg: undefined,
      co2_last_year_in_kg: undefined,
      co2_for_timespan: undefined,
    });
    const showOutput = ref(false);
    const useTimeFrames = ref(false);

    // Async function to fetch and calculate CO2 values
    async function calculate() {
      try {
        const formattedStartDate = startDate.value?.toISOString().substring(0, 10) ?? '';
        const formattedEndDate = endDate.value?.toISOString().substring(0, 10) ?? '';

        const apiUrl = `http://127.0.0.1:5000/data/5caf44d6ddfbb729a0c0ef66/${hsn.value}${tsn.value}/${formattedStartDate}/${formattedEndDate}`;
        const response = await fetch(apiUrl);
        const data = await response.json() as Co2DataResponse;

        co2Values.co2_for_timespan = data[5].calculated_emission_for_timespan_in_kg;
        co2Values.co2_last_track_in_kg = data[3].co2_data.co2_last_track_in_kg;
        co2Values.co2_last_day_in_kg = data[3].co2_data.co2_last_day_in_kg;
        co2Values.co2_last_week_in_kg = data[3].co2_data.co2_last_week_in_kg;
        co2Values.co2_last_month_in_kg = data[3].co2_data.co2_last_month_in_kg;
        co2Values.co2_last_year_in_kg = data[3].co2_data.co2_last_year_in_kg;
        showOutput.value = true;
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    }

    // Method to update showOutput
    const updateShowOutput = (value: boolean) => {
      showOutput.value = value;
    };
    watch([startDate, endDate], () => {
      updateShowOutput(false);


    });

    interface DateValues {
      startDate: Date;
      endDate: Date;
      // Add other properties if needed
    }

    const updateDatePickersValues = (values: DateValues) => {
      // Handle the updated values from DatePickersContainer
      startDate.value = values.startDate;
      endDate.value = values.endDate;
      // Update other values as needed
    };

    // Computed properties
    const calculationTitle = computed(() => {
      switch (distance.value) {
        case "co2_last_track_in_kg":
          return 'Bei der letzten Fahrt erzeugten Sie';
        case "co2_last_day_in_kg":
          return 'Bei den Fahrten am vergangenen Tag erzeugten Sie';
        case "co2_last_week_in_kg":
          return 'Bei den Fahrten der letzten Woche erzeugten Sie';
        case "co2_last_month_in_kg":
          return 'Bei den Fahrten im letzten Monat erzeugten Sie';
        case "co2_last_year_in_kg":
          return 'Bei den Fahrten des letzten Jahres erzeugten Sie';
      }
    });

    const calculationValue = computed(() => co2Values[distance.value]);
    const time_value = computed(() => co2Values.co2_for_timespan);

    return {
      hsn,
      tsn,
      distance,
      startDate,
      endDate,
      showOutput,
      calculationTitle,
      calculationValue,
      calculate,
      time_value,
      useTimeFrames,
      disabled: ref(true),
      active: ref(false),
      updateShowOutput,
      updateDatePickersValues,
      isRadioDisabled

    };
  },
});
</script>


<style scoped>

h1 {
  color: white;
  text-align: center;
  font-size: 50px;
}

p {
  color: white;
  font-size: 18px;
}

.logo {
  height: 22em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

.app-wrapper {
  border: 1px solid #ccc;
  height: 1200px; /* Set a fixed height for the container */
  overflow: auto; /* Add scrollbar if content overflows */
  padding: 20px;

  background: rgba(44,62,80)
}


</style>
