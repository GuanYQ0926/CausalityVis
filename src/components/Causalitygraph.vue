<template>
  <div id="causalitygraph">
    <div id="container"></div>
  </div>
</template>

<script>
import Causalitygraph from '../scripts/causalitygraph'

export default {
  name: 'Causalitygraph',
  data() {
    return {
      cg: new Causalitygraph(),
    }
  },
  mounted() {
    this.eventHub.$on('initCausalitygraphScene', () => this.cg.initScene())
  },
}
</script>

<style>
</style>
