<template>
  <div id="app">
    <div id="selector">
      <el-select v-model="matrixdata" placeholder="matrixC" size="mini">
        <el-option
          v-for="data in dataset"
          :key="data.value"
          :label="data.label"
          :value="data.value">
        </el-option>
      </el-select>
    </div>
    <matrixplot></matrixplot>
    <causalitygraph></causalitygraph>
  </div>
</template>

<script>
import Matrixplot from './components/Matrixplot.vue'
import Causalitygraph from './components/Causalitygraph.vue'


export default {
  name: 'App',
  data: () => ({
    matrixdata: '../static/matrixT.json',
    dataset: [
      {value: '../static/matrixC.json', label: 'matrixC'},
      {value: '../static/matrixT.json', label: 'matrixT'}
    ]
  }),
  components: {
    matrixplot: Matrixplot,
    causalitygraph: Causalitygraph,
  },
  watch: {
    matrixdata (val) {
      this.eventHub.$emit('initMatrixplotScene', this.matrixdata)
    }
  },
  mounted() {
    this.eventHub.$emit('initMatrixplotScene', this.matrixdata)
    this.eventHub.$emit('initCausalitygraphScene')
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  color: #2c3e50;
  /* margin-top: 60px; */
}
#forcelayout-container {
  position: relative;
  float: left;
}

</style>
