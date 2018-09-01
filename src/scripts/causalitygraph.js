import * as d3 from 'd3'


export default class Causalitygraph {
  constructor() {
    this.width = window.innerWidth / 3
    this.height = window.innerHeight
  }
  initScene() {
    // fetch('../static/resultT.json')
    //   .then(res => res.json())
    //   .then(dataset => {
    //     const colors = ['#FF564F', '#FFBB2B', '#25C73A']
    //     const edges = []
    //     let count = 0
    //     for(const key in dataset) {
    //       const data = dataset[key]
    //       const temp = data[data.length-1]
    //       edges.push({id: count, source: temp.d1, target: parseInt(key), type: 'arrow', color:colors[temp.lag1], size: 5})
    //       count += 1
    //       edges.push({id: count, source: temp.d2, target: parseInt(key), type: 'arrow', color:colors[temp.lag2], size: 5})
    //       count += 1
    //     }
    //     // console.log(temp)
    //     const nodes = [{id:0, x:-10, y: 10, color:'#CCC', size:10, label:'y1'},
    //       {id:1, x:10, y: 10, color:'#CCC', size:10, label:'y2'},
    //       {id:2, x:10, y: -10, color:'#CCC', size:10, label:'y3'},
    //       {id:3, x:-10, y: -10, color:'#CCC', size:10, label:'y4'}]
    //     const graph = {nodes: nodes, edges: edges}
    //     const container = document.getElementById('container')
    //     container.style.width = `${window.innerWidth/2}px`
    //     container.style.height = `${window.innerHeight}px`
    //     const s = new Sigma.sigma({
    //       graph: graph,
    //       container: container,
    //       settings: {
    //         maxNodeSize: 3,
    //         maxEdgeSize: 3
    //       }
    //     })
    //     s.refresh()
    //   })
    fetch('../static/resultT.json')
      .then(res => res.json())
      .then(dataset => {
        // generate dataset
        const nodesData = [],
          edgesData = []
        let color = 0
        for(const sk in dataset) {
          nodesData.push({id: parseInt(sk), x: parseInt(sk)*50, y: parseInt(sk)*50})
          const obj = dataset[sk][0]
          const targets = obj.data
          const lags = obj.lag
          for(let i=0; i<lags.length; i++) {
            const target = targets[i],
              lag = lags[i]
            edgesData.push({'source': parseInt(sk), 'target': parseInt(target),
              'lag': parseInt(lag), 'color': color})
          }
          color += 1
        }
        const margin = {top: 20, right: 20, bottom: 100, left: 20},
          height = this.height/2
        const colormap = ['#e6194b', '#3cb44b', '#ffe119', '#0082c8', '#f58231',
          '#911eb4', '#46f0f0', '#f032e6', '#d2f53c', '#fabebe', '#008080',
          '#e6beff', '#aa6e28', '#fffac8', '#800000', '#aaffc3', '#808000',
          '#ffd8b1', '#000080', '#808080', '#FFFFFF', '#000000']
        const svg = d3.select(document.getElementById('causalitygraph'))
          .append('svg')
          .attr('width', this.width)
          .attr('height', this.height)
          .append('g')
          .attr('transform', `translate(${margin.left}, ${margin.top})`)
        const idToNode = {}
        nodesData.forEach(n => {
          idToNode[n.id] = n
          n.x = parseInt(n.id)*130
          n.y = height
        })
        edgesData.forEach(e => {
          e.source = idToNode[e.source]
          e.target = idToNode[e.target]
        })
        const marker = svg.append('defs')
          .append('marker')
          .attr('id', 'Triangle')
          .attr('refX', 6)
          .attr('refY', 3)
          .attr('markerUnits', 'userSpaceOnUse')
          .attr('markerWidth', 6)
          .attr('markerHeight', 9)
          .attr('orient', 'auto')
          .append('path')
          .style('fill', '#111')
          .attr('d', 'M 0 0 6 3 0 6 1.5 3')
        const node = svg.append('g')
          .attr('class', 'nodes')
          .selectAll('circle')
          .data(nodesData)
          .enter().append('circle')
          .attr('cx', d => d.x)
          .attr('cy', d => d.y)
          .attr('r', 3)
        const link = svg.append('g')
          .attr('class', 'links')
          .selectAll('path')
          .data(edgesData)
          .enter().append('path')
          .attr('d', d => `M ${d.source.x} ${d.source.y} `
                           + `Q ${(d.source.x+d.target.x)/2} ${(d.source.y+d.target.y)/2-d.lag*20-15}, `
                           + `${d.target.x} ${d.target.y}`)
          .attr('marker-end', 'url(#Triangle)')
          .attr('stroke', d => colormap[d.color])
          .attr('stroke-width', 2)
      })
  }
}
