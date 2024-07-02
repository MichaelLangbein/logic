import { axisBottom, axisLeft } from "d3-axis";
import { scaleBand, scaleLinear } from "d3-scale";
import { Selection } from "d3-selection";


export function createArray<T>(size: number, fnc: (i: number) => T): T[] {
  const out: T[] = [];
  for (let i = 0; i < size; i++) {
    out.push(fnc(i));
  }
  return out;
}

export function barchart(
  svg: Selection<SVGSVGElement, unknown, null, undefined>,
  data: { label: string; value: number }[]
) {
  const fullWidth = parseFloat(svg.attr('width'));
  const fullHeight = parseFloat(svg.attr('height'));

  // set the dimensions and margins of the graph
  const margin = { top: 10, right: 30, bottom: 90, left: 40 };
  const width = fullWidth - margin.left - margin.right;
  const height = fullHeight - margin.top - margin.bottom;

  const maxVal = Math.max(...data.map((d) => d.value));

  const bodyGroup = svg.append('g').attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

  const xScale = scaleBand()
    .range([0, width])
    .domain(data.map((d) => d.label))
    .padding(0.2);
  const yScale = scaleLinear().domain([0, maxVal]).range([height, 0]);

  // bottom axis
  svg
    .append('g')
    .attr('transform', 'translate(0,' + height + ')')
    .call(axisBottom(xScale))
    .selectAll('text')
    .attr('transform', 'translate(-10,0)rotate(-45)')
    .style('text-anchor', 'end');
  // left axis
  svg.append('g').call(axisLeft(yScale));

  // Bars
  bodyGroup
    .selectAll('mybar')
    .data(data)
    .enter()
    .append('rect')
    .attr('x', (d) => xScale(d.label)!)
    .attr('y', (d) => yScale(d.value))
    .attr('width', xScale.bandwidth())
    .attr('height', (d) => height - yScale(d.value))
    .attr('fill', '#69b3a2');

  // Animation
  // svg
  //   .selectAll('rect')
  //   .transition()
  //   .duration(800)
  //   .attr('y', (d) =>y(d.value))
  //   .attr('height', (d) => height - y(d.value))
  //   .delay(function (d, i) {
  //     console.log(i);
  //     return i * 100;
  //   });
}
