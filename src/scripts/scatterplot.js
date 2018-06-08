import * as d3 from 'd3'


export default class Scatterplot {
  constructor() {
    this.width = 960 - 40 - 50
    this.height = 500 - 30 - 40
  }
  initScene(data) {
    this.renderScene(data)
  }
  renderScene(data) {
    fetch('../../static/mds_layout.json').then(res => res.json())
      .then(data => {
        const margin = {top: 30, right: 50, bottom: 40, left:40}
        const xScale = d3.scaleLinear()
          .range([0, this.width])
        const yScale = d3.scaleLinear()
          .range([this.height, 0])
        const xAxis = d3.axisBottom()
          .scale(xScale)
        const yAxis = d3.axisLeft()
          .scale(yScale)
        xScale.domain(d3.extent(data, d => d.x)).nice()
        yScale.domain(d3.extent(data, d => d.y)).nice()
        const svg = d3.select(document.getElementById('scatterplot')).append('svg')
          .attr('width', this.width + margin.left + margin.right)
          .attr('height', this.height + margin.top + margin.bottom)
        const g = svg.append('g')
          .attr('transform', `translate(${margin.left}, ${margin.top})`)
        svg.append('g')
          .attr('transform', `translate(${margin.left}, ${this.height})`)
          .attr('class', 'x axis')
          .call(xAxis)
        svg.append('g')
          .attr('transform', `translate(${margin.left}, 0)`)
          .attr('class', 'y axis')
          .call(yAxis)

        svg.selectAll('.dot').data(data)
          .enter().append('circle')
          .attr('class', 'dot')
          .attr('r', 3.5)
          .attr('cx', d => xScale(d.x))
          .attr('cy', d => yScale(d.y))
          .style('fill', () => '#4682b4')
      })
  }
}
