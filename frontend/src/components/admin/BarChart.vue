<template>
  <div ref="chart"></div>
</template>

<script>
import * as d3 from 'd3';

export default {
  props: {
    barData: {
      type: Array,
      required: true
    }
  },
  watch: {
    barData: {
      immediate: true, // Run the handler immediately on component mount
      handler(newVal, oldVal) {
        if (newVal !== oldVal) {
          this.drawChart();
        }
      }
    }
  },
  methods: {
    drawChart() {
      const data = this.barData;

      const margin = { top: 20, right: 20, bottom: 30, left: 40 };
      const width = 400 - margin.left - margin.right;
      const height = 400 - margin.top - margin.bottom;

      // Clear existing SVG before redrawing
      d3.select(this.$refs.chart).select("svg").remove();

      const svg = d3.select(this.$refs.chart)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

      const x = d3.scaleBand()
        .domain(data.map(d => d.label))
        .range([0, width])
        .padding(0.1);

      const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.value)])
        .nice()
        .range([height, 0]);

      svg.append("g")
        .call(d3.axisLeft(y));

      svg.selectAll("rect")
        .data(data)
        .enter()
        .append("rect")
        .attr("x", d => x(d.label))
        .attr("y", d => y(d.value))
        .attr("width", x.bandwidth())
        .attr("height", d => height - y(d.value))
        .attr("fill", "steelblue");

      svg.selectAll("text")
        .data(data)
        .enter()
        .append("text")
        .attr("x", d => x(d.label) + x.bandwidth() / 2)
        .attr("y", d => y(d.value) - 5)
        .attr("text-anchor", "middle")
        .text(d => d.value);

        svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x))
        .selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", "rotate(0)");
    }
  },
  mounted() {
    this.drawChart();
  }
};
</script>

<style scoped>
div {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f1f1f1;
  padding: 10px;
  box-sizing: border-box;
}

svg {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

text {
  fill: #000;
  font-family: Arial, sans-serif;
  font-size: 10px;
}

rect {
  stroke: #fff;
  stroke-width: 2px;
}
</style>