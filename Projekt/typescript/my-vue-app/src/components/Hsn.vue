<template>
  <div>
    <p>Bitte geben Sie die vierstellige HSN aus der Zulassungsbescheinigung ein:</p>

    <n-space justify="center">
      <n-space>
        <n-input :value="hsn" @update:value="$emit('update:hsn', $event)" round placeholder="HSN"/>

      </n-space>
    </n-space>

    <p>Bitte geben Sie die dreistellige TSN aus der Zulassungsbescheinigung ein:</p>
    <n-space justify="center">
      <n-space>
        <n-input :value="tsn" @update:value="$emit('update:tsn', $event.toUpperCase())" round placeholder="TSN"/>
      </n-space>
    </n-space>

  </div>
</template>

<script lang='ts'>
import {defineComponent} from 'vue'


export default defineComponent({
  props: {
    hsn: {type: String, required: true},
    tsn: {type: String, required: true},
  },
  emits: ['update:hsn', 'update:tsn']
})
</script>


<style scoped>
p {
  color: white;
  font-size: 18px
}

</style>