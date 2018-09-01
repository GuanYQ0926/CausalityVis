import * as d3 from 'd3'
// import * as Sigma from 'sigma'


export default class Matrixplot {
  constructor() {
    this.width = window.innerWidth
    this.height = window.innerHeight
  }
  initScene(file) {
    const matrixData = fetch(file).then(res => res.json())
    Promise.all([matrixData]).then(dataset => {
      this.renderScene(dataset)})
  }
  renderScene(datasets) {
    const matrixData = datasets[0]
    // const layoutData = datasets[1]
    const gridNum = matrixData.length,
      data = matrixData.causality,
      margin = {top: 20, right: 0, bottom: 100, left: 5},
      width = window.innerWidth/2,
      height = window.innerHeight,
      matrixWidth = Math.min(width, height*0.8),
      gridSize = Math.floor(matrixWidth / gridNum),
      axisLabel = d3.range(1, gridNum+1).map(d => d.toString()),
      minmax = d3.extent(data, d => d.value),
      colorScale = d3.scaleSequential(d3.interpolateMagma)
        .domain([minmax[1], minmax[0]])
    let grid  //grid dom
    let threshold = minmax[0]


    document.getElementById('matrixplot').innerHTML = ''
    //matrixplot
    const svg = d3.select(document.getElementById('matrixplot'))
      .append('svg')
      .attr('width', width)
      .attr('height', height)
    const g = svg.append('g')
      .attr('transform', `translate(${margin.left}, ${margin.top})`)
    //matrixplot axis
    g.selectAll('.axislabel')
      .data(axisLabel)
      .enter().append('text')
      .text((d, i) => ((i+1)%5==0 ? d : null))
      .attr('x', 0)
      .attr('y', (d, i) => i * gridSize)
      .style('text-anchor', 'end')
      .style('font-size', '0.7em')
      .attr('transform', `translate(-6, ${gridSize/1.5})`)
    g.selectAll('.axislabel')
      .data(axisLabel)
      .enter().append('text')
      .text((d, i) => ((i+1)%5==0 ? d : null))
      .attr('x', (d, i) => i * gridSize)
      .attr('y', 0)
      .style('text-anchor', 'middle')
      .style('font-size', '0.7em')
      .attr('transform', `translate(${gridSize/2}, -6)`)

    //matrixplot chart
    const matrixplotChart = (data) => {
      const grids = g.selectAll('.grid')
        .data(data)
      grids.append('title')
      grid = grids.enter().append('rect')
        .attr('x', d => d.src*gridSize)
        .attr('y', d => d.dst*gridSize)
        .attr('rx', 4)
        .attr('ry', 4)
        .attr('class', 'grid')
        .attr('width', gridSize)
        .attr('height', gridSize)
        .on('mouseover', d => mouseovered(d))
        .on('mouseleave', () => {d3.select('#text-g').remove()})
        .merge(grids)
        .style('fill', d => d.value>=threshold?colorScale(d.value):'white')
    }
    //matrixplot mouseover
    function mouseovered(gridData) {
      if(gridData.value<threshold) {
        return
      }
      d3.select('#text-g').remove()
      const text_g = svg.append('g')
        .attr('id', 'text-g')
      const gridText = text_g.selectAll('.gridText')
        .data([gridData])
      gridText.enter().append('text')
        .attr('x', matrixWidth+margin.left)
        .attr('y', matrixWidth+margin.top+60)
        .style('text-anchor', 'end')
        .text(d => `from node${d.src+1} to node${d.dst+1}: ${d.value}`)
        .style('font-size', '0.7em')
    }

    //slider bar
    const sliderWidth = gridSize*gridNum,
      sliderMin = minmax[0],
      sliderMax = minmax[1]
    let selectValue
    const slider_g = svg.append('g')
      .attr('transform', `translate(${margin.left}, ${matrixWidth+margin.top})`)
    const colormap = d3.scaleSequential(d3.interpolateMagma)
      .domain([sliderWidth, 0])
    slider_g.selectAll('.sliderBar')
      .data(d3.range(sliderWidth)).enter()
      .append('rect')
      .attr('x', d => d)
      .attr('y', 10)
      .attr('width', 1)
      .attr('height', 6)
      .style('fill', d => colormap(d))
    const valueRect = slider_g.append('rect')
      .attr('x', 0)
      .attr('y', 8)
      .attr('width', 4)
      .attr('height', 10)
      .style('fill', 'white')
      .style('stroke', 'black')
      .call(d3.drag().on('drag', dragEnded))
    const valueLabel = slider_g.append('text')
      .attr('x', 0)
      .attr('y', 8)
      .style('text-anchor', 'start')
      .style('font-size', '0.7em')
      .attr('transform', 'translate(0, 30)')
      .text(`current value: ${sliderMin}`)
    function dragEnded() {
      selectValue = d3.event.x
      if(selectValue<0) {
        selectValue = 0
      }
      if(selectValue > sliderWidth) {
        selectValue = sliderWidth
      }
      valueRect.attr('x', selectValue)
      threshold = selectValue / sliderWidth * (sliderMax-sliderMin)
      valueLabel.text(`current value: ${threshold}`)
      grid.style('fill', d => d.value>=threshold?colorScale(d.value):'white')
    }

    matrixplotChart(data)
  }
}
