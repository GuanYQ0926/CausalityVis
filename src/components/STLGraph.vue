<template>
  <div id="stlgraph">
  </div>
</template>

<script>
import * as dat from 'dat.gui'
import STLGraph from '../scripts/stlgraph'

export default {
  name: 'STLGraph',
  data() {
    return {
      gui: new dat.GUI(),
      sg: new STLGraph(),
      params: {
        slice: 0,
        reset: () => this.sg.resetCamera()
      },
    }
  },
  mounted() {
    this.eventHub.$on('initSTLGraphScene', () => this.sg.initScene())
    this.initDatGUI()
    document.getElementById('stlgraph').appendChild(this.sg.domElement)
    document.addEventListener('resize', () => this.sg.resetDimensions())
  },
  methods: {
    initDatGUI() {
      this.gui.domElement.id = 'dat-gui'
      this.gui.add(this.params, 'slice', {'--': 0 ,'slice1': 1, 'slice2': 2, 'slice3': 3}).onChange(val => {
        console.log(val)
      })
      this.gui.add(this.params, 'reset')
    }
  }
}
</script>

<style>
#dat-gui {
  position: absolute;
  top: 2px;
  left: 2px;
}
</style>



<!-- <template>
  <div id="app">
    <stlgraph></stlgraph>
  </div>
</template>

<script>
import STLGraph from './components/STLGraph.vue'


export default {
  name: 'App',
  data: () => ({
  }),
  components: {
    stlgraph: STLGraph,
  },
  watch: {
  },
  mounted() {
    this.eventHub.$emit('initSTLGraphScene')
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
#forcelayout-container {
  position: relative;
  float: left;
}

</style> -->
