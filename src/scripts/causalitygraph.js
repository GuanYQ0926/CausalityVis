import * as Sigma from 'sigma'


export default class Causalitygraph {
  constructor() {
    this.width = window.innerWidth
    this.height = window.innerHeight
  }
  initScene() {
    fetch('../static/resultT.json')
      .then(res => res.json())
      .then(dataset => {
        const colors = ['#FF564F', '#FFBB2B', '#25C73A']
        const edges = []
        let count = 0
        for(const key in dataset) {
          const data = dataset[key]
          const temp = data[data.length-1]
          edges.push({id: count, source: temp.d1, target: parseInt(key), type: 'arrow', color:colors[temp.lag1], size: 5})
          count += 1
          edges.push({id: count, source: temp.d2, target: parseInt(key), type: 'arrow', color:colors[temp.lag2], size: 5})
          count += 1
        }
        // console.log(temp)
        const nodes = [{id:0, x:-10, y: 10, color:'#CCC', size:10, label:'y1'},
          {id:1, x:10, y: 10, color:'#CCC', size:10, label:'y2'},
          {id:2, x:10, y: -10, color:'#CCC', size:10, label:'y3'},
          {id:3, x:-10, y: -10, color:'#CCC', size:10, label:'y4'}]
        const graph = {nodes: nodes, edges: edges}
        const container = document.getElementById('container')
        container.style.width = `${window.innerWidth/2}px`
        container.style.height = `${window.innerHeight}px`
        const s = new Sigma.sigma({
          graph: graph,
          container: container,
          settings: {
            maxNodeSize: 3,
            maxEdgeSize: 3
          }
        })
        s.refresh()
      })
  }
}
