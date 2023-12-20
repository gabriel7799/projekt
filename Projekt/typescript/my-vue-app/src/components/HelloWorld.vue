<template>
  <h1>{{ message }}</h1>


  <div class="card">
    <n-button @click="count++" type="info">{{ count }}</n-button>

  </div>


</template>


<script lang="ts">
import {computed, defineComponent, ref} from 'vue'

export default defineComponent({
  name: 'HelloWorld',
  props: {
    msg: {type: String, required: true}
  },
  setup(props) {

    console.log('HelloWorld Props', props.msg);

    const count = ref<number>(-10);

    setInterval(() => count.value--, 1000);

    return {
      count,
      message: computed(() => props.msg + ' ' + count.value)
    };

  }
});
</script>


<style scoped>
.read-the-docs {
  color: #888;
}

</style>
