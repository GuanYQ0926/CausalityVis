<template>
  <div id="matrixplot">
  </div>
</template>

<script>
import Matrixplot from '../scripts/matrixplot'

export default {
  name: 'Matrixplot',
  data() {
    return {
      mp: new Matrixplot(),
    }
  },
  mounted() {
    this.eventHub.$on('initMatrixplotScene', (file) => this.mp.initScene(file))
  },
}
</script>

<style>
  .dot {
    stroke: #000;
  }
  .axis path,
	.axis line{
		fill: none;
		stroke-width: 1px;
		stroke: #777;
	}
  #matrixplot {
    position: relative;
    float: left;
  }
</style>
