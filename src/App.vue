<template>
  <div id="app">
    <div id="stlgraph"></div>
    <el-tabs v-model="activeName" @tab-click="handleTabClick">
      <el-tab-pane label="view1" name="first">
        <div id="imageview1"></div>
      </el-tab-pane>
      <el-tab-pane label="view2" name="second">
        <div id="imageview2"></div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import * as dat from 'dat.gui'
import STLGraph from './scripts/stlgraph'
import SliceGraph from './scripts/slicegraph'


export default {
  name: 'App',
  data() {
    return {
      gui: new dat.GUI(),
      params: {
        slice: 1,
        reset: () => this.sg.resetCamera()
      },
      sg: new STLGraph(),
      slg: new SliceGraph(),
      activeName: 'first',
    }
  },
  mounted() {
    this.initDatGUI()
    this.sg.initScene()
    document.getElementById('stlgraph').appendChild(this.sg.domElement)
    document.addEventListener('resize', () => this.sg.resetDimensions())
    this.renderSliceView()
  },
  methods: {
    initDatGUI() {
      this.gui.domElement.id = 'dat-gui'
      this.gui.add(this.params, 'slice', {'slice1': 1, 'slice2': 2, 'slice3': 3}).onChange(val => {
        this.renderSliceView()
      })
      this.gui.add(this.params, 'reset')
    },
    renderSliceView() {
      this.sg.drawSlice()
      this.slg.drawFirstImage(512, 384.4, 'imageview1', '../../static/images/photo2.jpg')
      this.slg.drawFirstImage(596, 345.8, 'imageview2', '../../static/images/photo1.tiff')
    },
    handleTabClick(tab, event) {}
  }
}
</script>

<style>
#dat-gui {
  position: absolute;
  top: 2px;
  left: 2px;
}
#stlgraph {
  position: relative;
  float: left;
}
#slicegraph {
  position: relative;
  float: right;
}
</style>
