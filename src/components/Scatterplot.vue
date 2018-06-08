<template>
  <div id="scatterplot"></div>
</template>

<script>
import Scatterplot from '../scripts/scatterplot'

export default {
  name: 'Scatterplot',
  data() {
    return {
      sp: new Scatterplot(),
    }
  },
  mounted() {
    this.eventHub.$on('initScatterplotScene', () => this.sp.initScene())
  }
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
</style>
