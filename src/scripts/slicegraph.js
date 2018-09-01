import * as d3 from 'd3'

export default class SliceGraph {
  constructor() {}
  drawFirstImage(width=512, height=384.4,
    elementId='imageview1',
    filepath='../../static/images/photo2.jpg') {
    const margin = {top: 30, right: 50, bottom: 40, left:40}
    const xScale = d3.scaleLinear()
      .range([0, width-margin.left-margin.right])
    const yScale = d3.scaleLinear()
      .range([height-margin.top-margin.bottom, 0])
    const xAxis = d3.axisBottom()
      .scale(xScale)
      .ticks(50)
      .tickSize(-(height-margin.top-margin.bottom))
      .tickFormat('')
    const yAxis = d3.axisLeft()
      .scale(yScale)
      .ticks(50)
      .tickSize(-(width-margin.left-margin.right))
      .tickFormat('')

    const svg = d3.select(document.getElementById(elementId)).append('svg')
      .attr('width', width)
      .attr('height', height)
    // image graph
    svg.append('svg:image')
      .attr('xlink:href', filepath)
      .attr('x', margin.left)
      .attr('y', margin.top)
      .attr('width', width-margin.left-margin.right)
      .attr('height', height-margin.top-margin.bottom)
    svg.append('g')
      .attr('transform', `translate(${margin.left}, ${height-margin.bottom})`)
      .attr('class', 'x axis')
      .call(xAxis)
    svg.append('g')
      .attr('transform', `translate(${margin.left}, ${margin.top})`)
      .attr('class', 'y axis')
      .call(yAxis)
  }
}
